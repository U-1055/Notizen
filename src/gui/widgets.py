from PySide6.QtWidgets import QWidget, QMenu
from PySide6.QtCore import Signal

import datetime

from src.gui.ui_note_widget import Ui_Form
from src.gui.ui_note_window import Ui_Form as UiNoteWindow


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


class WindowDamagedNotes(QWidget):
    notes_chosen = Signal(tuple[str, ...])
    reclaiming_cancelled = Signal()

    def __init__(self):
        super().__init__()
        self._notes: tuple[str, ...] = None

    def set_notes(self, notes: tuple[str, ...] | list[str]):
        self._notes = notes


if __name__ == '__main__':
    from view import setup_gui
    from PySide6.QtWidgets import QApplication, QMainWindow

    app = QApplication()
    root = QMainWindow()

    setup_gui(root, app)
    NoteView()
