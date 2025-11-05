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
    def __init__(self, notes: Path, notes_data: Path, common_data_path: Path, resources: Path,
                 data_struct: DataStructConst):
        pass


    @abstractmethod
    @property
    def notes(self) -> Path:
        """Возвращает путь к папке с заметками."""
        pass

    @abstractmethod
    @property
    def notes_data(self) -> Path:
        """Возвращает путь к базе данных."""
        pass

    @abstractmethod
    @property
    def resources(self) -> Path:
        """Возвращает путь к файлу ресурсов."""
        pass

    @abstractmethod
    @property
    def data_struct(self) -> DataStructConst:
        """Возвращает экземпляр класса набора констант DataStructConst."""
        pass

    @abstractmethod
    def validate_files(self) -> tuple[str, ...]:
        """Проверяет файлы на соответствие структуре (notes и DBB)."""
        pass

    @abstractmethod
    def reclaim_common_data(self, common_data: dict) -> dict:
        """Восстанавливает common_data при наличии повреждений."""
        pass

    @abstractmethod
    def reclaim_note(self, note: str):
        pass

    @abstractmethod
    def get_style(self, style: str) -> str:
        """
        Возвращает стиль QSS.
        :param style: путь к стилю
        """
        pass

    @abstractmethod
    def get_last_style(self) -> str:
        """Возвращает установленный пользователем стиль (из config.json)"""
        pass

    @abstractmethod
    def get_note_tags(self, note: str) -> tuple[str, ...]:
        pass

    @abstractmethod
    def get_tags(self) -> tuple[str, ...]:
        """Возвращает все теги."""
        pass

    @abstractmethod
    def get_notes_tags(self) -> tuple[str, ...]:
        """Возвращает теги, к которым прикреплены заметки."""
        pass

    @abstractmethod
    def get_note_content(self, note: str) -> str:
        pass

    @abstractmethod
    def get_note_date_changing(self, note: str) -> str:
        pass
    @abstractmethod
    def get_notes(self) -> tuple:
        """Возвращает список со всеми заметками"""
        pass

    @abstractmethod
    def set_note_date_changing(self, note: str, date_changing: str):
        pass

    @abstractmethod
    def set_note_tags(self, note: str, tags: list[str] | tuple[str, ...]):
        pass

    @abstractmethod
    def set_note_content(self, note: str, content: str):
        pass

    @abstractmethod
    def delete_note(self, note: str):
        pass

    @abstractmethod
    def change_note_name(self, note: str, name: str):
        """
        Изменяет название заметки.
        :param note: текущее название заметки.
        :param name: новое название.
        """
        pass

    @abstractmethod
    def add_tag(self, tag: str):
        pass

    @abstractmethod
    def delete_tag(self, tag: str):
        pass

    @abstractmethod
    def add_note(self, name: str, tags: list[str] | tuple[str, ...]):
        pass


class INoteWindow(ABC):
    pass


if __name__ == '__main__':
    model = IModel()
    model.get_tags()