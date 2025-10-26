from PySide6.QtWidgets import QWidget, QMenu, QListWidgetItem
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction

import datetime

from src.gui.ui_note_widget import Ui_Form
from src.gui.ui_note_window import Ui_Form as UiNoteWindow
from src.gui.ui_tags_widget import Ui_Form as UiTagWidget
from src.gui.ui_tag_card import Ui_Form as UiTagCard
from src.gui.ui_elements_window import Ui_Form as UiElementsWindow


class NoteWindow(QWidget):
    closed = Signal()  # Сигнал закрытия окна

    def __init__(self):
        super().__init__()
        self._view = UiNoteWindow()
        self._view.setupUi(self)
        self._view.btn_return.clicked.connect(self.closed.emit)

        self._name = self._content = self._date_changing = self._tags = None

    def close_window(self):
        pass

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def content(self) -> str:
        return self._content[0::]

    @content.setter
    def content(self, content: str):
        self._content = content

    @property
    def date_changing(self) -> str:
        return self._date_changing

    @date_changing.setter
    def date_changing(self, date_changing: str | datetime.datetime):
        self._date_changing = str(date_changing)

    @property
    def tags(self) -> list[str]:
        return self._tags

    @tags.setter
    def tags(self, tags: list[str, ...]):
        self._tags = tags


class NoteView(QWidget):
    pressed = Signal(object)  # Сигнал нажатия на заметку. Передает экземпляр класса заметки(себя)
    # ToDo: как описать тип в сигнале вместо object

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


class WindowDamagedNotes(QWidget):
    notes_chosen = Signal(tuple[str, ...])
    reclaiming_cancelled = Signal()

    def __init__(self):
        super().__init__()
        self._notes: tuple[str, ...] = None

    def set_notes(self, notes: tuple[str, ...] | list[str]):
        self._notes = notes


class TagCardWidget(QWidget):
    deleted = Signal(str)

    def __init__(self, name: str = None):
        super().__init__()
        self._view = UiTagCard()
        self._view.setupUi(self)

        self._name: str = name
        if self._name:
            self._view.lbl_tag_card.setText(self._name)

    def name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name
        self._view.lbl_tag_card.setText(self._name)


class TagWidget(QWidget):

    def __init__(self, menu: QMenu):
        super().__init__()
        self._view = UiTagWidget()
        self._view.setupUi(self)
        self._view.btn_add_tag.clicked.connect(self._open_tags_window)

        self._tags: set[str] = set()
        self._tag_menu: QMenu = menu
        self.set_tag_menu(menu)

    def _open_tags_window(self):
        if self._tag_menu:
            self._view.btn_add_tag.showMenu()
            self._tag_menu.exec()

    def _add_tag(self, action: QAction):
        tag = action.text()
        if tag not in self._tags:
            self._tags.add(tag)
            wdg_tag = TagCardWidget(tag)
            wdg_tag.deleted.connect(self._delete_tag)

            self._view.frm_tags.addWidget(wdg_tag)
            self._tag_menu.removeAction(action)
            if len(self._tag_menu.actions()) == 0:
                self._tag_menu.addAction(QAction('', self))

    def _delete_tag(self, tag: str):
        self._tags.remove(tag)
        action = QAction(tag, self)
        action.triggered.connect(lambda: self._add_tag(action))
        self._tag_menu.addAction(action)


    def _clear_widget(self):
        for wdg_tag in self._view.frm_tags.children():
            if isinstance(wdg_tag, TagCardWidget):
                wdg_tag: TagCardWidget
                wdg_tag.hide()

    def set_tags(self, tags: tuple[str, ...] | list[str]):
        self._tags = set(tags)
        self._clear_widget()
        for tag in self._tags:
            wdg_tag = TagCardWidget(tag)
            self._view.frm_tags.addWidget(wdg_tag)

    def tags(self) -> tuple:
        tags = set()
        for wdg_tag in self._view.frm_tags.children():
            if isinstance(wdg_tag, TagCardWidget):
                tags.add(wdg_tag.name())

        return tuple(tags)

    def set_tag_menu(self, menu: QMenu):
        """Устанавливает меню для выбора тегов. (Меню должно содержать действия, соответствующие названиям тегов)."""

        self._tag_menu = menu
        for action in self._tag_menu.actions():  # Привязка действий к слотам
            action.triggered.connect(lambda _, act=action: self._add_tag(act))

        self._view.btn_add_tag.setMenu(self._tag_menu)


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication, QMainWindow

    app = QApplication()

    root = QMainWindow()
    menu = QMenu()
    actions = [QAction('tag#1', root), QAction('tag#2', root)]
    menu.addActions(actions)

    mlw = TagWidget(menu)

    root.setCentralWidget(mlw)
    root.show()

    app.exec()
