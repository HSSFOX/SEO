# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FTP_management.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from tools.frontend_tools.QTableWidgetWithMenu import TableWidgetWithMenu


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(967, 565)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        # self.dateEdit = QtWidgets.QDateEdit(Form)
        # self.dateEdit.setMinimumSize(QtCore.QSize(130, 30))
        # self.dateEdit.setMaximumSize(QtCore.QSize(130, 30))
        # self.dateEdit.setCalendarPopup(True)
        # self.dateEdit.setObjectName("dateEdit")
        # self.horizontalLayout.addWidget(self.dateEdit)
        # self.label = QtWidgets.QLabel(Form)
        # self.label.setObjectName("label")
        # self.horizontalLayout.addWidget(self.label)
        # self.dateEdit_2 = QtWidgets.QDateEdit(Form)
        # self.dateEdit_2.setMinimumSize(QtCore.QSize(130, 30))
        # self.dateEdit_2.setMaximumSize(QtCore.QSize(130, 30))
        # self.dateEdit_2.setCalendarPopup(True)
        # self.dateEdit_2.setObjectName("dateEdit_2")
        # self.horizontalLayout.addWidget(self.dateEdit_2)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setMaximumSize(QtCore.QSize(400, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(100, 30))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = TableWidgetWithMenu(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "FTP管理"))
        # self.label.setText(_translate("Form", "~"))
        self.pushButton.setText(_translate("Form", "搜索"))
        self.pushButton_2.setText(_translate("Form", "添加FTP"))
