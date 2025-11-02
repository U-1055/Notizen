import pytest
from PySide6.QtCore import Signal, QObject

from src.src.logic import NoteWindowHandler
from src.src.model import DataModel
from src.gui.widgets import NoteWindow
from src.base import DataStructConst, GuiLabels
from tests.mock_objects import MockTagWidget


class TestNoteWindow(QObject):
    # Сигналы для имитации NoteWindow
    tried_to_close = Signal()  # Сигнал закрытия окна
    name_changed = Signal()  # Название изменено
    text_changed = Signal()  # Текст изменён
    tags_changed = Signal()  # Теги изменены
    btn_save_pressed = Signal()  # Нажата кнопка сохранения
    btn_delete_pressed = Signal()  # Нажата кнопка удаления заметки
    btn_return_pressed = Signal()  # Нажата кнопка "Назад"

    # Сигналы для тестов
    error_shown = Signal()
    save_message_shown = Signal()


    def __init__(self):
        super().__init__()
        self.name = self.tags = self.content = self.date_changing = None

    def on_btn_delete_pressed(self):
        pass

    def on_tried_to_close(self):
        pass

    def set_ops_menu(self, menu):
        pass

    def show_error(self, text: str):
        self.error_shown.emit()

    def show_save_message(self, text: str):
        from src.gui.widgets import WindowSave
        self.save_message_shown.emit()
        return WindowSave

    def change_name(self, name: str):
        self.name = name
        self.name_changed.emit()

    def change_content(self, content: str):
        self.content = content
        self.text_changed.emit()

    def change_tags(self, tags: list[str] | tuple[str, ...]):
        self.tags = tags
        self.tags_changed.emit()

    def get_tag_widget(self) -> MockTagWidget:
        return MockTagWidget()



class TestDataModel(QObject):
    note_deleted = Signal()  # Заметка удалена
    new_tags_set = Signal()  # Изменены теги
    new_content_set = Signal()  # Изменено содержимое заметки
    new_date_changing_set = Signal()  # Изменена дата изменения
    new_name_set = Signal(tuple[str, str])  # Изменено имя заметки

    def __init__(self, note: str, tags: list[str] | tuple[str, ...], content: str, date_changing: str):
        super().__init__()
        self.note, self.tags, self.content, self.date_changing = note, tags, content, date_changing

    def _set_new_name(self):
        self.new_name_set.emit()

    def delete_note(self):
        self.note_deleted.emit()

    def set_note_tags(self, _: str, tags: list[str] | tuple[str, ...]):
        self.tags = tags
        self.new_tags_set.emit()

    def set_note_content(self, _: str, content: str):
        self.content = content
        self.new_content_set.emit()

    def set_note_date_changing(self, _: str, date_changing: str):
        self.date_changing = date_changing
        self.new_date_changing_set.emit()

    def change_note_name(self, _: str, name: str):
        self.note = name
        self.new_name_set.emit()


class NoteWindowHandlerTest:
    def __init__(self, note_window: TestNoteWindow):
        self._note_window = note_window
        self._test_data_model = TestDataModel(self._note_window.name, self._note_window.tags, self._note_window.content,
                                              self._note_window.date_changing)
        self._note_window_handler: NoteWindowHandler = NoteWindowHandler(note_window.name, note_window, self._test_data_model, GuiLabels(), DataStructConst())

        self._error_shown = self._save_message_shown = self._note_deleted = self._tags_changed = self._name_changed = \
        self._content_changed = self._date_changing_changed = False

        self._note_window.error_shown.connect(self._on_error_shown)
        self._note_window.save_message_shown.connect(self._on_save_message_shown)

    def _on_error_shown(self):
        self._error_shown = True

    def _on_save_message_shown(self):
        self._save_message_shown = True

    def _on_note_deleted(self):
        self._note_deleted = True

    def _on_name_changed(self):
        self._name_changed = True

    def _on_tags_changed(self):
        self._tags_changed = True

    def _on_content_changed(self):
        self._content_changed = True

    def _on_date_changing_changed(self):
        self._date_changing_changed = True

    def test_base(self, name: str):
        """Тест-пример"""
        assert self._note_window_handler._name == name

    def test_output(self, new_name: str):
        """Тестирует выведение окна сохранения при попытке выхода."""
        self._note_window.change_name(new_name)
        self._note_window.tried_to_close.emit()
        assert self._save_message_shown, 'The save-window must be shown after try to close'

    def test_renaming(self, new_name: str):
        self._note_window.change_name(new_name)
        self._note_window.btn_save_pressed.emit()
        assert self._test_data_model.note == new_name, (f'The name of the note ({self._test_data_model.note}) '
                                                        f'must be equal to the new name {new_name}')


@pytest.fixture()
def note_window() -> TestNoteWindow:
    return TestNoteWindow()


def set_note_win_test(
        note_window: TestNoteWindow,
        name: str,
        tags: list[str] | tuple[str, ...],
        content: str,
        date_changing: str) -> NoteWindowHandlerTest:

    note_window.name = name
    note_window.tags = tags
    note_window.content = content
    note_window.date_changing = date_changing

    return NoteWindowHandlerTest(note_window)

@pytest.mark.parametrize(
        'name, tags, content, date_changing',
        (
                ('note#1', ['tag1'], 'New content', '31.10.2025'),
                ('note#2', ['tag1', 'tag2'], 'New content', '31.10.2025'),
                ('note#3', ['tag2', 'tag3'], 'New content', '31.10.2025')
        )
    )
def test_base(note_window: TestNoteWindow, name: str, tags: list[str] | tuple[str, ...], content: str, date_changing: str):
    note_win_test = set_note_win_test(note_window, name, tags, content, date_changing)
    note_win_test.test_base(name)


@pytest.mark.parametrize(
        'name, tags, content, date_changing, new_name',
        (
                ('note#1', ['tag1'], 'New content', '31.10.2025', 'note#4'),
                ('note#2', ['tag1', 'tag2'], 'New content', '31.10.2025', 'note#5'),
                ('note#3', ['tag2', 'tag3'], 'New content', '31.10.2025', 'note#6')
        )
    )
def test_renaming(note_window: TestNoteWindow, name: str, tags: list[str] | tuple[str, ...], content: str, date_changing: str,
                new_name: str):
    note_win_test = set_note_win_test(note_window, name, tags, content, date_changing)
    note_win_test.test_renaming(new_name)


if __name__ == '__main__':
    pass
