import typing as tp
from pathlib import Path
import json

class BaseTest:

    def __init__(self):
        pass


def get_test_data(path: Path) -> dict:
    with open(path, 'rb') as test_case:
        return json.load(test_case)
