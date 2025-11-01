from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QMenu, QSizePolicy, QAbstractItemView, QLabel
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal, Qt

import typing as tp

from src.interfaces import IView
from src.gui.ui_view import Ui_Form
from src.gui.widgets import NoteView, NoteWindow, MessageListWidget
from src.gui.tags_widget import TagWidget
from src.base import GuiLabels


class MainWindow(QMainWindow):

    btn_create_note_pressed = Signal()
    btn_tags_pressed = Signal()
    btn_dark_theme_pressed = Signal()
    btn_light_theme_pressed = Signal()
    btn_add_tag_pressed = Signal()
    tried_to_close = Signal()  # Окно попытались закрыть
    btn_search_pressed = Signal()  # Нажата кнопка поиска
    btn_update_pressed = Signal()  # Нажата кнопка "Обновить"

    showed = Signal()

    def __init__(self, labels: GuiLabels):
        super().__init__()
        self._main_widget = QStackedWidget()
        self.setCentralWidget(self._main_widget)

        container = QWidget()
        self._view = Ui_Form()
        self._view.setupUi(container)
        self._main_widget.insertWidget(0, container)

        self._view.btn_update.clicked.connect(self.press_btn_update)
        self._view.btn_create_note_2.clicked.connect(self.press_btn_create_note)
        self._view.btn_search.clicked.connect(self.press_btn_search)
        self._view.btn_tags_2.clicked.connect(self.press_btn_tags)
        self._view.btn_dark_theme.clicked.connect(self.press_btn_dark_theme)
        self._view.btn_light_theme.clicked.connect(self.press_btn_light_theme)

        self._labels = labels

        self._last_row, self._last_column = 0, 0
        self.open_main_menu()

    def _show_damaged_notes_window(self, window: MessageListWidget):
        window.setWindowModality(Qt.WindowModality.ApplicationModal)
        window.show()
        window.raise_()
        window.selectAll()

    def try_to_close(self):
        self.tried_to_close.emit()

    def press_btn_create_note(self):
        self.btn_create_note_pressed.emit()

    def press_btn_tags(self):
        self.btn_tags_pressed.emit()

    def press_btn_dark_theme(self):
        self.btn_dark_theme_pressed.emit()

    def press_btn_light_theme(self):
        self.btn_light_theme_pressed.emit()

    def press_btn_search(self):
        self.btn_search_pressed.emit()

    def press_btn_update(self):
        self.btn_update_pressed.emit()

    def show_no_found_label(self, text: str):
        lbl = QLabel(text)
        self._view.frm_notes.addWidget(lbl)

    def open_main_menu(self):
        self._main_widget.setCurrentIndex(0)

        if self._labels:
            self._view.btn_dark_theme.setText(self._labels.set_theme_dark)
            self._view.btn_light_theme.setText(self._labels.set_theme_light)
            self._view.btn_create_note_2.setText(self._labels.create_note)
            self._view.btn_tags_2.setText(self._labels.view_tags)
            self._view.btn_search.setText(self._labels.search)
            self._view.btn_update.setText(self._labels.update)

    def set_style(self, style: str):
        self.setStyleSheet(style)

    def clear_notes(self):
        for idx in range(self._view.frm_notes.count()):
            self._view.frm_notes.itemAt(idx).widget().hide()
        self._last_row = self._last_column = 0

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
        list(action.triggered.connect(elements[idx][1]) for idx, action in enumerate(actions))  # Привязка слотов к действиям

        menu.addActions(actions)  # Добавление действий в меню

        return menu

    def get_tag_widget(self) -> TagWidget:
        """Возвращает виджет тегов."""
        return self._view.wdg_tags

    def get_tag_window(self):
        pass

    def get_create_note_window(self):
        pass

    def show_message(self, title: str, message: str):
        """
        Показывает окно с сообщением.
        :param title: заголовок.
        :param message: сообщение.
        """
        pass

    def open_damaged_notes_window(self) -> MessageListWidget:
        window = MessageListWidget()
        window.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        window.set_title_text(self._labels.damaged_notes_message)
        window.set_btn_text(self._labels.reclaim)

        self.showed.connect(lambda: self._show_damaged_notes_window(window))

        return window

    def get_selected_tags(self) -> tuple[str]:
        pass

    def search_text(self) -> str:
        return self._view.line_edit_search.text()

    def showEvent(self, event, /):
        self.showed.emit()

    def closeEvent(self, event, /):
        self.try_to_close()

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
    root_ = MainWindow(GuiLabels())
    setup_gui(root_, app_)
