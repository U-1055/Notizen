import pytest
from PySide6.QtCore import Signal, QObject

import typing as tp
from pathlib import Path
from datetime import datetime

from src.src.logic import Logic
from src.base import GuiLabels, GuiConst, DataStructConst
from tests.logic_tests.note_window_test import TestNoteWindow
from tests.mock_objects import MockTagWidget, MockWindowDamagedNotes


class TestNoteView(QObject):
    pressed = Signal(object)  # См. оригинальный виджет
    btn_delete_pressed = Signal(object)
    def __init__(self):
        super().__init__()
        self.name = self.tags = self.content = self.date_changing = None

    def press_btn_delete(self):
        self.btn_delete_pressed.emit(self)

    def hide(self):
        del self

    def setMenu(self, menu):
        pass

class TestDataModel:
    """Тестовая модель данных."""
    note_deleted = Signal(str)  # Заметка удалена, возвращает имя заметки
    note_created = Signal(str)  # Заметка создана, возвращает имя заметки

    def __init__(self):
        self._main_struct = {}
        self.data_struct = DataStructConst()

    def _check_compliance(self, path: Path) -> bool:
        """Проверяет соответствие файла требованиям"""
        pass

    def _check_note_data_compliance(self, note_data: dict) -> list:  # ToDo: сделать так, чтобы метод возвращал список кодов ошибки (сделано)
        pass

    def _get_note_file_date_changing(self, note: str) -> datetime:
        """Возвращает дату последнего изменения файла заметки."""
        return datetime.today()

    def update_state(self):
        pass

    def validate_files(self) -> tuple[str, ...]:
        """Проверяет файлы на соответствие структуре (notes и DBB)."""
        return ()

    def reclaim_common_data(self, common_data: dict) -> dict:
        """Восстанавливает common_data при наличии повреждений."""
        pass

    def reclaim_note(self, note: str):
        pass

    def get_style(self, style: str) -> str:
        """
        Возвращает стиль QSS.
        :param style: путь к стилю
        """
        return ''

    def get_last_style(self) -> str:
        """Возвращает установленный пользователем стиль (из config.json)"""
        return ''

    def get_note_tags(self, note: str) -> tuple[str, ...]:
        return self._main_struct[note][self.data_struct.tags]

    def get_tags(self) -> tuple[str, ...]:
        """Возвращает все теги."""
        return self.get_notes_tags()

    def get_notes_tags(self) -> tuple[str, ...]:
        """Возвращает теги, к которым прикреплены заметки."""
        tags = set()
        for note in self._main_struct:
            list(tags.add(tag) for tag in self._main_struct[note][self.data_struct.tags])
        return tuple(tags)

    def get_note_content(self, note: str) -> str:
        return ''

    def get_note_date_changing(self, note: str) -> str:
        return ''

    def get_notes(self) -> tuple:
        return tuple(self._main_struct.keys())

    def set_note_date_changing(self, note: str, date_changing: str):
        pass

    def set_note_tags(self, note: str, tags: list[str] | tuple[str, ...]):
        pass

    def set_note_content(self, note: str, content: str):
        pass

    def delete_note(self, note: str):
        self._main_struct.pop(note)

    def change_note_name(self, note: str, name: str):
        """
        Изменяет название заметки.
        :param note: текущее название заметки.
        :param name: новое название.
        """
        if name in self.get_notes():
            raise ValueError
        self._main_struct[name] = self._main_struct[note]
        self._main_struct.pop(note)

    def add_tag(self, tag: str):
        pass

    def add_note(self, name: str, tags: list[str] | tuple[str, ...]):
        self._main_struct[name] = {
            self.data_struct.tags: tags,
            self.data_struct.date_changing: datetime.today().date().strftime(self.data_struct.datetime_date_format)
        }


class TestMainWindow(QObject):

    btn_create_note_pressed = Signal()
    btn_tags_pressed = Signal()
    btn_dark_theme_pressed = Signal()
    btn_light_theme_pressed = Signal()
    btn_add_tag_pressed = Signal()
    tried_to_close = Signal()  # Окно попытались закрыть
    btn_search_pressed = Signal()  # Нажата кнопка поиска
    btn_update_pressed = Signal()  # Нажата кнопка "Обновить"

    showed = Signal()

    def __init__(self):
        super().__init__()
        self._note_views: list[TestNoteView] = []  # Размещённые заметки TestNoteView
        self._opened_note_window = None  # Открытое окно TestNoteWindow

        self._search_text = ''
        self._tags: list[str] = []

    @property
    def notes(self):
        return [note_view.name for note_view in self._note_views]

    @property
    def opened_note_window(self) -> TestNoteWindow:
        return self._opened_note_window

    @property
    def note_views(self) -> list[TestNoteView]:
        return self._note_views

    def set_search_text(self, text: str):
        self._search_text = text

    def set_tags(self, tags: list[str] | tuple[str, ...]):
        self._tags = tags

    def _show_damaged_notes_window(self, window):
        pass

    def try_to_close(self):
        self.tried_to_close.emit()

    def press_btn_create_note(self):
        self.btn_create_note_pressed.emit()

    def press_btn_tags(self):
        self.btn_tags_pressed.emit()

    def press_btn_dark_theme(self):
        self.btn_dark_theme_pressed.emit()

    def press_btn_light_theme(self):
        self.btn_light_theme_pressed.emit()

    def press_btn_search(self):
        self.btn_search_pressed.emit()

    def press_btn_update(self):
        self.btn_update_pressed.emit()

    def show_no_found_label(self, text: str):
        pass
    def open_main_menu(self):
        pass

    def set_style(self, style: str):
        pass

    def clear_notes(self):
        self._note_views = []

    def add_note(self) -> TestNoteView:
        note_view = TestNoteView()
        self._note_views.append(note_view)
        return note_view

    def open_note_window(self) -> TestNoteWindow:
        self._opened_note_window = TestNoteWindow()
        return self._opened_note_window

    def get_menu(self, elements: tuple[tuple[str, tp.Callable], ...]) -> None:
        pass

    def get_tag_widget(self) -> MockTagWidget:
        """Возвращает виджет тегов."""
        wdg_tags = MockTagWidget()
        wdg_tags.set_tags(self._tags)
        return wdg_tags

    def get_tag_window(self):
        pass

    def get_create_note_window(self):
        pass

    def show_message(self, title: str, message: str):
        pass

    def open_damaged_notes_window(self) -> MockWindowDamagedNotes:
        return MockWindowDamagedNotes()

    def get_selected_tags(self) -> tuple[str, ...]:
        return tuple(self._tags)

    def search_text(self) -> str:
        return self._search_text

    def showEvent(self, event, /):
        self.showed.emit()

    def closeEvent(self, event, /):
        self.try_to_close()

    def _setup_widgets(self):
        pass


def set_model(notes: list[tuple[str, tuple[str, ...]]]):
    model = TestDataModel()
    for note in notes:
        model.add_note(note[0], note[1])
    return model


all_notes_1 = \
    [
        *[(f'note#{i}', ['tag1', 'tag2']) for i in range(5)],
        *[(f'note#{i}', ['tag3']) for i in range(5, 10)],
        *[(f'sth', []) for i in range(10)]
    ]

relevant_notes_1 = list(f'note#{i}' for i in range(5, 10))

all_notes_2 = \
    [
        *[(f'sth{i}', []) for i in range(10)]
    ]

relevant_notes_2 = [f'sth{i}' for i in range(10)]


def set_test_state(notes: list[tuple[str, tuple[str, ...]]]) -> TestMainWindow:
    view = TestMainWindow()
    model = set_model(notes)
    logic = Logic(model, view, GuiLabels(), GuiConst(), DataStructConst())
    return view

@pytest.mark.parametrize(
    ('search_text', 'tags', 'expecting_notes', 'notes'),
    (
            (
                'note', ['tag3'],  # Найти заметки с названием, включающим note и тегом tag3
                relevant_notes_1,
                all_notes_1,
             ),
            (
                '', 'tag1',  # Ничего не делать, т.к. поискового текста нет (Заметки не должны измениться)
                relevant_notes_2,
                all_notes_2
            )
    )
)
def test_search(search_text: str, tags: list[str] | tuple[str, ...], expecting_notes: list[str] | tuple[str, ...], notes: list[tuple[str, tuple[str, ...]]]):
    test_view = set_test_state(notes)
    test_view.set_search_text(search_text)
    test_view.set_tags(tags)
    test_view.press_btn_search()

    shown_notes = test_view.notes
    assert shown_notes == expecting_notes


@pytest.mark.parametrize(
    ('note_name', 'notes'),
    [(f'new_note{i}', all_notes_1) for i in range(10)]

)
def test_create_note(note_name: str, notes: list[tuple[str, tuple[str, ...]]]):
    test_view = TestMainWindow()
    model = set_model(notes)
    logic = Logic(model, test_view, GuiLabels(), GuiConst(), DataStructConst())
    test_view.press_btn_create_note()

    notes_before = model.get_notes()
    assert note_name not in notes_before  # Заметки ещё не существует

    note_window = test_view.opened_note_window
    note_window.change_name(note_name)  # Создание заметки с заданным именем
    note_window.btn_save_pressed.emit()
    note_window.btn_return_pressed.emit()

    notes_after = model.get_notes()
    assert note_name in notes_after  # Заметка добавлена
    notes_in_view_after = test_view.notes
    assert note_name in notes_in_view_after

@pytest.mark.parametrize(
    ('note_name', 'notes'),
    [(f'note#{i}', all_notes_1) for i in range(10)]

)
def test_delete_note(note_name: str, notes: list[tuple[str, tuple[str, ...]]]):
    test_view = TestMainWindow()
    model = set_model(notes)
    logic = Logic(model, test_view, GuiLabels(), GuiConst(), DataStructConst())

    assert note_name in model.get_notes()
    note_views: list[TestNoteView] = test_view.note_views

    for note_view in note_views:
        if note_view.name == note_name:
            note_view.press_btn_delete()

    assert note_name not in model.get_notes()


if __name__ == '__main__':
    pass
