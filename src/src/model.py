from pathlib import Path
from src.base import DataConst


class DataModel:

    def __init__(self):
        pass

    def _check_compliance(self, path: Path) -> bool:
        """Проверяет соответствие файла требованиям"""
        if path.suffix != '.txt':
            return False
        if path.stat().st_size > DataConst.max_size:
            return False
        return True

    def get_note_data(self, note: str):
        return

    def get_note_tags(self, note: str):
        pass

    def get_tags(self) -> tuple[str, ...]:
        pass

    def get_note_content(self, note: str):
        pass

    def get_note_date_changing(self, note: str):
        pass

    def get_notes(self) -> tuple:
        """Возвращает список со всеми заметками"""

