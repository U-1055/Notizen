from PySide6.QtCore import Signal, QObject

class MockTagWidget:

    def __init__(self):
        self._tags = ()

    def set_tags(self, tags: list[str] | tuple[str, ...]):
        self._tags = tags

    def tags(self) -> tuple[str, ...]:
        return self._tags

    def set_tag_menu(self, menu):
        pass


class MockWindowDamagedNotes(QObject):
    elements_chosen = Signal(tuple[str, ...])

    def set_elements(self, elements: tuple[str, ...]):
        pass