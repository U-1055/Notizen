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

    def __init__(self, notes: Path, notes_data: Path, resources: Path, data_struct: DataStructConst):
        self._notes, self._notes_data, self._resources, self._data_struct = notes, notes_data, resources, data_struct

    def _check_compliance(self, path: Path) -> bool:
        """Проверяет соответствие файла требованиям"""
        if path.suffix != '.txt':
            return False
        if path.stat().st_size > DataConst.max_size:
            return False
        return True

    def _check_note_data_compliance(self, note_data: dict) -> bool:
        """
        Проверяет соответствие записи о заметке (в notes_data) требованиям.
        :param note_data: словарь с данными заметки.
        :param reclaim: восстанавливать ли данные.
        """
        def check_note_data_key(note_data: dict, key: str):
            match key:

                case self._data_struct.tags:
                    if not isinstance(note_data[key], list):
                        return False

        if not isinstance(note_data, dict):
            return False
        allowed_keys = (self._data_struct.tags, self._data_struct.date_changing)

        for key in allowed_keys:  # Проверка наличия нужны ключей
            if key not in note_data:
                return False

        for key in note_data:  # Проверка на лишние ключи
            if key not in allowed_keys:
                return False
            else:
                match key:  # Проверка содержимого ключей
                    case self._data_struct.tags:
                        if not isinstance(note_data[key], list):
                            return False

        return True

    def update_state(self):
        pass

    def validate_files(self) -> list[str]:
        """Проверяет файлы на соответствие структуре (notes и DBB)."""
        damaged_notes = []  # Заметки, записи которых в notes_data некорректны (подлежат восстановлению с Model.reclaim_note)

        notes_with_content = []  # Проверка папки notes
        for file in self._notes.iterdir():
            if file.is_file() and self._check_compliance(file):
                notes_with_content.append(file.stem)

        notes_with_data = []
        with shelve.open(self._notes_data) as notes_data:  # Проверка notes_data
            for note in notes_data:
                if self._check_note_data_compliance(notes_data[note]):
                    notes_with_data.append(note)
                else:
                     damaged_notes.append(note)

        if len(notes_with_data) > len(notes_with_content):  # Если есть лишние записи в notes_data
            for note in notes_with_data:
                if not note in notes_with_content:
                    with shelve.open(self._notes_data, 'w') as notes_data:
                        notes_data.pop(note)

        if len(notes_with_content) > len(notes_with_data):  # Если есть лишние записи в notes_data
            for note in notes_with_content:
                if not note in notes_with_data:
                    Path(self._notes, f'{note}.txt').unlink()

        return damaged_notes

    def reclaim_note(self, note: str):
        with shelve.open(self._notes_data) as notes_data:
            note_data = notes_data[note]

        if self._check_note_data_compliance(note_data):
            return


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
            raise ValueError(f'Name must be unique, but name {name} already exists.')  # ToDo: доделать

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

        with open(Path(self._notes, f'{name}.txt'), 'w') as note_content:
            note_content.write('')


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
    model.add_note('note#3', ['tag1'])