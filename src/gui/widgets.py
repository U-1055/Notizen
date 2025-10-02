from PySide6.QtWidgets import QWidget

from ui_note_widget import Ui_Form


class NoteView(QWidget):

    def __init__(self):
        super().__init__()
        self._view = Ui_Form()
        self._view.setupUi(self)


if __name__ == '__main__':
    from view import setup_gui
    setup_gui()
    NoteView()
