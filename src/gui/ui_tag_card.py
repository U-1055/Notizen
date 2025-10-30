# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tag_card.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QToolButton, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QSize(16777215, 300))
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(110, 50, 121, 24))
        self.horizontalLayout = QHBoxLayout(self.verticalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_tag_card = QLabel(self.verticalLayoutWidget)
        self.lbl_tag_card.setObjectName(u"lbl_tag_card")
        sizePolicy.setHeightForWidth(self.lbl_tag_card.sizePolicy().hasHeightForWidth())
        self.lbl_tag_card.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.lbl_tag_card)

        self.btn_tag_card = QToolButton(self.verticalLayoutWidget)
        self.btn_tag_card.setObjectName(u"btn_tag_card")
        sizePolicy.setHeightForWidth(self.btn_tag_card.sizePolicy().hasHeightForWidth())
        self.btn_tag_card.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.btn_tag_card)

        self.horizontalLayout.setStretch(0, 10)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lbl_tag_card.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.btn_tag_card.setText(QCoreApplication.translate("Form", u"x", None))
    # retranslateUi

