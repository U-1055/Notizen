from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QMenu, QSizePolicy
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal

import typing as tp

from src.interfaces import IView
from src.gui.ui_view import Ui_Form
from src.gui.widgets import NoteView, NoteWindow, WindowDamagedNotes
from src.base import GuiLabels


class MainWindow(QMainWindow):

    btn_create_note_pressed = Signal()
    btn_tags_pressed = Signal()
    btn_change_theme_pressed = Signal()
    btn_add_tag_pressed = Signal()

    def __init__(self, labels=None):
        super().__init__()
        self._main_widget = QStackedWidget()
        self.setCentralWidget(self._main_widget)

        container = QWidget()
        self._view = Ui_Form()
        self._view.setupUi(container)
        self._main_widget.insertWidget(0, container)
        self._main_widget.setCurrentIndex(0)

        self._labels = labels

        if self._labels:
            self._view.btn_theme_dark_2.setText(self._labels.set_theme_dark)
            self._view.btn_theme_light_2.setText(self._labels.set_theme_light)
            self._view.btn_create_note_2.setText(self._labels.create_note)
            self._view.btn_tags_2.setText(self._labels.view_tags)

        self._last_row, self._last_column = 0, 0
        self.open_main_menu()

    def open_main_menu(self):

        self._main_widget.setCurrentIndex(0)

        if self._labels:
            self._view.btn_theme_dark_2.setText(self._labels.set_theme_dark)
            self._view.btn_theme_light_2.setText(self._labels.set_theme_light)
            self._view.btn_create_note_2.setText(self._labels.create_note)
            self._view.btn_tags_2.setText(self._labels.view_tags)

    def set_style(self, style: str):
        self.setStyleSheet(style)

    def add_note(self):
        note_widget = NoteView()
        self._view.frm_notes.addWidget(note_widget, self._last_row, self._last_column)

        if self._last_column == 1:
            self._last_column = 0
            self._last_row += 1
        else:
            self._last_column += 1

        return note_widget

    def open_note_window(self) -> NoteWindow:
        note_window = NoteWindow()
        self._main_widget.insertWidget(1, note_window)
        self._main_widget.setCurrentIndex(1)

        return note_window

    def get_menu(self, elements: tuple[tuple[str, tp.Callable], ...]) -> QMenu:
        """
        Создаёт меню.
        :param elements: кортеж элементов вида ((Название пункта, Функция, выполняемая при нажатии на пункт), (...))
        """
        menu = QMenu()

        actions = [QAction(el[0], self) for el in elements]
        [action.triggered.connect(elements[idx][1]) for idx, action in enumerate(actions)]  # Привязка слотов к действиям

        menu.addActions([QAction(el[0], self) for el in elements])  # Добавление действий в меню

        return menu

    def show_message(self, title: str, message: str):
        """
        Показывает окно с сообщением.
        :param title: заголовок.
        :param message: сообщение.
        """
        pass

    def open_damaged_notes_window(self) -> WindowDamagedNotes:
        return WindowDamagedNotes()

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
    root.setMinimumSize(root_width, root_height)
    root.show()

    app.exec()


if __name__ == '__main__':
    app_ = QApplication()
    root_ = MainWindow(GuiLabels)
    setup_gui(root_, app_)
