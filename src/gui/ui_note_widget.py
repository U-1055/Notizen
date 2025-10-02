# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'note_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(448, 300)
        self.gridLayoutWidget = QWidget(Form)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(70, 70, 301, 201))
        self.main_layout = QGridLayout(self.gridLayoutWidget)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.lbl_name = QLabel(self.gridLayoutWidget)
        self.lbl_name.setObjectName(u"lbl_name")

        self.main_layout.addWidget(self.lbl_name, 0, 0, 1, 1, Qt.AlignHCenter)

        self.txt_content = QTextEdit(self.gridLayoutWidget)
        self.txt_content.setObjectName(u"txt_content")

        self.main_layout.addWidget(self.txt_content, 1, 0, 1, 2)

        self.btn_ops = QPushButton(self.gridLayoutWidget)
        self.btn_ops.setObjectName(u"btn_ops")

        self.main_layout.addWidget(self.btn_ops, 0, 1, 1, 1, Qt.AlignRight|Qt.AlignTop)

        self.lbl_date_changed = QLabel(self.gridLayoutWidget)
        self.lbl_date_changed.setObjectName(u"lbl_date_changed")

        self.main_layout.addWidget(self.lbl_date_changed, 2, 1, 1, 1)

        self.main_layout.setColumnStretch(0, 3)
        self.main_layout.setColumnStretch(1, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lbl_name.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.btn_ops.setText(QCoreApplication.translate("Form", u"...", None))
        self.lbl_date_changed.setText(QCoreApplication.translate("Form", u"TextLabel", None))
    # retranslateUi

