import datetime

from src.gui.view import MainWindow
from src.gui.widgets import NoteView, NoteWindow
from src.src.model import DataModel

from PySide6.QtCore import Signal, QObject


class Logic:

    # Сигналы для тестов
    note_added_to_menu = Signal(NoteView)

    def __init__(self, model, view):
        self._model: DataModel = model
        self._view: MainWindow = view

        self._notes: list[str] = None
        self._tags: list[str] = None
        self._search_text: str = None

        self._notes_struct: dict[str, list[str]] = {}
        self._update_state()
        self._init_menu()

    def _update_state(self):
        self._notes = self._model.get_notes()
        self._tags = self._view.get_selected_tags()
        self._search_text = self._view.text_search()

        notes_tags = self._model.get_tags()

        if notes_tags:
            for tag in notes_tags:  # Инициализация notes_struct
                self._notes_struct[tag] = []

        for note in self._notes:  # Добавление заметки в списки по её тегам
            tags = self._model.get_note_tags(note)
            if tags:
                for tag in tags:
                    self._notes_struct[tag].append(note)

    def _init_menu(self):

        for note in self._notes:
            note_view = self._view.add_note()

            note_view.name = note
            note_view.content = self._model.get_note_content(note)
            note_view.date_changing = self._model.get_note_date_changing(note)
            note_view.tags = self._model.get_note_tags(note)

            note_view.pressed.connect(lambda note=note_view: self._open_note(note))

    def _open_note(self, note_view: NoteView):
        """Обрабатывает открытие заметки."""
        note_window = self._view.open_note_window()
        self.note_handler = NoteWindowHandler(note_window)

        note_window.tags = note_view.tags
        note_window.name = note_view.name
        note_window.date_changing = note_view.date_changing
        note_window.content = note_view.content

        self.note_handler.closed.connect(self._close_note)

    def _close_note(self):
        self._view.open_main_menu()


class NoteWidgetHandler:

    def __init__(self, note_view):
        self._name: str = None
        self._content: str = None
        self._date_changing: str = None
        self._tags: list[str] = None


class NoteWindowHandler(QObject):
    closed = Signal()  # Handler сам обрабатывает сигналы от NoteWindow

    def __init__(self, note_window: NoteWindow):
        super().__init__()
        self._note_window = note_window
        self._note_window.closed.connect(self.closed.emit)

    def _close_window(self):
        self.closed.emit()
        self._note_window.close_window()

