from PySide6.QtWidgets import QApplication, QMainWindow

from pathlib import Path

from src.gui.view import MainWindow, setup_gui
from src.src.logic import Logic
from src.src.model import DataModel
from src.base import DataStructConst, GuiLabels, GuiConst


def launch():
    notes_data_path = Path('..', '..', 'data', 'notes_data', 'notes_data')
    notes_path = Path('..', '..', 'notes')
    common_data_path = Path('..', '..', 'data', 'notes_data', 'common_data.json')
    resource_path = Path('..', '..', 'data', 'gui_data', 'resource.qrc')

    app_ = QApplication()
    root_ = MainWindow(GuiLabels())
    model = DataModel(notes_path, notes_data_path, common_data_path, resource_path, DataStructConst())
    presenter = Logic(model, root_, GuiLabels(), GuiConst(), DataStructConst())
    setup_gui(root_, app_)


if __name__ == '__main__':
    try:
        launch()
    except:
        raise
