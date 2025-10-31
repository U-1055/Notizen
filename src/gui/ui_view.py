# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_menu_new.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLayout, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

from src.gui.tags_widget import TagWidget

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1023, 610)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetMinimumSize)
        self.btn_create_note_2 = QPushButton(Form)
        self.btn_create_note_2.setObjectName(u"btn_create_note_2")

        self.verticalLayout_3.addWidget(self.btn_create_note_2)

        self.btn_tags_2 = QPushButton(Form)
        self.btn_tags_2.setObjectName(u"btn_tags_2")

        self.verticalLayout_3.addWidget(self.btn_tags_2, 0, Qt.AlignRight)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.line_edit_search = QLineEdit(Form)
        self.line_edit_search.setObjectName(u"line_edit_search")

        self.horizontalLayout_2.addWidget(self.line_edit_search)

        self.btn_search = QPushButton(Form)
        self.btn_search.setObjectName(u"btn_search")

        self.horizontalLayout_2.addWidget(self.btn_search)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line)

        self.btn_update = QPushButton(Form)
        self.btn_update.setObjectName(u"btn_update")

        self.horizontalLayout_2.addWidget(self.btn_update)

        self.horizontalLayout_2.setStretch(0, 10)
        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.wdg_tags = TagWidget()
        self.wdg_tags.setObjectName(u"wdg_tags")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.wdg_tags.sizePolicy().hasHeightForWidth())
        self.wdg_tags.setSizePolicy(sizePolicy1)
        self.wdg_tags.setMinimumSize(QSize(440, 75))
        self.wdg_tags.setMaximumSize(QSize(16777215, 3547))

        self.verticalLayout_2.addWidget(self.wdg_tags, 0, Qt.AlignVCenter)

        self.verticalLayout_2.setStretch(0, 2)
        self.verticalLayout_2.setStretch(1, 1)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.btn_dark_theme = QPushButton(Form)
        self.btn_dark_theme.setObjectName(u"btn_dark_theme")

        self.verticalLayout_5.addWidget(self.btn_dark_theme)

        self.btn_light_theme = QPushButton(Form)
        self.btn_light_theme.setObjectName(u"btn_light_theme")

        self.verticalLayout_5.addWidget(self.btn_light_theme)


        self.horizontalLayout_3.addLayout(self.verticalLayout_5)


        self.horizontalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaContent = QWidget()
        self.scrollAreaContent.setObjectName(u"scrollAreaContent")
        self.scrollAreaContent.setEnabled(True)
        self.scrollAreaContent.setGeometry(QRect(0, 0, 16, 16))
        sizePolicy.setHeightForWidth(self.scrollAreaContent.sizePolicy().hasHeightForWidth())
        self.scrollAreaContent.setSizePolicy(sizePolicy)
        self.gridLayoutWidget = QWidget(self.scrollAreaContent)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 1001, 501))
        self.frm_notes = QGridLayout(self.gridLayoutWidget)
        self.frm_notes.setObjectName(u"frm_notes")
        self.frm_notes.setSizeConstraint(QLayout.SetMaximumSize)
        self.frm_notes.setVerticalSpacing(10)
        self.frm_notes.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setWidget(self.scrollAreaContent)
        self.scrollAreaContent.setLayout(self.frm_notes)

        self.verticalLayout_4.addWidget(self.scrollArea)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(2, 6)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_create_note_2.setText(QCoreApplication.translate("Form", u"+ \u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0437\u0430\u043c\u0435\u0442\u043a\u0443", None))
        self.btn_tags_2.setText(QCoreApplication.translate("Form", u"\u0422\u0435\u0433\u0438 ...", None))
        self.btn_search.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.btn_update.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.btn_dark_theme.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.btn_light_theme.setText(QCoreApplication.translate("Form", u"PushButton", None))
    # retranslateUi

