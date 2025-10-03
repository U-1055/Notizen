from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

import datetime

from src.gui.ui_note_widget import Ui_Form


class NoteWindow(QWidget):

    def __init__(self):
        super().__init__()

class NoteView(QWidget):
    pressed = Signal()

    def __init__(self):
        super().__init__()
        self._view = Ui_Form()
        self._view.setupUi(self)

        self._name: str = None
        self._content: str = None
        self._date_changing: str = None
        self._tags: list[str] = None

    def setup_wdg_state(self):
        """Устанавливает надписи на виджете."""
        self._view.lbl_name.setText(self._name)
        self._view.txt_content.setText(self._content)
        self._view.lbl_date_changed.setText(self._date_changing)

    def mousePressEvent(self, event, /):
        self.pressed.emit()

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
        self.tags = 0
        return self._tags

    @tags.setter
    def tags(self, tags: list[str, ...]):
        self._tags = tags
        self.setup_wdg_state()

    def add_tag(self, tag: str):
        self._tags.append(tag)


if __name__ == '__main__':
    from view import setup_gui
    from PySide6.QtWidgets import QApplication, QMainWindow

    app = QApplication()
    root = QMainWindow()

    setup_gui(root, app)
    NoteView()
