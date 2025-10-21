import json
import shelve
from pathlib import Path
import typing as tp

from src.src.model import DataModel
from src.base import DataStructConst

invalid_note_structs_path = Path('..', '..', 'data', 'test_cases', 'base_tests', 'invalid_notes.json')
normal_note_names = tuple(map(lambda i: f'note#{i}', range(1, 11)))
notes_without_data = tuple(map(lambda i: f'no_note_data_note#{i}', range(1, 6)))
notes_invalid = tuple(map(lambda i: f'invalid_note#{i}', range(1, 6)))
notes_damaged = tuple(map(lambda i: f'damaged_note#{i}', range(1, 6)))
notes_without_file = tuple(map(lambda i: f'no_file_note#{i}', range(1, 6)))


class TestBaseManager:

    def __init__(self, notes_path: Path, notes_data_path: Path, data_struct: DataStructConst):
        self._notes_path, self._notes_data_path, self._data_struct = notes_path, notes_data_path, data_struct

    def create_file(self, file_name: str):
        """Создаёт файл в notes."""
        with open(Path(self._notes_path, file_name), 'w') as note:
            note.write('')

    def create_note_data(self, note: str, tags: list[str] | tuple[str, ...], date_changing: str):
        """Создаёт запись о заметке в notes_data."""
        data = self._data_struct.note_struct
        data[self._data_struct.tags] = tags
        data[self._data_struct.date_changing] = date_changing

        with shelve.open(self._notes_data_path, 'w') as notes_data:
            notes_data[note] = data

    def get_note_data(self, note: str):
        with shelve.open(self._notes_data_path) as notes_data:
            return notes_data[note]


def clear_base(notes_data_path: Path, notes_path: Path):
    with shelve.open(notes_data_path, 'w') as notes_data:
        notes_data.clear()

    tuple(path.unlink() for path in notes_path.iterdir())


def set_test_state_1(notes_data_path: Path, notes_path: Path):
    """
    Устанавливает тестовое состояние: 25 файлов в notes и 20 записей: из них 5 файлов не имеют записи, 5 - невалидны,
    5 записей повреждены, 5 не имеют файла, остальные валидны.
    """
    data_struct = DataStructConst()
    with open(invalid_note_structs_path) as file:
        invalid_note_structs = json.load(file)

    for name in normal_note_names:  # Создание валидных заметок
        with open(Path(notes_path, f'{name}.txt'), 'w') as note:
            note.write('')
        with shelve.open(notes_data_path, 'w') as notes_data:
            notes_data[name] = data_struct.note_struct

    for name in notes_without_data:  # Создание заметок без записи
        with open(Path(notes_path, f'{name}.txt'), 'w') as note:
            note.write('')

    for idx, name in enumerate(notes_damaged):  # Создание повреждённых записей
        with shelve.open(notes_data_path, 'w') as note:
            note[name] = invalid_note_structs[idx]

        with open(Path(notes_path, f'{name}.txt'), 'w') as note_data:
            note_data.write('')

    for name in notes_invalid:  # Создание заметок неверного файла
        with open(Path(notes_path, f'{name}.png'), 'w') as invalid_file:
            invalid_file.write('')

        with shelve.open(notes_data_path, 'w') as notes_data:
            notes_data[name] = data_struct.note_struct

    for name in notes_without_file:  # Создание заметок без содержимого (файла notes)
        with shelve.open(notes_data_path) as notes_data:
            notes_data[name] = data_struct.note_struct


def test(model: DataModel,
         test_base_manager: TestBaseManager,
         notes_must_be_deleted: list[str] = None,
         notes_data_must_be_deleted: list[str] = None,
         notes_must_be_created: list[str] = None,
         notes_must_be_damaged: list[str] = None,
         notes_must_be_reclaimed: list[str] | tuple[str, ...] = None,
         check_reclaim: tp.Callable = None
         ):
    """

    Тестирует проверку состояния DataModel.

    :param notes_must_be_deleted: заметки, которые должны быть удалены во время проверки (есть запись - нет файла).
    :param notes_data_must_be_deleted: файлы notes, которые должны быть удалены (не соответствуют требованиям).
    :param notes_must_be_created: заметки, которые должны быть созданы (валидный файл в notes есть - записи в notes_data нет)
    :param notes_must_be_damaged: заметки, которые должны быть отмечены как повреждённые
    :param notes_must_be_reclaimed: повреждённые заметки, которые должны быть восстановлены

    """

    notes_before = list(model.get_notes())  # Записи о заметках и файлы содержимого заметок
    notes_data_before = list(map(lambda path: path.stem, model.notes.iterdir()))

    if notes_must_be_deleted is not None:
        notes_must_be_deleted = list(notes_must_be_deleted)
        for i, note in enumerate(notes_must_be_deleted):  # Проверка на существование заметок, которые должны быть удалены
            if note not in notes_before:
                list(notes_must_be_deleted).pop(i)

        for note in notes_before:  # Проверка заметок без содержимого (нет файла в notes_data)
            if note not in notes_data_before:
                notes_must_be_deleted.append(note)

    if notes_data_must_be_deleted is not None:
        notes_data_must_be_deleted = list(notes_data_must_be_deleted)
        for i, note_data in enumerate(notes_data_must_be_deleted):  # Проверка на существование записи о заметке, которая (запись) должна быть удалена
            if not Path(model.notes_data, f'{note_data}.txt').is_file():
                notes_data_must_be_deleted.pop(i)

    if notes_must_be_created is not None:
        notes_must_be_created = list(notes_must_be_created)

        for note_data in notes_data_before:  # Проверка файлов notes без записи о заметке (есть содержимое - нет записи)
            note_data_path = Path(model.notes_data, f'{note_data}.txt')

            if not note_data_path.is_file():
                continue

            if note_data not in notes_before and model._check_compliance(note_data_path):
                notes_must_be_created.append(note_data)

        for i, note in enumerate(notes_must_be_created):  # Проверка на наличие уже существующих записей
            if note in notes_before:
                notes_must_be_created.pop(i)

    if notes_must_be_reclaimed is not None:
        for i, note in enumerate(notes_must_be_reclaimed):
            if note not in notes_before:
                notes_must_be_reclaimed.pop(i)

    damaged_notes = model.validate_files()

    notes_after = model.get_notes()
    notes_data_after = [path.stem for path in model.notes.iterdir()]

    if notes_must_be_deleted is not None:
        for note in notes_must_be_deleted:
            assert note not in notes_after, (f'This note must be deleted: {note}. \n '
                                             f'Notes for deleting: {notes_must_be_deleted} \n'
                                             f'Notes after: {notes_after} \n'
                                             f'Notes before: {notes_before}')

    if notes_data_must_be_deleted is not None:
        for note_data in notes_data_must_be_deleted:
            assert note_data not in notes_data_after, f'This note_data file must be deleted: {note_data}'

    if notes_must_be_created is not None:
        for note in notes_must_be_created:
            assert note in notes_after, f'This note must be created: {note}'

    if notes_must_be_damaged is not None:
        for note in notes_must_be_damaged:
            assert note in damaged_notes, (f'This note must be marked as damaged: {note}. \n'
                                           f'Notes marked as damaged: {damaged_notes} \n'
                                           f'Notes must be marked as damaged: {notes_must_be_damaged}')

    if notes_must_be_reclaimed and check_reclaim:

        for note in notes_must_be_reclaimed:
            model.reclaim_note(note)
            note_data = test_base_manager.get_note_data(note)

            assert check_reclaim(note_data), (f'This note must be reclaimed, but it is invalid: {note} \n'
                                                                          f'Note data: {note_data}')

    print(f'Test completed. State: \n Notes: {notes_after} \n Note_files: {notes_data_after}')


if __name__ == '__main__':
    def run_test():
        try:
            test(
                DataModel(notes_path, notes_data_path, resource_path, DataStructConst()), test_base_manager,
                notes_must_be_reclaimed=notes_damaged,
                check_reclaim=lambda note_data: False if model._check_note_data_compliance(note_data) else True
            )
            print([test_base_manager.get_note_data(note) for note in notes_damaged])
        except AssertionError as error:
            print(model.get_notes())
            print([path.stem for path in notes_path.iterdir()])
            raise error


    notes_data_path = Path('..', '..', 'data', 'test_cases', 'model_tests', 'test_data_struct', 'notes_data')
    notes_path = Path('..', '..', 'data', 'test_cases', 'model_tests', 'test_data_struct', 'notes')
    resource_path = Path('..', '..', 'data', 'gui_data', 'resource.qrc')

    clear_base(notes_data_path, notes_path)
    set_test_state_1(notes_data_path, notes_path)
    test_base_manager = TestBaseManager(notes_path, notes_data_path, DataStructConst())

    model = DataModel(notes_path, notes_data_path, resource_path, DataStructConst())

    run_test()
