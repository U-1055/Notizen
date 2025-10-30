from PySide6.QtWidgets import QWidget, QMenu, QHBoxLayout
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal

from src.gui.ui_tags_widget import Ui_Form as UiTagWidget
from src.gui.ui_tag_card import Ui_Form as UiTagCard


class TagWidget(QWidget):

    def __init__(self, menu: QMenu = None):
        super().__init__()
        self._view = UiTagWidget()
        self._view.setupUi(self)
        self._view.btn_add_tag.clicked.connect(self._open_tags_window)

        self._tags: set[str] = set()
        self._tag_menu: QMenu = menu
        if self._tag_menu:
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

            if self._tag_menu:
                self._tag_menu.removeAction(action)
                if len(self._tag_menu.actions()) == 0:
                    self._tag_menu.addAction(QAction('', self))

    def _delete_tag(self, tag: str):
        self._tags.remove(tag)

        action = QAction(tag, self)
        action.triggered.connect(lambda: self._add_tag(action))
        if self._tag_menu:
            self._tag_menu.addAction(action)

    def _clear_widget(self):
        for wdg_tag in self._view.frm_tags.children():
            if isinstance(wdg_tag, TagCardWidget):
                wdg_tag: TagCardWidget
                wdg_tag.hide()

    def tags(self) -> tuple:
        return tuple(self._tags)

    def set_tag_menu(self, menu: QMenu):
        """Устанавливает меню для выбора тегов. (Меню должно содержать действия, соответствующие названиям тегов)."""

        self._tag_menu = menu
        menu_tags = []
        for action in self._tag_menu.actions():  # Привязка действий к слотам
            menu_tags.append(action.text())
            action.triggered.connect(lambda _, act=action: self._add_tag(act))

        for tag in self.tags():  # Удаление тегов, которых нет в меню
            if tag not in menu_tags:
                self._delete_tag(tag)

        self._view.btn_add_tag.setMenu(self._tag_menu)


class TagCardWidget(QWidget):
    deleted = Signal(str)

    def __init__(self, name: str = None):
        super().__init__()
        self._view = UiTagCard()
        self._view.setupUi(self)

        self._view.btn_tag_card.clicked.connect(self._on_delete)
        self._name: str = name
        if self._name:
            self._view.lbl_tag_card.setText(self._name)

    def _on_delete(self):
        self.hide()
        self.deleted.emit(self._name)

    def name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name
        self._view.lbl_tag_card.setText(self._name)


if __name__ == '__main__':

    from PySide6.QtWidgets import QApplication, QMainWindow

    app = QApplication()

    root = QMainWindow()
    menu = QMenu()
    actions = [QAction('tag#1', root), QAction('tag#2', root)]
    menu.addActions(actions)

    mlw = TagWidget()
    mlw.set_tag_menu(menu)

    mlw.show()

    app.exec()
