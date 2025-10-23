from PySide6.QtWidgets import QApplication, QMainWindow

from pathlib import Path

from src.gui.view import MainWindow, setup_gui
from src.src.logic import Logic
from src.src.model import DataModel
from src.base import DataStructConst, GuiLabels


def launch():
    notes_data_path = Path('..', '..', 'data', 'notes_data', 'notes_data')
    notes_path = Path('..', '..', 'notes')
    resource_path = Path('..', '..', 'data', 'gui_data', 'resource.qrc')

    app_ = QApplication()
    root_ = MainWindow()
    model = DataModel(notes_path, notes_data_path, resource_path, DataStructConst())
    presenter = Logic(model, root_, GuiLabels())

    setup_gui(root_, app_)


if __name__ == '__main__':
    try:
        launch()
    except:
        raise
