from pathlib import Path
from src.base import DataConst

notes = {
    'note1': {'tags': ['tag1', 'tag2', 'tag3'], 'date_changing': '21.09.2025'},
    'note2': {'tags': ['tag2', 'tag3'], 'date_changing': '21.09.2025'},
    'note3': {'tags': ['tag3'], 'date_changing': '21.09.2025'},
'note4': {'tags': ['tag3'], 'date_changing': '21.09.2025'},
'note5': {'tags': ['tag3'], 'date_changing': '21.09.2025'},
'note6': {'tags': ['tag3'], 'date_changing': '21.09.2025'},
'note7': {'tags': ['tag3'], 'date_changing': '21.09.2025'},
'note8': {'tags': ['tag3'], 'date_changing': '21.09.2025'},
'note9': {'tags': ['tag3'], 'date_changing': '21.09.2025'},
'note10': {'tags': ['tag3'], 'date_changing': '21.09.2025'},
}

content = {
    'note1': ''.join(tuple('note1' for i in range(1000))),
    'note2': ''.join(tuple('note2' for i1 in range(1000))),
    'note3': ''.join(tuple('note3' for i2 in range(1000))),
'note4': ''.join(tuple('note1' for i3 in range(1000))),
    'note5': ''.join(tuple('note2' for i4 in range(1000))),
    'note6': ''.join(tuple('note3' for i5 in range(1000))),
'note7': ''.join(tuple('note1' for i6 in range(1000))),
    'note8': ''.join(tuple('note2' for i7 in range(1000))),
    'note9': ''.join(tuple('note3' for i8 in range(1000))),
'note10': ''.join(tuple('note1' for i9 in range(1000)))
}


class TestDataModel:

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

    def get_note_tags(self, note: str) -> str:
        return notes[note]['tags']

    def get_tags(self) -> tuple[str, ...]:
        return 'tag1', 'tag2', 'tag3'

    def get_note_content(self, note: str):
        return content[note]

    def get_note_date_changing(self, note: str):
        return notes[note]['date_changing']

    def get_notes(self) -> tuple:
        """Возвращает список со всеми заметками"""
        return tuple(notes.keys())


if __name__ == '__main__':
    pass
