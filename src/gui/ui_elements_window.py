# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'elements_window.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 374)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 401, 371))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_title = QLabel(self.verticalLayoutWidget)
        self.lbl_title.setObjectName(u"lbl_title")

        self.verticalLayout.addWidget(self.lbl_title)

        self.wdg_items = QListWidget(self.verticalLayoutWidget)
        self.wdg_items.setObjectName(u"wdg_items")

        self.verticalLayout.addWidget(self.wdg_items)

        self.btn_accept = QPushButton(self.verticalLayoutWidget)
        self.btn_accept.setObjectName(u"btn_accept")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_accept.sizePolicy().hasHeightForWidth())
        self.btn_accept.setSizePolicy(sizePolicy1)
        self.btn_accept.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout.addWidget(self.btn_accept, 0, Qt.AlignRight)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lbl_title.setText(QCoreApplication.translate("Form", u"Title", None))
        self.btn_accept.setText(QCoreApplication.translate("Form", u"OK", None))
    # retranslateUi

