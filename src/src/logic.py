import datetime

from src.gui.view import MainWindow
from src.src.model import DataModel


class Logic:

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

            note_view.pressed.connect(lambda: print('Clicked!'))

class NoteWidgetHandler:

    def __init__(self, note_view):
        self._name: str = None
        self._content: str = None
        self._date_changing: str = None
        self._tags: list[str] = None


class NoteWindowHandler:
    pass
