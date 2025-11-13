from PySide6.QtWidgets import QWidget, QMenu, QLabel, QMessageBox, QDialog, QLineEdit, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction, QCloseEvent

import datetime
import typing as tp

from src.gui.ui_note_widget import Ui_Form
from src.gui.ui_note_window import Ui_Form as UiNoteWindow
from src.gui.ui_elements_window import Ui_Form as UiElementsWindow
from src.gui.ui_save_window import Ui_Form as UiSaveWindow
from src.gui.ui_tags_manage_widget import Ui_Form as UiTagManageWidget
from src.gui.tags_widget import TagCardWidget
from src.base import GuiLabels


class NoteWindow(QWidget):
    """
    Окно заметки.
    :var name: название заметки.
    :var content: содержимое заметки.
    :var tags: теги заметки.
    :var date_changing: дата изменения заметки.
    """

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

        self._date_changing = None

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

    def show_save_message(self, text: str, save_func: tp.Callable, discard_func: tp.Callable):
        win_save = WindowSave()
        win_save.setText(text)
        win_save.setWindowModality(Qt.WindowModality.ApplicationModal)
        win_save.btn_save_pressed.connect(save_func)
        win_save.btn_discard_pressed.connect(discard_func)

        win_save.exec()


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
    """Виджет заметки."""

    pressed = Signal(object)  # Сигнал нажатия на заметку. Передает экземпляр класса заметки(себя)
    btn_delete_pressed = Signal(object)  # Нажата кнопка удаления. Передает себя

    def __init__(self):
        super().__init__()
        self._view = Ui_Form()
        self._view.setupUi(self)

        self._name: str = None
        self._content: str = None
        self._date_changing: str = None
        self._tags: list[str] = None
        self._context_menu: QMenu = None

    def press_btn_delete(self):
        self.btn_delete_pressed.emit(self)

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


class MessageListWidget(QWidget):
    """Виджет для сообщений с множественным выбором элементов"""
    elements_chosen = Signal(tuple)  # Элементы выбраны

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
    """Окно подтверждения выхода при несохранённых данных."""

    btn_save_pressed = Signal()  # Нажата кнопка сохранения
    btn_discard_pressed = Signal()  # Нажата кнопка выхода

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

    def setSaveText(self, text: str):
        self._view.btn_save.setText(text)

    def saveText(self) -> str:
        return self._view.btn_save.text()

    def setDiscardText(self, text: str):
        self._view.btn_discard.setText(text)

    def discardText(self) -> str:
        return self._view.btn_discard.text()

    def setText(self, text: str):
        self._view.label.setText(text)

    def text(self) -> str:
        return self._view.label.text()


class LineEditBtn(QWidget):
    """QLineEdit с кнопкой QPushButton."""

    editingFinished = Signal()
    textChanged = Signal(str)
    textEdited = Signal(str)
    clicked = Signal(bool)

    def __init__(self, text: str = None):
        super().__init__()
        self._main_layout = QHBoxLayout()
        self._line_edit = QLineEdit(text)
        self._btn = QPushButton()

        self._btn.clicked.connect(lambda state: self.clicked.emit(state))
        self._line_edit.editingFinished.connect(self.editingFinished)
        self._line_edit.textChanged.connect(self.textChanged)
        self._line_edit.textEdited.connect(self.textEdited)

        self._main_layout.addWidget(self._line_edit)
        self._main_layout.addWidget(self._btn)
        self.setLayout(self._main_layout)

    def text(self) -> str:
        return self._line_edit.text()

    def setText(self, text: str):
        self._line_edit.setText(text)

    def btnText(self) -> str:
        return self._btn.text()

    def setBtnText(self, text: str):
        self._btn.setText(text)


class TagManageWindget(QDialog):
    """
    Виджет управления тегами.
    :var _labels: константы GuiLabels.
    :var _tags: теги, размещённые в виджете.
    :var _line_edit_new_tag: виджет ввода нового тега.
    :var _line_edit_btn_text: текст кнопки виджета ввода.
    """

    tag_added = Signal(str)  # Тег добавлен
    tag_deleted = Signal(str)  # Тег удален
    btn_save_pressed = Signal()  # Нажата кнопка сохранения, передаёт текущие теги в виджете

    def __init__(self, labels: GuiLabels):
        super().__init__()
        self._view = UiTagManageWidget()
        self._view.setupUi(self)
        self._view.btn_add_tag.clicked.connect(self._on_btn_add_tag_pressed)
        self._view.btn_save.clicked.connect(self.press_btn_save)
        self._view.btn_save.setFocus()

        self._labels = labels
        self._tags: set = set()
        self._line_edit_new_tag: LineEditBtn | None = None
        self._line_edit_btn_text: str | None = None

    def _on_btn_add_tag_pressed(self):
        self._view.btn_add_tag.setDisabled(True)
        self._line_edit_new_tag = LineEditBtn('')
        self._view.frm_tags.addWidget(self._line_edit_new_tag)
        self._line_edit_new_tag.setBtnText(self._line_edit_btn_text)
        self._line_edit_new_tag.clicked.connect(lambda: self.add_tag(self._line_edit_new_tag.text()))

    def _prepare_tag_exists(self):
        win_dialog = QMessageBox()
        win_dialog.setText(self._labels.tag_exists_message)
        win_dialog.setWindowTitle(self._labels.title_win_message)
        win_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)

        win_dialog.exec()

    def _clear_widget(self):
        """Очищает виджет."""
        self._tags = set()
        for idx in range(self._view.frm_tags.count()):
            self._view.frm_tags.itemAt(idx).widget().hide()

    def _place_tag_widget(self, tag: str):
        """Размещает виджет тега."""
        if self._line_edit_new_tag:
            self._line_edit_new_tag.hide()
            self._line_edit_new_tag = None
        wdg_tag = TagCardWidget(tag)
        wdg_tag.deleted.connect(self.delete_tag)
        self._view.frm_tags.addWidget(wdg_tag)

    def _delete_tag_widget(self, tag: str):
        """Удаляет виджет тега."""
        for idx in range(self._view.frm_tags.count()):
            widget: TagCardWidget = self._view.frm_tags.itemAt().widget()
            if widget.name == tag:
                widget.hide()

    def press_btn_save(self):
        self.btn_save_pressed.emit()
        self.hide()

    def tags(self) -> tuple[str, ...]:
        return tuple(self._tags)

    def set_tags(self, tags: list[str] | tuple[str, ...] | set[str]):
        """Устанавливает теги."""
        self._tags = set(tags)
        for tag in self._tags:
            self._place_tag_widget(tag)

    def setBtnSaveText(self, text: str):
        self._view.btn_save.setText(text)

    def btnSaveText(self) -> str:
        return self._view.btn_save.text()

    def setBtnConfirmText(self, text: str):  # Текст кнопки на виджете ввода тега (LineEditBtn)
        self._line_edit_btn_text = text

    def btnConfirmText(self) -> str | None:
        return self._line_edit_btn_text

    def setBtnAddText(self, text: str):
        self._view.btn_add_tag.setText(text)

    def btnAddText(self) -> str:
        return self._view.btn_add_tag.text()

    def add_tag(self, tag: str):
        """Добавляет тег. Испускает сигнал tag_added."""
        if tag in self._tags:
            self._prepare_tag_exists()
            return

        self._tags.add(tag)
        self._place_tag_widget(tag)
        self._view.btn_add_tag.setEnabled(True)
        self.tag_added.emit(tag)

    def delete_tag(self, tag: str):
        """Удаляет тег. Испускает сигнал tag_deleted."""
        if tag in self._tags:
            self._tags.remove(tag)
            self.tag_deleted.emit(tag)


class AuthorizeWindow(QWidget):
    btn_confirm_pressed = Signal(str, str)

    def __init__(self):
        super().__init__()

    @property
    def password(self) -> str:
        return ''

    @property
    def login(self) -> str:
        return ''


if __name__ == '__main__':
    pass
