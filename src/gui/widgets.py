from PySide6.QtWidgets import QWidget, QMenu, QLabel, QMessageBox, QDialog
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction, QCloseEvent

import datetime
import typing as tp

from src.gui.ui_note_widget import Ui_Form
from src.gui.ui_note_window import Ui_Form as UiNoteWindow
from src.gui.ui_elements_window import Ui_Form as UiElementsWindow
from src.gui.ui_save_window import Ui_Form as UiSaveWindow


class NoteWindow(QWidget):
    tried_to_close = Signal()  # Сигнал закрытия окна, передаёт событие закрытия
    name_changed = Signal()  # Название изменено
    text_changed = Signal()  # Текст изменён
    tags_changed = Signal()  # Теги изменены
    btn_save_pressed = Signal()  # Нажата кнопка сохранения
    btn_delete_pressed = Signal()  # Нажата кнопка удаления заметки
    btn_return_pressed = Signal()  # Нажата кнопка "Назад"

    def __init__(self):
        super().__init__()
        self._view = UiNoteWindow()
        self._view.setupUi(self)

        self._view.btn_return.clicked.connect(self._on_btn_return_pressed)
        self._view.line_edit_name.textChanged.connect(self._on_name_changed)
        self._view.wdg_text.textChanged.connect(self._on_text_changed)
        self._view.wdg_tags.tag_deleted.connect(self._on_tags_changed)
        self._view.wdg_tags.tag_added.connect(self._on_tags_changed)
        self._view.btn_save.clicked.connect(self._on_btn_save_pressed)
        self._view.btn_info.clicked.connect(self._on_btn_info_pressed)

        self._name = self._content = self._date_changing = self._tags = None

    def _on_btn_return_pressed(self):
        self.btn_return_pressed.emit()

    def _on_btn_info_pressed(self):
        menu = self._view.btn_info.menu()
        if menu:
            self._view.btn_info.showMenu()
            menu.exec()

    def _on_btn_save_pressed(self):
        self.btn_save_pressed.emit()

    def _on_name_changed(self):
        self.name_changed.emit()

    def _on_text_changed(self):
        self.text_changed.emit()

    def _on_tags_changed(self):
        self.tags_changed.emit()

    def on_tried_to_close(self):
        self.tried_to_close.emit()

    def on_btn_delete_pressed(self):
        self.btn_delete_pressed.emit()

    def set_ops_menu(self, menu: QMenu):
        """
        Устанавливает меню операций.
        :param menu: меню.
        """
        self._view.btn_info.setMenu(menu)
        self._view.btn_info.menu()  # Иначе последующие вызовы menu() будут возвращать None ToDo: понять, почему

    def show_error(self, text: str):
        win_error = QMessageBox()
        win_error.setText(text)
        win_error.setWindowModality(Qt.WindowModality.ApplicationModal)

        win_error.exec()

    def show_save_message(self, text: str) -> 'WindowSave':
        win_save = WindowSave()
        win_save.setText(text)
        win_save.setWindowModality(Qt.WindowModality.ApplicationModal)

        win_save.exec()
        return win_save

    def get_tag_widget(self):
        return self._view.wdg_tags

    @property
    def name(self) -> str:
        return self._view.line_edit_name.text()

    @name.setter
    def name(self, name: str):
        self._view.line_edit_name.setText(name)

    @property
    def content(self) -> str:
        return self._view.wdg_text.toPlainText()

    @content.setter
    def content(self, content: str):
        self._view.wdg_text.setText(content)

    @property
    def date_changing(self) -> str:
        return self._date_changing

    @date_changing.setter
    def date_changing(self, date_changing: str | datetime.datetime):
        self._date_changing = str(date_changing)

    @property
    def tags(self) -> list[str]:
        return list(self._view.wdg_tags.tags())

    @tags.setter
    def tags(self, tags: list[str, ...]):
        self._view.wdg_tags.set_tags(tags)


class NoteView(QWidget):
    pressed = Signal(object)  # Сигнал нажатия на заметку. Передает экземпляр класса заметки(себя)

    def __init__(self):
        super().__init__()
        self._view = Ui_Form()
        self._view.setupUi(self)

        self._name: str = None
        self._content: str = None
        self._date_changing: str = None
        self._tags: list[str] = None
        self._context_menu: QMenu = None

    def setup_wdg_state(self):
        """Устанавливает надписи на виджете."""
        self._view.lbl_name.setText(self._name)
        self._view.txt_content.setText(self._content)
        self._view.lbl_date_changed.setText(self._date_changing)

    def show_menu(self):
        self._view.btn_ops.showMenu()
        self._context_menu.exec()

    def setMenu(self, menu: QMenu):
        self._context_menu = menu
        self._view.btn_ops.setMenu(self._context_menu)
        self._view.btn_ops.clicked.connect(self.show_menu)

    def mousePressEvent(self, event, /):
        self.pressed.emit(self)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name
        self.setup_wdg_state()

    @property
    def content(self) -> str:
        return self._content[0::]

    @content.setter
    def content(self, content: str):
        self._content = content
        self.setup_wdg_state()

    @property
    def date_changing(self) -> str:
        return self._date_changing

    @date_changing.setter
    def date_changing(self, date_changing: str | datetime.datetime):
        self._date_changing = str(date_changing)
        self.setup_wdg_state()

    @property
    def tags(self) -> list[str]:
        return self._tags

    @tags.setter
    def tags(self, tags: list[str, ...]):
        self._tags = tags
        self.setup_wdg_state()

    def add_tag(self, tag: str):
        self._tags.append(tag)


class WindowTagChoose(QWidget):
    tag_chosen = Signal(str)

    def __init__(self):
        super().__init__()


class MessageListWidget(QWidget):
    """Виджет для сообщений с множественным выбором элементов."""
    elements_chosen = Signal(tuple)

    def __init__(self):
        super().__init__()
        self._view = UiElementsWindow()
        self._view.setupUi(self)
        self._view.btn_accept.clicked.connect(self._prepare_elements_choose)

    def _prepare_elements_choose(self):
        self.elements_chosen.emit(tuple(item.text() for item in self._view.wdg_items.selectedItems()))
        self.hide()

    def set_elements(self, elements: tuple[str, ...] | list[str]):
        self._view.wdg_items.addItems(elements)

    def elements(self) -> tuple[str, ...]:
        return tuple(item.text() for item in self._view.wdg_items.selectedItems())

    def setSelectionMode(self, selection_mode):
        """Меняет selection mode у QListWidget."""
        self._view.wdg_items.setSelectionMode(selection_mode)

    def set_btn_text(self, text: str):
        self._view.btn_accept.setText(text)

    def set_title_text(self, text: str):
        self._view.lbl_title.setText(text)

    def selectAll(self):
        self._view.wdg_items.selectAll()


class WindowDamagedNotes(QWidget):
    notes_chosen = Signal(tuple[str, ...])
    reclaiming_cancelled = Signal()

    def __init__(self):
        super().__init__()
        self._notes: tuple[str, ...] = None

    def set_notes(self, notes: tuple[str, ...] | list[str]):
        self._notes = notes


class WindowSave(QDialog):
    btn_save_pressed = Signal()
    btn_discard_pressed = Signal()

    def __init__(self):
        super().__init__()
        self._view = UiSaveWindow()
        self._view.setupUi(self)
        self._view.btn_save.clicked.connect(self._on_btn_save_pressed)
        self._view.btn_discard.clicked.connect(self._on_btn_discard_pressed)

    def _on_btn_save_pressed(self):
        self.btn_save_pressed.emit()
        self.hide()

    def _on_btn_discard_pressed(self):
        self.hide()
        self.btn_discard_pressed.emit()

    def setText(self, text: str):
        self._view.label.setText(text)

    def text(self) -> str:
        return self._view.label.text()


if __name__ == '__main__':
    pass
