# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FTP_setting.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(552, 522)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(120, 30))
        self.label.setMaximumSize(QtCore.QSize(120, 30))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setMinimumSize(QtCore.QSize(100, 30))
        self.radioButton.setMaximumSize(QtCore.QSize(100, 30))
        self.radioButton.setChecked(True)
        self.radioButton.setAutoExclusive(False)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setMinimumSize(QtCore.QSize(100, 30))
        self.radioButton_2.setMaximumSize(QtCore.QSize(100, 30))
        self.radioButton_2.setAutoExclusive(False)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(120, 30))
        self.label_2.setMaximumSize(QtCore.QSize(120, 30))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.radioButton_3 = QtWidgets.QRadioButton(Form)
        self.radioButton_3.setMinimumSize(QtCore.QSize(100, 30))
        self.radioButton_3.setMaximumSize(QtCore.QSize(100, 30))
        self.radioButton_3.setAutoExclusive(False)
        self.radioButton_3.setObjectName("radioButton_3")
        self.horizontalLayout_2.addWidget(self.radioButton_3)
        self.radioButton_4 = QtWidgets.QRadioButton(Form)
        self.radioButton_4.setMinimumSize(QtCore.QSize(100, 30))
        self.radioButton_4.setMaximumSize(QtCore.QSize(100, 30))
        self.radioButton_4.setChecked(True)
        self.radioButton_4.setAutoExclusive(False)
        self.radioButton_4.setObjectName("radioButton_4")
        self.horizontalLayout_2.addWidget(self.radioButton_4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setMinimumSize(QtCore.QSize(120, 30))
        self.label_3.setMaximumSize(QtCore.QSize(120, 30))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setMinimumSize(QtCore.QSize(400, 30))
        self.lineEdit.setMaximumSize(QtCore.QSize(400, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setMinimumSize(QtCore.QSize(120, 30))
        self.label_4.setMaximumSize(QtCore.QSize(120, 30))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(300, 30))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(300, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_4.addWidget(self.lineEdit_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setMinimumSize(QtCore.QSize(120, 30))
        self.label_5.setMaximumSize(QtCore.QSize(120, 30))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(300, 30))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(300, 30))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_5.addWidget(self.lineEdit_3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setMinimumSize(QtCore.QSize(120, 30))
        self.label_6.setMaximumSize(QtCore.QSize(120, 30))
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(100, 30))
        self.lineEdit_4.setMaximumSize(QtCore.QSize(100, 30))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_6.addWidget(self.lineEdit_4)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setMinimumSize(QtCore.QSize(120, 30))
        self.label_7.setMaximumSize(QtCore.QSize(120, 30))
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        self.lineEdit_5 = QtWidgets.QLineEdit(Form)
        self.lineEdit_5.setMinimumSize(QtCore.QSize(300, 30))
        self.lineEdit_5.setMaximumSize(QtCore.QSize(300, 30))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_8.addWidget(self.lineEdit_5)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setMinimumSize(QtCore.QSize(120, 30))
        self.label_8.setMaximumSize(QtCore.QSize(120, 30))
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_7.addWidget(self.label_8)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setMinimumSize(QtCore.QSize(400, 200))
        self.textEdit.setMaximumSize(QtCore.QSize(400, 200))
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_7.addWidget(self.textEdit)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem8)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_9.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "FTP设置"))
        self.label.setText(_translate("Form", "远程附件: "))
        self.radioButton.setText(_translate("Form", "启用"))
        self.radioButton_2.setText(_translate("Form", "关闭"))
        self.label_2.setText(_translate("Form", "被动模式: "))
        self.radioButton_3.setText(_translate("Form", "开启"))
        self.radioButton_4.setText(_translate("Form", "不开启"))
        self.label_3.setText(_translate("Form", "FTP地址: "))
        self.lineEdit.setPlaceholderText(_translate("Form", "请填写完整地址"))
        self.label_4.setText(_translate("Form", "FTP账号: "))
        self.label_5.setText(_translate("Form", "FTP密码: "))
        self.label_6.setText(_translate("Form", "FTP端口: "))
        self.lineEdit_4.setPlaceholderText(_translate("Form", "默认\'21\'"))
        self.label_7.setText(_translate("Form", "FTP目录: "))
        self.lineEdit_5.setPlaceholderText(_translate("Form", "默认\'/\'"))
        self.label_8.setText(_translate("Form", "已解析域名: "))
        self.pushButton.setText(_translate("Form", "确认"))
