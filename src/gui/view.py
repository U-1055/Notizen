from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Signal

from src.interfaces import View
from src.gui.ui_view import Ui_MainWindow
from src.gui.widgets import NoteView


class MainWindow(QMainWindow):
    btn_create_note_pressed = Signal()
    btn_tags_pressed = Signal()
    btn_change_theme_pressed = Signal()
    btn_add_tag_pressed = Signal()

    def __init__(self):
        super().__init__()
        self._view = Ui_MainWindow()
        self._view.setupUi(self)
        self._last_row = 0
        self._last_column = 0

    def set_style(self, style: str):
        self.setStyleSheet(style)

    def add_note(self):
        note_widget = NoteView()
        if self._last_column == 1:
            self._last_column = 0
            self._last_row += 1
        else:
            self._last_column += 1

        self._view.layout_notes.addWidget(note_widget, self._last_row, self._last_column)

        return note_widget

    def open_note(self):
        pass

    def get_selected_tags(self) -> tuple[str]:
        pass

    def text_search(self) -> str:
        return self._view.line_edit_search.text()

    def _setup_widgets(self):
        pass


def setup_gui(root, app):

    screen = root.screen()

    screen_width = screen.geometry().width()
    screen_height = screen.geometry().height()

    root_width = int(screen_width * 0.5)
    root_height = int(screen_height * 0.6)
    padx = (screen_width - root_width) // 2
    pady = (screen_height - root_height) // 2

    root.setGeometry(padx, pady, root_width, root_height)
    root.show()

    app.exec()


if __name__ == '__main__':
    app_ = QApplication()
    root_ = MainWindow()
    setup_gui(root_, app_)
