import requests
from PySide6.QtWidgets import QApplication, QMainWindow

from pathlib import Path

from src.gui.view import MainWindow, setup_gui
from src.src.logic import Logic
from src.src.model import DataModel, Model
from src.base import DataStructConst, GuiLabels, GuiConst
from server.app import run_server
from src.src.requests_module import Requester


if __name__ == '__main__':
    try:
        notes_data_path = Path('..', '..', 'data', 'notes_data', 'notes_data')
        notes_path = Path('..', '..', 'notes')
        common_data_path = Path('..', '..', 'data', 'notes_data', 'common_data.json')
        resource_path = Path('..', '..', 'data', 'gui_data', 'resource.qrc')

        config_path = Path('..', '..', 'data', 'client_data', 'config')

        app_ = QApplication()
        root_ = MainWindow(GuiLabels())
        server = 'http://127.0.0.1:5000'
        requester = Requester(server)
        model = DataModel(notes_path, notes_data_path, common_data_path, resource_path, DataStructConst())
        presenter = Logic(Model(resource_path, config_path), root_, server, requester, GuiLabels(), GuiConst(),
                          DataStructConst())
        setup_gui(root_, app_)

    except:
        raise
