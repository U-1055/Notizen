from PySide6.QtCore import Signal, QObject

import typing as tp
from pathlib import Path
import random
import json
import datetime

from src.src.logic import Logic
from tests.test_configs.model_test_config import TestDataModel
from src.interfaces import IModel, IView
from src.base import DataStructConst


class TestNoteWindow(QObject):
    pressed = Signal()
    closed = Signal()

    changed_date_changing = Signal(str)
    changed_content = Signal(str)
    changed_tags = Signal(list)
    changed_name = Signal(str)

    def __init__(self):
        super().__init__()
        self._name = self._content = self._tags = self._date_changing = None

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name
        self.changed_name.emit(self._name)

    @property
    def content(self) -> str:
        return self._content[0::]

    @content.setter
    def content(self, content: str):
        self._content = content
        self.changed_content.emit(self._content)

    @property
    def date_changing(self) -> str:
        return self._date_changing

    @date_changing.setter
    def date_changing(self, date_changing: str | datetime.datetime):
        self._date_changing = str(date_changing)
        self.changed_date_changing.emit(self._date_changing)

    @property
    def tags(self) -> list[str]:
        return self._tags

    @tags.setter
    def tags(self, tags: list[str, ...]):
        self._tags = tags
        self.changed_tags.emit(self._tags)


class TestNoteView(QObject):
    pressed = Signal(object)

    def __init__(self):
        super().__init__()
        self._name = self._tags = self._content = self._date_changing = None


class TestViewConfig(QObject):
    note_window_opened = Signal(TestNoteWindow)

    def __init__(self):
        super().__init__()
        self.notes: list[TestNoteView] = []

    def open_note_window(self):
        note_window = TestNoteWindow()
        self.note_window_opened.emit(note_window)
        return note_window

    def add_note(self):
        note_view = TestNoteView()
        self.notes.append(note_view)

        return note_view

    def get_selected_tags(self) -> tuple[str, ...]:
        return '', ''

    def open_main_menu(self):
        pass

    def text_search(self) -> str:
        pass

    def set_style(self, style: str):
        pass


class TestModelConfig(IModel):
    """
    Конфигурация модели для теста переключения окон.
    :param test_case_path: путь к файла JSON, содержащему структуру, аналогичную структуре DBB notes_data.
    """

    def __init__(self, test_case_path: Path, data_struct: DataStructConst):
        with open(test_case_path) as case:
            data = json.load(case)

        self._test_case = data
        self._data_struct = data_struct

    def _get_tags(self) -> set[str]:
        tags = set()
        for note in self._test_case.values():
            tuple(map(tags.add, note[self._data_struct.tags]))
        return tags

    def get_notes(self) -> tuple:
        return tuple(self._test_case.keys())

    def get_note_date_changing(self, note: str) -> str:
        return self._test_case[note][self._data_struct.date_changing]

    def get_note_tags(self, note: str) -> list[str]:
        return self._test_case[note][self._data_struct.tags]

    def get_note_data(self, note: str):
        return self._test_case[note]

    def get_note_content(self, note: str):
        return

    def get_tags(self) -> tuple[str, ...]:
        return tuple(self._get_tags())


def test(logic_class):
    view = TestViewConfig()
    model = TestModelConfig(test_case_path, DataStructConst())
    logic_class(model, view)

    note: TestNoteView = random.choice(view.notes)

    tags = model.get_note_tags(note.name)
    date_changing = model.get_note_date_changing(note.name)

    view.note_window_opened.connect(lambda window: test_window(window, tags, date_changing))
    note.pressed.emit(note)


def test_window(window: TestNoteWindow, tags: list[str], date_changing: str, content: str = ''):
    """
    Проверяет данные окна на соответствие данным из data.
    :param window: тестируемое окно TestNoteWindow
    :param tags: теги заметки
    :param date_changing: дата изменения заметки
    :param content: содержимое заметки
    """
    def check_tags(new_tags: str):
        assert new_tags == tags, f'Changed tags: {new_tags} must be {tags}'

    def check_date_changing(new_date_changing_: str):
        assert new_date_changing_ == date_changing, f'Changed date_changing: {new_date_changing_} must be {date_changing}'

    window.changed_tags.connect(check_tags)
    window.changed_date_changing.connect(check_date_changing)


if __name__ == '__main__':
    test_case_path = Path(r'C:\Users\filat\PycharmProjects\Notizen\data\test_cases\base_tests\notes_data.json')
    test(Logic)
