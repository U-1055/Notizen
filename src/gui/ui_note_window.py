# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'note_window.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QTextEdit, QToolButton,
    QVBoxLayout, QWidget)

from src.gui.tags_widget import TagWidget

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1030, 583)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.btn_return = QToolButton(Form)
        self.btn_return.setObjectName(u"btn_return")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_return.sizePolicy().hasHeightForWidth())
        self.btn_return.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.btn_return)

        self.wdg_tags = TagWidget()
        self.wdg_tags.setObjectName(u"wdg_tags")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.wdg_tags.sizePolicy().hasHeightForWidth())
        self.wdg_tags.setSizePolicy(sizePolicy2)
        self.wdg_tags.setMinimumSize(QSize(500, 80))
        self.wdg_tags.setMaximumSize(QSize(16777215, 0))

        self.horizontalLayout.addWidget(self.wdg_tags, 0, Qt.AlignLeft|Qt.AlignTop)

        self.line_edit_name = QLineEdit(Form)
        self.line_edit_name.setObjectName(u"line_edit_name")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.line_edit_name.sizePolicy().hasHeightForWidth())
        self.line_edit_name.setSizePolicy(sizePolicy3)
        self.line_edit_name.setMaximumSize(QSize(133, 16777215))
        self.line_edit_name.setMaxLength(32767)
        self.line_edit_name.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.line_edit_name, 0, Qt.AlignRight)

        self.btn_save = QToolButton(Form)
        self.btn_save.setObjectName(u"btn_save")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.btn_save.sizePolicy().hasHeightForWidth())
        self.btn_save.setSizePolicy(sizePolicy4)

        self.horizontalLayout.addWidget(self.btn_save)

        self.btn_info = QPushButton(Form)
        self.btn_info.setObjectName(u"btn_info")

        self.horizontalLayout.addWidget(self.btn_info, 0, Qt.AlignRight)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(4, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.wdg_text = QTextEdit(Form)
        self.wdg_text.setObjectName(u"wdg_text")

        self.horizontalLayout_5.addWidget(self.wdg_text)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 11)

        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_return.setText(QCoreApplication.translate("Form", u"<-", None))
        self.line_edit_name.setText("")
        self.btn_save.setText(QCoreApplication.translate("Form", u"...", None))
        self.btn_info.setText(QCoreApplication.translate("Form", u"...", None))
    # retranslateUi

