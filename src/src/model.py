from PySide6.QtCore import QFile

import datetime
import pathlib
import shelve
from pathlib import Path

from src.base import DataConst, DataStructConst
import src.gui.resources_rc


class DataModel:
    """
    Модель. Работает с данными: заметками и данными GUI (стилями, иконками и пр.)
    """
    # Ключи, которые возвращает метод _check_note_data_compliance
    unknown_tags_type = 0  # Некорректный тип данных в поле tags
    unknown_date_type = 1  # Некорректный тип данных в поле date_changing
    unknown_keys = 2  # Лишние ключи в записи
    no_keys = 3  # Нет нужных ключей в записи
    no_dict_type = 4  # Тип записи - не dict
    correct_note = 5  # Заметка корректна

    err_codes = (unknown_tags_type, unknown_date_type, unknown_keys, no_keys)

    def __init__(self, notes: Path, notes_data: Path, resources: Path, data_struct: DataStructConst):
        self._notes, self._notes_data, self._resources, self._data_struct = notes, notes_data, resources, data_struct

    @property
    def notes(self) -> Path:
        """Возвращает путь к папке с заметками."""
        return self._notes

    @property
    def notes_data(self) -> Path:
        """Возвращает путь к базе данных."""
        return self._notes_data

    @property
    def resources(self) -> Path:
        """Возвращает путь к файлу ресурсов."""
        return self._resources

    @property
    def data_struct(self) -> DataStructConst:
        """Возвращает экземпляр класса набора констант DataStructConst."""
        return self._data_struct

    def _check_compliance(self, path: Path) -> bool:
        """Проверяет соответствие файла требованиям"""
        if path.suffix != '.txt':
            return False
        if path.stat().st_size > DataConst.max_size:
            return False
        return True

    def _check_note_data_compliance(self, note_data: dict) -> list:  # ToDo: сделать так, чтобы метод возвращал список кодов ошибки (сделано)
        """
        Проверяет соответствие записи о заметке (в notes_data) требованиям. Возвращает один из err_codes или True, если
        запись корректная.
        :return: Список кодов ошибки.
        :param note_data: словарь с данными заметки.
        """
        err_codes = []  # Список кодов ошибки

        if not isinstance(note_data, dict):
            err_codes.append(self.no_dict_type)
        allowed_keys = (self._data_struct.tags, self._data_struct.date_changing)

        for key in allowed_keys:  # Проверка наличия нужны ключей
            if key not in note_data:
                err_codes.append(self.no_keys)

        for key in note_data:  # Проверка на лишние ключи
            if key not in allowed_keys:
                err_codes.append(self.unknown_keys)
            else:
                match key:  # Проверка типов содержимого ключей
                    case self._data_struct.tags:
                        if not isinstance(note_data[key], list):
                            err_codes.append(self.unknown_tags_type)
                        else:
                            for tag in note_data[key]:  # Проверка типов тегов
                                if not isinstance(tag, str):
                                    err_codes.append(self.unknown_tags_type)

                    case self._data_struct.date_changing:
                        if not isinstance(note_data[key], str):
                            err_codes.append(self.unknown_date_type)  # ToDo: сделать проверку соответствия формату даты

        return err_codes  # Заметка корректна

    def _get_note_file_date_changing(self, note: str) -> datetime:
        """Возвращает дату последнего изменения файла заметки."""
        path = Path(self._notes, f'{note}.txt')
        return datetime.datetime.fromtimestamp(path.stat().st_mtime).date().strftime(self._data_struct.datetime_date_format)

    def update_state(self):
        pass

    def validate_files(self) -> list[str]:
        """Проверяет файлы на соответствие структуре (notes и DBB)."""
        damaged_notes = []  # Заметки, записи которых в notes_data некорректны (подлежат восстановлению с Model.reclaim_note)

        notes_with_content = []
        for file in self._notes.iterdir():  # Проверка папки notes на валидность файлов
            if file.is_file():
                if self._check_compliance(file):
                    notes_with_content.append(file.stem)
                else:
                    file.unlink()
                    if file.stem in self.get_notes():
                        self.delete_note(file.stem)

        notes_with_data = []
        with shelve.open(self._notes_data) as notes_data:  # Проверка notes_data
            for note in notes_data:
                if self._check_note_data_compliance(notes_data[note]) == []:  # Вернули пустой список
                    notes_with_data.append(note)
                else:
                    damaged_notes.append(note)

        for note in [*notes_with_data, *damaged_notes]:  # Удаление заметок без файла
            if note not in notes_with_content:
                self.delete_note(note)

        for note in notes_with_content:  # Создание заметок по валидным файлам notes без записи в notes_data
            if note not in notes_with_data and note not in damaged_notes:
                self.add_note(note, [])  # Если новый файл в notes_data - создаётся новая заметка с именем файла и без тегов

        notes = self.get_notes()
        return filter(lambda note: note in notes, damaged_notes)  # Отсеивание удалённых заметок

    def reclaim_note(self, note: str):
        with shelve.open(self._notes_data) as notes_data:
            note_data = notes_data[note]

            err_codes = self._check_note_data_compliance(note_data)
            allowed_keys = self._data_struct.note_struct.keys()  # Ключи записи в notes_data

            if err_codes:  # Вернули непустой список
                for code in err_codes:
                    match code:
                        case self.unknown_keys:  # Лишние ключи
                            for key in list(note_data.keys()):
                                if key not in allowed_keys:
                                    note_data.pop(key)

                        case self.no_keys:  # Отсутствуют нужные ключи
                            for key in self._data_struct.note_struct.keys():
                                if key not in note_data:
                                    if key == self._data_struct.tags:
                                        note_data[key] = []  # Создание тега
                                    elif key == self._data_struct.date_changing:
                                        note_data[key] = str(self._get_note_file_date_changing(note))  # Создание метки
                        case self.unknown_tags_type:
                            tags = note_data[self._data_struct.tags]
                            if isinstance(tags, list):  # Восстановление тегов с неверным типом
                                for i, tag in enumerate(tags):
                                    if not isinstance(tag, str):
                                        note_data[self._data_struct.tags].pop(i)
                            else:
                                note_data[self._data_struct.tags] = []

                        case self.unknown_date_type:
                            note_data[self._data_struct.date_changing] = str(self._get_note_file_date_changing(note))

            notes_data[note] = note_data

    def get_style(self, style: str) -> str:
        """
        Возвращает стиль QSS.
        :param style: путь к стилю
        """

        style_file = QFile(style)

        style_file.open(QFile.OpenModeFlag.ReadOnly)
        style = style_file.readAll().toStdString()
        return style

    def get_last_style(self) -> str:
        """Возвращает установленный пользователем стиль (из config.json)"""
        return self._data_struct.light_theme

    def get_note_tags(self, note: str) -> tuple[str, ...]:
        with shelve.open(self._notes_data) as notes_data:
            return notes_data[note][self._data_struct.tags]

    def get_tags(self) -> tuple[str, ...]:
        with shelve.open(self._notes_data) as notes_data:
            tags = set()
            for note in notes_data.values():
                tuple(map(tags.add, note[self._data_struct.tags]))
            return tuple(tags)

    def get_note_content(self, note: str) -> str:
        with open(Path(self._notes, f'{note}.txt')) as note_content:
            return note_content.read()

    def get_note_date_changing(self, note: str) -> str:
        with shelve.open(self._notes_data, 'r') as notes_data:
            return notes_data[note][self._data_struct.date_changing]

    def get_notes(self) -> tuple:
        """Возвращает список со всеми заметками"""
        with shelve.open(self._notes_data, 'r') as notes_data:
            return tuple(notes_data.keys())

    def set_note_date_changing(self, note: str, date_changing: str):
        with shelve.open(self._notes_data, 'r') as notes_data:
            data = notes_data[note]
            data[self._data_struct.date_changing] = date_changing  # ToDo: разобраться с этим и примером из доки (изменением в одном контекстном менеджере)

        with shelve.open(self._notes_data, 'w') as notes_data:
            notes_data[note] = data

    def set_note_tags(self, note: str, tags: list[str] | tuple[str, ...]):
        with shelve.open(self._notes_data, 'r') as notes_data:
            data = notes_data[note]
            data[self._data_struct.tags] = tags

        with shelve.open(self._notes_data, 'w') as notes_data:
            notes_data[note] = data

    def set_note_content(self, note: str, content: str):
        with open(Path(self._notes, f'{note}.txt')) as note_content:
            note_content.write(content)

    def delete_note(self, note: str):
        with shelve.open(self._notes_data, 'w') as notes_data:
            notes_data.pop(note)

        try:
            note_content_path = Path(self._notes, f'{note}.txt')
            note_content_path.unlink()
        except FileNotFoundError:
            pass

    def change_note_name(self, note: str, name: str):
        if name in self.get_notes():  # Проверка на уникальность названия
            raise ValueError(f'Name must be unique, but name {name} already exists.')

        Path(self._notes, f'{note}.txt').rename(Path(self._notes, f'{name}.txt'))  # Переименование файла в notes

        with shelve.open(self._notes_data) as notes_data:  # Переименование записи в notes_data
            note_data = notes_data.pop(note)
            notes_data[name] = note_data

    def add_note(self, name: str, tags: list[str] | tuple[str, ...]):
        with shelve.open(self._notes_data, 'w') as notes_data:
            if name in notes_data:  # Проверка на уникальность названия
                raise ValueError(f'Name must be unique, but name {name} already exists.')

            note_struct = self._data_struct.note_struct  # Инициализация данных заметки
            note_struct[self._data_struct.tags] = tags
            note_struct[self._data_struct.date_changing] = str(datetime.date.today().strftime(self._data_struct.datetime_date_format))

            notes_data[name] = note_struct

        try:
            with open(Path(self._notes, f'{name}.txt'), 'w') as note_content:  # Создание записи о заметке
                note_content.write('')
        except (FileExistsError, IOError, PermissionError) as error:
            print(error)


if __name__ == '__main__':
    def check_note(note: str, tags: list[str] | tuple[str, ...] = None, date_changing: str = None, content: str = None):

        saved_tags = model.get_note_tags(note)
        saved_date_changing = model.get_note_date_changing(note)
        saved_content = model.get_note_content(note)

        if tags:
            assert saved_tags == tags, f'New: {tags}, Saved: {saved_tags}'
        if date_changing:
            assert saved_date_changing == date_changing, f'New: {date_changing}, Saved: {saved_date_changing}'
        if content:
            assert saved_content == content, f'New: {content}, Saved: {saved_content}'
        print('Test completed')

    def check_changed_note(note: str,
                           new_tags: list[str] | tuple[str, ...] = None,
                           new_date_changing: str = None,
                           new_content: str = None
                           ):
        if new_tags:
            model.set_note_tags(note, new_tags)
        if new_date_changing:
            model.set_note_date_changing(note, new_date_changing)
        if new_content:
            model.set_note_content(note, new_content)

        check_note(note, new_tags, new_date_changing, new_content)

    def check_deleted_note(note: str):
        notes_before = model.get_notes()
        assert note in notes_before, f'Note {note} must be an existing note'
        model.delete_note(note)
        notes_after = model.get_notes()
        assert note not in notes_after, f'Note {note} must has been deleted'

    def check_renamed_note(note: str, new_name: str):
        saved_tags, saved_date_changing, saved_content = (model.get_note_tags(note),
                                                          model.get_note_date_changing(note),
                                                          model.get_note_content(note))
        model.change_note_name(note, new_name)
        check_note(new_name, saved_tags, saved_date_changing, saved_content)

    notes_data_path = Path('..', '..', 'data', 'notes_data', 'notes_data')
    notes_path = Path('..', '..', 'notes')
    resource_path = Path('..', '..', 'data', 'gui_data', 'resource.qrc')

    model = DataModel(notes_path, notes_data_path, resource_path, DataStructConst())
    for note in model.get_notes():
        model.delete_note(note)

    for i in range(10):
        model.add_note(f'note#{i}', [])