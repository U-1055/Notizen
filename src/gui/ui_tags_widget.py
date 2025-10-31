# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tags_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLayout,
    QPushButton, QScrollArea, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(541, 118)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.tag_widget = QFrame(Form)
        self.tag_widget.setObjectName(u"tag_widget")
        self.tag_widget.setGeometry(QRect(50, 20, 421, 81))
        sizePolicy.setHeightForWidth(self.tag_widget.sizePolicy().hasHeightForWidth())
        self.tag_widget.setSizePolicy(sizePolicy)
        self.tag_widget.setFrameShape(QFrame.StyledPanel)
        self.tag_widget.setFrameShadow(QFrame.Plain)
        self.tag_widget.setLineWidth(5)
        self.horizontalLayoutWidget = QWidget(self.tag_widget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 421, 73))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.horizontalLayoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setEnabled(True)
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 16, 16))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_2.setSizePolicy(sizePolicy1)
        self.scrollAreaWidgetContents_2.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.horizontalLayoutWidget_2 = QWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, -1, 331, 51))
        self.frm_tags = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.frm_tags.setObjectName(u"frm_tags")
        self.frm_tags.setSizeConstraint(QLayout.SetMinimumSize)
        self.frm_tags.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.scrollAreaWidgetContents_2.setLayout(self.frm_tags)

        self.horizontalLayout.addWidget(self.scrollArea, 0, Qt.AlignTop)

        self.btn_add_tag = QPushButton(self.horizontalLayoutWidget)
        self.btn_add_tag.setObjectName(u"btn_add_tag")
        sizePolicy1.setHeightForWidth(self.btn_add_tag.sizePolicy().hasHeightForWidth())
        self.btn_add_tag.setSizePolicy(sizePolicy1)
        self.btn_add_tag.setMaximumSize(QSize(16777215, 16777213))
        self.btn_add_tag.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.btn_add_tag, 0, Qt.AlignTop)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_add_tag.setText(QCoreApplication.translate("Form", u"+", None))
    # retranslateUi

