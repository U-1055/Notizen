from src.gui.widgets import NoteView

note_state_ = {'tags': ['tag1', 'tag2', 'tag3'], 'date_changing': '21.09.2025'}


def test_placing_notes_state(note_state: dict, note_view: NoteView):
    assert note_state['tags'] == note_view.tags, \
        f'Note tags != note tags in base: Note tags: {note_view.tags} != in base: {note_state['tags']} '
    assert note_state['date_changing'] == note_view.date_changing, \
        f'Note tags != note tags in base: Note tags: {note_view.date_changing} != in base: {note_state['date_changing']} '


class TestPlacingNotesState:

    def __init__(self, notes: list[str], l):
        self._notes_state = notes


