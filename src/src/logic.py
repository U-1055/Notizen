import datetime

from src.gui.view import MainWindow
from src.gui.widgets import NoteView, NoteWindow
from src.src.model import DataModel
from src.base import GuiLabels, DataStructConst, GuiConst
from src.src.requests_module import Requester
from utils.utils import set_unique_note_name

import typing as tp

from PySide6.QtCore import Signal, QObject, Slot
from requests import request


class Logic:

    # Сигналы для тестов
    note_added_to_menu = Signal(NoteView)

    def __init__(
            self,
            model,
            view,
            server: str,
            requester: Requester,
            labels: GuiLabels = GuiLabels(),
            gui_const: GuiConst = GuiConst(),
            data_struct_const: DataStructConst = DataStructConst()
    ):
        self._model: DataModel = model
        self._view: MainWindow = view
        self._server = server
        self._labels: GuiLabels = labels
        self._gui_const: GuiConst = gui_const
        self._data_struct: DataStructConst = data_struct_const
        self._requester = requester
        self._user: dict = {}

        self._notes: list[str] = None
        self._tags: list[str] = None
        self._notes_struct: dict[str, list[str]] = {}

        current_style = self._model.get_last_style()  # Установка стиля
        self._view.set_style(self._model.get_style(current_style))

        self._view.btn_create_note_pressed.connect(self._on_btn_create_note_pressed)
        self._view.btn_tags_pressed.connect(self._on_btn_tags_pressed)
        self._view.btn_update_pressed.connect(self._on_btn_update_pressed)
        self._view.btn_search_pressed.connect(self._on_btn_search_pressed)
        self._view.btn_dark_theme_pressed.connect(self._on_btn_dark_theme_pressed)
        self._view.btn_light_theme_pressed.connect(self._on_btn_light_theme_pressed)

        win_auth = self._view.get_authorize_window()
        win_auth.btn_confirm_pressed.connect(lambda: self._authorize('username#1', '12345'))
        #self._authorize('username1', '12345')
        self._update_state()
        self._requester.add_note(1, 'note#2', [])

    def _authorize(self, login: str, password: str):
        user_id = self._requester.authorize(login, password)  # Токен авторизации? Как обозначить то, что пользователь уже авторизован?
        self._user = self._requester.get_user_data(user_id)

    def _on_btn_search_pressed(self):
        self._show_relevant_notes()

    def _on_btn_update_pressed(self):
        self._update_state()

    def _on_btn_create_note_pressed(self):
        self._create_new_note()

    def _on_btn_tags_pressed(self):
        wdg_tags_manage = self._view.show_tag_manage_widget()

        wdg_tags_manage.setWindowTitle(self._labels.title_tags_manage_widget)
        wdg_tags_manage.setBtnAddText(self._labels.add_tag)
        wdg_tags_manage.setBtnSaveText(self._labels.save)
        wdg_tags_manage.setBtnConfirmText(self._labels.confirm)

        wdg_tags_manage.set_tags(self._model.get_tags())
        wdg_tags_manage.btn_save_pressed.connect(lambda: self._change_tags(wdg_tags_manage.tags()))
        wdg_tags_manage.exec()

    def _on_btn_light_theme_pressed(self):
        self._view.set_style(self._model.get_style(self._data_struct.light_theme))

    def _on_btn_dark_theme_pressed(self):
        self._view.set_style(self._model.get_style(self._data_struct.dark_theme))

    def _change_tags(self, new_tags: tuple[str, ...]):
        """Изменяет теги: сравнивает полученные теги с текущими, меняет теги в базе и обновляет состояние."""

        current_tags = self._model.get_tags()
        for tag in new_tags:  # Добавление новых тегов
            if tag not in current_tags:
                self._model.add_tag(tag)

        for tag in current_tags:  # Удаление удалённых тегов
            if tag not in new_tags:
                self._model.delete_tag(tag)
        self._update_state()

    def _create_new_note(self):

        name = set_unique_note_name(self._labels.base_note_name, self._notes)
        self._model.add_note(name, [])

        note_window = self._view.open_note_window()
        note_window = self._set_note_window(note_window, name, [], datetime.date.today().strftime(self._data_struct.datetime_date_format))

        note_handler = NoteWindowHandler(name, note_window, self._model, self._labels, DataStructConst())
        note_handler.closed.connect(self._close_note)

    def _reclaim_damaged_notes(self, damaged_notes: tuple[str, ...]):
        for note in damaged_notes:
            self._model.reclaim_note(note)
        self._view.show_message(self._labels.notes_reclaimed, ''.join(damaged_notes))
        self._update_state()

    def _show_relevant_notes(self):
        search_text = self._view.search_text()

        if search_text == '':  # Если текста нет - поиск не происходит
            return

        tags = self._view.get_tag_widget().tags()
        if search_text:
            name_relevant_notes = list(filter(lambda note: search_text in note, self._notes))
        if tags:
            tags_relevant_notes = list(filter(lambda note: any(tag in tags for tag in self._model.get_note_tags(note)), self._notes))  # Находим заметки с подходящими тегами

        relevant_notes = []
        if search_text and tags:
            relevant_notes = list(filter(lambda note: note in tags_relevant_notes, name_relevant_notes))
        elif search_text:
            relevant_notes = name_relevant_notes
        elif tags:
            relevant_notes = tags_relevant_notes

        self._init_menu(relevant_notes)

    def _update_state(self):
        damaged_notes = self._model.validate_files()

        self._notes = list(filter(lambda note: note not in damaged_notes, self._model.get_notes()))
        self._notes_struct: dict[str, list[str]] = {}

        tag_menu = self._view.get_menu(tuple((str(tag), lambda: None) for tag in self._model.get_tags()))  # Настройка виджета тегов
        tag_widget = self._view.get_tag_widget()
        tag_widget.set_tag_menu(tag_menu)

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

        if self._view.search_text() or self._view.get_tag_widget().tags():
            self._show_relevant_notes()
        else:
            self._init_menu(self._notes)

    def _init_menu(self, notes: tuple[str, ...] | list[str]):
        self._view.clear_notes()
        if len(notes) == 0:
            self._view.show_no_found_label(self._labels.no_found)

        for note in notes:

            note_view = self._view.add_note()

            note_view.name = note
            content = self._model.get_note_content(note)
            if len(content) > self._gui_const.max_text_view_length:
                content = f'{content[0:self._gui_const.max_text_view_length]}...'
            note_view.content = content
            note_view.date_changing = self._model.get_note_date_changing(note)
            note_view.tags = self._model.get_note_tags(note)

            note_view.setMenu(self._view.get_menu(((self._labels.delete, note_view.press_btn_delete),)))
            note_view.btn_delete_pressed.connect(self._delete_note)

            note_view.pressed.connect(lambda note=note_view: self._open_note(note))

    def _open_note(self, note_view: NoteView):
        """Обрабатывает открытие заметки."""
        note_window = self._view.open_note_window()

        self._set_note_window(note_window, note_view.name, note_view.tags, note_view.date_changing)

        note_handler = NoteWindowHandler(note_view.name, note_window, self._model, self._labels, DataStructConst())
        note_handler.closed.connect(self._close_note)

    def _set_note_window(self,
                         note_window: NoteWindow,
                         name: str,
                         tags: list[str] | tuple[str, ...],
                         date_changing: str
                         ) -> NoteWindow:
        wdg_tags = note_window.get_tag_widget()
        wdg_tags.set_tag_menu(self._view.get_menu(tuple((str(tag), lambda: None) for tag in self._model.get_tags())))

        note_window.tags = tags
        note_window.name = name
        note_window.date_changing = date_changing
        note_window.content = self._model.get_note_content(name)

        menu = self._view.get_menu(
            (
                (self._labels.delete, note_window.on_btn_delete_pressed),
            )
        )
        note_window.set_ops_menu(menu)
        self._view.tried_to_close.connect(note_window.on_tried_to_close)

        return note_window

    def _close_note(self):
        self._view.open_main_menu()
        self._update_state()

    def _delete_note(self, note_view: NoteView):
        self._model.delete_note(note_view.name)
        self._notes.pop(self._notes.index(note_view.name))
        note_view.hide()


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

        self._note_window.tried_to_close.connect(lambda: self._on_close())
        self._note_window.btn_return_pressed.connect(lambda: self._on_close())
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
            except ValueError:  # Если название неуникально
                self._note_window.show_error(f'{self._note_window.name} - {self._labels.name_is_not_unique_error}')

        self._model.set_note_tags(self._name, self._note_window.tags)
        self._model.set_note_content(self._name, self._note_window.content)
        self._model.set_note_date_changing(self._name, str(datetime.date.today().strftime(self._data_struct.datetime_date_format)))

        self._name_changed = False
        self._note_changed = False

    def _save(self):
        self._save_note()
        self._close_window()

    def _discard(self):
        self._name_changed = False
        self._note_changed = False
        self._close_window()

    def _on_close(self):
        if self._note_changed:
            self._note_window.show_save_message(self._labels.save_message, self._save, self._close_window)
        else:
            self._close_window()

    def _on_deleted(self):
        self._model.delete_note(self._name)
        self._close_window()

    def _on_name_changed(self):
        self._name_changed = True
        self._note_changed = True

    def _on_change(self):
        self._note_changed = True

    def _close_window(self):
        self.closed.emit()


if __name__ == '__main__':
    pass
