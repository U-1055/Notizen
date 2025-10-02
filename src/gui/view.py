from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from src.interfaces import View
from src.gui.ui_view import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self._view = Ui_MainWindow()
        self._view.setupUi(self)

    def set_style(self, style: str):
        self.setStyleSheet(style)

    def open_note(self):
        pass

    def _setup_widgets(self):
        pass


def setup_gui():
    app = QApplication()
    root = MainWindow()

    screen = root.screen()

    screen_width = screen.geometry().width()
    screen_height = screen.geometry().height()

    root_width = int(screen_width * 0.7)
    root_height = int(screen_height * 0.6)
    padx = (screen_width - root_width) // 2
    pady = (screen_height - root_height) // 2

    root.setGeometry(padx, pady, root_width, root_height)
    root.show()
    root.set_style('')
    app.exec()


if __name__ == '__main__':
    setup_gui()
