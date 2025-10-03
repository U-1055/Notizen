# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_menu.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1011, 600)
        MainWindow.setStyleSheet(u"\n"
"QWidget {\n"
"    background-color: #262B2B;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #1F387A;\n"
"    color: white;\n"
"    font-size: 12px;\n"
"    border: 1px solid #FFFFFF;\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QPushButton#start_button {\n"
"    background-color: #1F387A;\n"
"    color: white;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: #000000;\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"QSpinBox {\n"
"    background-color: #000000;\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"QComboBox {\n"
"    background-color: #000000;\n"
"    color: #FFFFFF;\n"
"    border-radius: 3;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView{\n"
"    background-color: black;\n"
"    color: white;\n"
"    selection-background-color: #525252;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item{\n"
"    background-color: black;\n"
"    color: white;\n"
"    selection-background-color: #525252;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item::selected{\n"
"    background-color: #1F387A;\n"
"   "
                        " border: 1px solid gray;\n"
"}\n"
"\n"
"QScrollBar::vertical{\n"
"    background-color: #1F387A;\n"
"    border: 2px solid gray;\n"
"}\n"
"\n"
"QLabel {\n"
"    background-color: #262B2B;\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"QTextEdit {\n"
"    background-color: black;\n"
"    color: #FFFCCF;\n"
"    border: 1px solid white;\n"
"    border-radius: 3;\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"    background-color: #13224A;\n"
"    color: white;\n"
"    font: 12 px;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, -1, 1011, 91))
        self.layout_tools = QGridLayout(self.gridLayoutWidget)
        self.layout_tools.setObjectName(u"layout_tools")
        self.layout_tools.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.gridLayoutWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"")
        self.btn_theme_dark = QPushButton(self.widget)
        self.btn_theme_dark.setObjectName(u"btn_theme_dark")
        self.btn_theme_dark.setGeometry(QRect(890, 0, 111, 23))
        self.btn_theme_light = QPushButton(self.widget)
        self.btn_theme_light.setObjectName(u"btn_theme_light")
        self.btn_theme_light.setGeometry(QRect(890, 30, 111, 23))
        self.line_edit_search = QLineEdit(self.widget)
        self.line_edit_search.setObjectName(u"line_edit_search")
        self.line_edit_search.setGeometry(QRect(340, 0, 341, 31))
        self.btn_search = QPushButton(self.widget)
        self.btn_search.setObjectName(u"btn_search")
        self.btn_search.setGeometry(QRect(680, 0, 31, 31))
        self.frm_tags = QFrame(self.widget)
        self.frm_tags.setObjectName(u"frm_tags")
        self.frm_tags.setGeometry(QRect(340, 40, 341, 31))
        self.frm_tags.setFrameShape(QFrame.StyledPanel)
        self.frm_tags.setFrameShadow(QFrame.Raised)
        self.btn_tag_add = QPushButton(self.widget)
        self.btn_tag_add.setObjectName(u"btn_tag_add")
        self.btn_tag_add.setGeometry(QRect(680, 40, 31, 31))
        self.btn_create_note = QPushButton(self.widget)
        self.btn_create_note.setObjectName(u"btn_create_note")
        self.btn_create_note.setGeometry(QRect(10, 0, 191, 21))
        self.btn_tags = QPushButton(self.widget)
        self.btn_tags.setObjectName(u"btn_tags")
        self.btn_tags.setGeometry(QRect(750, 0, 75, 21))

        self.layout_tools.addWidget(self.widget, 0, 0, 1, 1)

        self.gridLayoutWidget_2 = QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(0, 90, 1011, 481))
        self.layout_notes = QGridLayout(self.gridLayoutWidget_2)
        self.layout_notes.setObjectName(u"layout_notes")
        self.layout_notes.setContentsMargins(0, 0, 0, 0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1011, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_theme_dark.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0451\u043c\u043d\u0430\u044f", None))
        self.btn_theme_light.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0432\u0435\u0442\u043b\u0430\u044f", None))
        self.btn_search.setText("")
        self.btn_tag_add.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.btn_create_note.setText(QCoreApplication.translate("MainWindow", u"+ \u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0437\u0430\u043c\u0435\u0442\u043a\u0443", None))
        self.btn_tags.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u0433\u0438 ...", None))
    # retranslateUi

