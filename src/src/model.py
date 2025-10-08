import datetime
import pathlib
import shelve
from pathlib import Path
from src.base import DataConst, DataStructConst


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

    def update_state(self):
        pass

    def validate_files(self):
        """Проверяет файлы на соответствие структуре (notes и DBB)."""

    def reclaim_note(self):
        pass

    def get_style(self) -> str:
        """Возвращает стиль QSS."""
        # ToDo: узнать про взаимодействие с файлом ресурсов

    def get_note_tags(self, note: str) -> tuple[str, ...]:
        with shelve.open(self._notes_data) as notes_data:
            return notes_data[note][self._data_struct.tags]

    def get_tags(self) -> tuple[str, ...]:
        pass

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

        note_content_path = Path(self._notes, f'{note}.txt')
        note_content_path.unlink()

    def change_note_name(self, note: str, name: str):
        if name in self.get_notes():  # Проверка на уникальность названия
            raise ValueError(f'Name must be unique, but name {name} already exists.')

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
        assert note not in notes_after, f'Note {note} must has deleted'


    notes_data_path = Path('..', '..', 'data', 'notes_data', 'notes_data')
    notes_path = Path('..', '..', 'notes')
    resource_path = Path('..', '..', 'data', 'gui_data', 'resource.qrc')

    model = DataModel(notes_path, notes_data_path, resource_path, DataStructConst())

    check_changed_note('note#1', ['tag#1', 'tag#25'], '23.12.12')
