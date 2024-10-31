# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'upload.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from tools.frontend_tools.SearchComboBox import ExtendedComboBox


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(897, 444)
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
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setMinimumSize(QtCore.QSize(120, 30))
        self.pushButton_3.setMaximumSize(QtCore.QSize(120, 30))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(100, 30))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(120, 30))
        self.label_2.setMaximumSize(QtCore.QSize(120, 30))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setMinimumSize(QtCore.QSize(120, 30))
        self.pushButton_4.setMaximumSize(QtCore.QSize(120, 30))
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setMinimumSize(QtCore.QSize(120, 30))
        self.label_3.setMaximumSize(QtCore.QSize(120, 30))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.comboBox = ExtendedComboBox(Form)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox.setMaximumSize(QtCore.QSize(16777215, 30))
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_3.addWidget(self.comboBox)
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton_5.setMaximumSize(QtCore.QSize(100, 30))
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_3.addWidget(self.pushButton_5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setMinimumSize(QtCore.QSize(0, 30))
        self.checkBox.setMaximumSize(QtCore.QSize(16777215, 30))
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_5.addWidget(self.checkBox)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "上传"))
        self.label.setText(_translate("Form", "选择上传文件"))
        self.pushButton_3.setText(_translate("Form", "打开文件"))
        self.pushButton.setText(_translate("Form", "上传"))
        self.label_2.setText(_translate("Form", "选择上传文件夹"))
        self.pushButton_4.setText(_translate("Form", "打开文件夹"))
        self.pushButton_2.setText(_translate("Form", "上传"))
        self.label_3.setText(_translate("Form", "上传目录"))
        self.pushButton_5.setText(_translate("Form", "搜索文件夹"))
        self.checkBox.setText(_translate("Form", "是否覆盖"))
