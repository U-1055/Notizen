from pathlib import Path

from src.src.logic import Logic
from src.gui.widgets import WindowDamagedNotes
from src.base import DataStructConst, Messages
from tests.base_tests.test_windows_switching import TestModelConfig, TestViewConfig


class MockView(TestViewConfig):

    def __init__(self):
        pass

    def show_message(self, _: str):
        pass

    def open_damaged_notes_window(self) -> WindowDamagedNotes:
        return WindowDamagedNotes()

class MockModel(TestModelConfig):

    def __init__(self, test_case_path: Path, data_struct: DataStructConst):
        super().__init__(test_case_path, data_struct)


def test(logic, model):
    pass


if __name__ == '__main__':
    model = MockModel(Path(r'C:\Users\filat\PycharmProjects\Notizen\data\test_cases\base_tests\notes_data.json'))
    view = TestViewConfig()
    logic = Logic(model, view, Messages())
    test(logic, model, )

