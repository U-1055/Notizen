import datetime

from src.gui.view import MainWindow
from src.gui.widgets import NoteView, NoteWindow
from src.src.model import DataModel
from src.base import GuiLabels, DataStructConst, GuiConst

from PySide6.QtCore import Signal, QObject


class Logic:

    # Сигналы для тестов
    note_added_to_menu = Signal(NoteView)

    def __init__(self, model, view, labels: GuiLabels, gui_const: GuiConst):
        self._model: DataModel = model
        self._view: MainWindow = view
        self._labels: GuiLabels = labels
        self._gui_const: GuiConst = gui_const

        self._notes: list[str] = None
        self._tags: list[str] = None
        self._search_text: str = None
        self._notes_struct: dict[str, list[str]] = {}

        current_style = self._model.get_last_style()  # Установка стиля
        self._view.set_style(self._model.get_style(current_style))

        self._update_state()
        tag_menu = self._view.get_menu(tuple((str(tag), lambda: None) for tag in self._model.get_tags()))
        self._tag_widget = self._view.get_tag_widget()
        self._tag_widget.set_tag_menu(tag_menu)

    def _reclaim_damaged_notes(self, damaged_notes: tuple[str, ...]):
        for note in damaged_notes:
            self._model.reclaim_note(note)
        self._view.show_message(self._labels.notes_reclaimed, ''.join(damaged_notes))
        self._update_state()

    def _update_state(self):
        damaged_notes = self._model.validate_files()

        self._notes = list(filter(lambda note: note not in damaged_notes, self._model.get_notes()))
        self._tags = self._view.get_selected_tags()
        self._search_text = self._view.text_search()
        self._notes_struct: dict[str, list[str]] = {}

        notes_tags = self._model.get_tags()

        if notes_tags:
            for tag in notes_tags:  # Инициализация notes_struct
                self._notes_struct[tag] = []

        for note in self._notes:  # Добавление заметки в списки по её тегам
            tags = self._model.get_note_tags(note)
            if tags:
                for tag in tags:
                    self._notes_struct[tag].append(note)

        if damaged_notes:  # Если есть повреждённые заметки
            win_damaged_notes = self._view.open_damaged_notes_window()
            win_damaged_notes.set_elements(damaged_notes)
            win_damaged_notes.elements_chosen.connect(self._reclaim_damaged_notes)
        self._init_menu(self._notes)

    def _init_menu(self, notes: tuple[str, ...] | list[str]):
        self._view.clear_notes()

        for note in notes:

            note_view = self._view.add_note()

            note_view.name = note
            content = self._model.get_note_content(note)
            if len(content) > self._gui_const.max_text_view_length:
                content = f'{content[0:self._gui_const.max_text_view_length]}...'
            note_view.content = content
            note_view.date_changing = self._model.get_note_date_changing(note)
            note_view.tags = self._model.get_note_tags(note)

            note_view.setMenu(self._view.get_menu(((self._labels.delete, lambda _, name=note_view.name: self._delete_note(name)),)))

            note_view.pressed.connect(lambda note=note_view: self._open_note(note))

    def _open_note(self, note_view: NoteView):
        """Обрабатывает открытие заметки."""
        note_window = self._view.open_note_window()

        wdg_tags = note_window.get_tag_widget()
        wdg_tags.set_tag_menu(self._view.get_menu(tuple((str(tag), lambda: None) for tag in self._model.get_tags())))

        note_window.tags = note_view.tags
        note_window.name = note_view.name
        note_window.date_changing = note_view.date_changing
        note_window.content = self._model.get_note_content(note_view.name)

        menu = self._view.get_menu(
            (
                (self._labels.delete, note_window.on_btn_delete_pressed),
            )
        )
        note_window.set_ops_menu(menu)
        self._view.tried_to_close.connect(note_window.on_tried_to_close)

        self.note_handler = NoteWindowHandler(note_view.name, note_window, self._model, self._labels, DataStructConst())
        self.note_handler.closed.connect(lambda: self._close_note(note_view))

    def _close_note(self, note_view: NoteView):
        self._view.open_main_menu()
        self._update_state()

    def _delete_note(self, note: str):
        pass


class NoteWindowHandler(QObject):
    closed = Signal()  # Handler сам обрабатывает сигналы от NoteWindow

    def __init__(self, name: str, note_window: NoteWindow, model: DataModel, labels: GuiLabels, data_struct_const: DataStructConst):
        super().__init__()
        self._model = model
        self._labels = labels
        self._data_struct = data_struct_const
        self._name = name
        self._name_changed = False
        self._note_changed = False

        self._note_window = note_window

        self._note_window.tried_to_close.connect(self._on_tried_to_close)
        self._note_window.btn_return_pressed.connect(self._on_btn_return_pressed)
        self._note_window.name_changed.connect(self._on_name_changed)
        self._note_window.tags_changed.connect(self._on_change)
        self._note_window.text_changed.connect(self._on_change)
        self._note_window.btn_save_pressed.connect(self._save_note)
        self._note_window.btn_delete_pressed.connect(self._on_deleted)

    def _save_note(self):

        if not self._note_changed:  # Если заметка не изменена
            return

        if self._name_changed:
            try:
                self._model.change_note_name(self._name, self._note_window.name)
                self._name = self._note_window.name
            except ValueError as error:  # Если название неуникально
                raise error

        self._model.set_note_tags(self._name, self._note_window.tags)
        self._model.set_note_content(self._name, self._note_window.content)
        self._model.set_note_date_changing(self._name, str(datetime.date.today().strftime(self._data_struct.datetime_date_format)))

        self._name_changed = False
        self._note_changed = False

    def _on_tried_to_close(self):
        if self._note_changed:
            self._on_closed()


    def _on_btn_return_pressed(self):
        if self._note_changed:
            self._on_closed()
        self.closed.emit()

    def _on_closed(self):

        win_save = self._note_window.show_save_message(self._labels.save_message)
        win_save.btn_save_pressed.connect(self._save_note)

        try:
            self._save_note()
            self.closed.emit()
        except ValueError:  # Новое название заметки неуникально
            self._note_window.show_error(f'{self._note_window.name} - {self._labels.name_is_not_unique_error}')


    def _on_deleted(self):
        self._model.delete_note(self._name)
        self.closed.emit()

    def _on_name_changed(self):
        self._name_changed = True
        self._note_changed = True

    def _on_change(self):
        self._note_changed = True

    def _close_window(self):
        self.closed.emit()


if __name__ == '__main__':
    pass
