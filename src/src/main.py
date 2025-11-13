import requests
from PySide6.QtWidgets import QApplication, QMainWindow

from pathlib import Path

from src.gui.view import MainWindow, setup_gui
from src.src.logic import Logic
from src.src.model import DataModel
from src.base import DataStructConst, GuiLabels, GuiConst
from server.app import run_server
from src.src.requests_module import Requester

def launch():
    notes_data_path = Path('..', '..', 'data', 'notes_data', 'notes_data')
    notes_path = Path('..', '..', 'notes')
    common_data_path = Path('..', '..', 'data', 'notes_data', 'common_data.json')
    resource_path = Path('..', '..', 'data', 'gui_data', 'resource.qrc')

    app_ = QApplication()
    root_ = MainWindow(GuiLabels())
    server = 'http://127.0.0.1:5000'
    run_server()
    requester = Requester(server)
    model = DataModel(notes_path, notes_data_path, common_data_path, resource_path, DataStructConst())
    presenter = Logic(model, root_, server, requester, GuiLabels(), GuiConst(), DataStructConst())
    setup_gui(root_, app_)


if __name__ == '__main__':
    try:
        launch()
    except:
        raise
