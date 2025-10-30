from PySide6.QtWidgets import QApplication, QMainWindow, QMenu
from PySide6.QtGui import QAction
import pytest

import typing as tp

from src.gui.tags_widget import TagWidget


def base_test(test_func: tp.Callable):

    def test(*args):
        print(f'Start test {test_func}')
        test_func(*args)
        print('Test completed')

    return test


class TagWidgetTest:

    def __init__(self, root: QMainWindow, tag_widget: TagWidget):
        self.root = root
        self.tag_widget = tag_widget

    def set_new_tag_widget(self, tag_widget: TagWidget):
        self.tag_widget = tag_widget

    def test_delete_tags(self, tags_before: list[str]):
        menu_before = QMenu()
        actions_before = {tag: QAction(tag, self.root) for tag in tags_before}
        menu_before.addActions(tuple(actions_before.values()))

        menu_after = QMenu()
        tags_after = tags_before[0:len(tags_before) // 2]
        actions_after = {tag: QAction(tag, self.root) for tag in tags_after}
        menu_after.addActions(tuple(actions_after.values()))

        self.tag_widget.set_tag_menu(menu_before)  # Установка меню
        for tag in actions_before.values():  # Добавление тегов
            self.tag_widget._add_tag(tag)
        self.tag_widget.set_tag_menu(menu_after)  # Смена меню на то, в котором нет половины тегов
        # TagWidget должен удалить теги, которых нет в его текущем меню
        current_tags = self.tag_widget.tags()
        assert set(current_tags) == set(tags_after), f'\nTags before: {tags_before}\nTags after: {tags_after}\nCurrent tags: {current_tags}'


def test_1():
    app = QApplication()

    root = QMainWindow()

    mlw = TagWidget()
    root.setCentralWidget(mlw)
    root.show()

    test = TagWidgetTest(root, mlw)
    test.test_delete_tags([f'tag#{i}' for i in range(20)])

    app.exec()



if __name__ == '__main__':
    pass
