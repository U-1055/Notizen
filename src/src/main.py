from PySide6.QtWidgets import QApplication, QMainWindow

from src.gui.view import MainWindow, setup_gui
from src.src.logic import Logic
from src.src.model import DataModel


if __name__ == '__main__':
    from tests.test_configs.model_test_config import TestDataModel

    app_ = QApplication()
    root_ = MainWindow()
    model = TestDataModel()
    presenter = Logic(model, root_)

    setup_gui(root_, app_)
