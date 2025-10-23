from PySide6.QtCore import Signal

from abc import abstractmethod, ABC
from pathlib import Path

from src.gui.widgets import NoteWindow


class IView(ABC):
    btn_create_note_pressed = Signal()
    btn_tags_pressed = Signal()
    btn_change_theme_pressed = Signal()
    btn_add_tag_pressed = Signal()

    @abstractmethod
    def open_main_menu(self):
        pass

    @abstractmethod
    def set_style(self, style: str):
        pass

    @abstractmethod
    def add_note(self):
        pass

    @abstractmethod
    def open_note_window(self) -> str:
        pass

    @abstractmethod
    def get_selected_tags(self) -> tuple[str]:
        pass

    @abstractmethod
    def text_search(self) -> str:
        pass


class IModel(ABC):

    @abstractmethod
    def get_note_data(self, note: str):
        pass

    @abstractmethod
    def get_note_tags(self, note: str) -> str:
        pass

    @abstractmethod
    def get_tags(self) -> tuple[str, ...]:
        pass

    @abstractmethod
    def get_note_content(self, note: str):
        pass

    @abstractmethod
    def get_note_date_changing(self, note: str):
        pass

    def get_notes(self) -> tuple:
        """Возвращает список со всеми заметками"""
        pass


class INoteWindow(ABC):
    pass


if __name__ == '__main__':
    model = IModel()
    model.get_tags()