# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QSplitter
from PyQt5 import QtCore, QtGui, QtWidgets
from api_requests.TokenAPI import Token
import requests
import datetime
from PyQt5.QtCore import *
import random
import base64
import re
from api_requests.TokenAPI import Token
import os
from urllib.parse import urlparse, urlsplit

import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtWidgets import QApplication, QLineEdit, QSizePolicy, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent, QSize

# Form implementation generated from reading ui file 'textEdit_layout_testing.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setObjectName("textEdit_2")
        # self.verticalLayout.addWidget(self.textEdit_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))




if __name__ == '__main__':
    app = QApplication([])
    ex = Ui_Form()

    # window = MainWindow()
    # window.show()
    app.exec_()