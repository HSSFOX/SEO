# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AI_write.ui'
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
        Form.resize(1350, 542)
        Form.setMinimumSize(QtCore.QSize(1350, 500))
        Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(120, 30))
        self.label.setMaximumSize(QtCore.QSize(120, 30))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setMinimumSize(QtCore.QSize(160, 30))
        self.comboBox.setMaximumSize(QtCore.QSize(16777215, 30))
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(120, 30))
        self.label_2.setMaximumSize(QtCore.QSize(120, 30))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.comboBox_2 = ExtendedComboBox(Form)
        self.comboBox_2.setMinimumSize(QtCore.QSize(160, 30))
        self.comboBox_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout_4.addWidget(self.comboBox_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setMinimumSize(QtCore.QSize(300, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_10.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_10.addWidget(self.textEdit)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_7.setMinimumSize(QtCore.QSize(140, 30))
        self.pushButton_7.setMaximumSize(QtCore.QSize(140, 30))
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_3.addWidget(self.pushButton_7)
        self.verticalLayout_10.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5.addWidget(self.groupBox)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setMinimumSize(QtCore.QSize(120, 30))
        self.label_3.setMaximumSize(QtCore.QSize(120, 30))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.textEdit_2 = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_2.setMinimumSize(QtCore.QSize(0, 32))
        self.textEdit_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textEdit_2.setAcceptRichText(False)
        self.textEdit_2.setObjectName("textEdit_2")
        self.horizontalLayout_6.addWidget(self.textEdit_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setMinimumSize(QtCore.QSize(120, 0))
        self.label_4.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)
        self.textEdit_3 = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_3.setMinimumSize(QtCore.QSize(0, 100))
        self.textEdit_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textEdit_3.setAcceptRichText(False)
        self.textEdit_3.setObjectName("textEdit_3")
        self.horizontalLayout_7.addWidget(self.textEdit_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setMinimumSize(QtCore.QSize(120, 45))
        self.label_5.setMaximumSize(QtCore.QSize(120, 45))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_13.addWidget(self.label_5)
        self.textEdit_4 = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_4.setMinimumSize(QtCore.QSize(0, 56))
        self.textEdit_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textEdit_4.setAcceptRichText(False)
        self.textEdit_4.setObjectName("textEdit_4")
        self.horizontalLayout_13.addWidget(self.textEdit_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setContentsMargins(0, 5, 0, 5)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.comboBox_5 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_5.setMinimumSize(QtCore.QSize(120, 30))
        self.comboBox_5.setMaximumSize(QtCore.QSize(16777215, 30))
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.horizontalLayout_15.addWidget(self.comboBox_5)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem3)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setMinimumSize(QtCore.QSize(0, 30))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_15.addWidget(self.label_7)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit.setMinimumSize(QtCore.QSize(70, 30))
        self.lineEdit.setMaximumSize(QtCore.QSize(70, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_15.addWidget(self.lineEdit)
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        self.label_14.setMinimumSize(QtCore.QSize(0, 30))
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_15.addWidget(self.label_14)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(40, 30))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(40, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_15.addWidget(self.lineEdit_2)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(40, 30))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(40, 30))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_15.addWidget(self.lineEdit_3)
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_5.setMinimumSize(QtCore.QSize(0, 30))
        self.checkBox_5.setMaximumSize(QtCore.QSize(16777215, 30))
        self.checkBox_5.setObjectName("checkBox_5")
        self.horizontalLayout_15.addWidget(self.checkBox_5)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_3.setMinimumSize(QtCore.QSize(120, 30))
        self.pushButton_3.setMaximumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setUnderline(True)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_15.addWidget(self.pushButton_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_15)
        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 4)
        self.verticalLayout_5.setStretch(2, 2)
        self.verticalLayout_5.setStretch(3, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_11.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_20 = QtWidgets.QLabel(self.groupBox_3)
        self.label_20.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_20.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_12.addWidget(self.label_20)
        self.label_21 = QtWidgets.QLabel(self.groupBox_3)
        self.label_21.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_21.setStyleSheet("color:red;")
        self.label_21.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_21.setObjectName("label_21")
        self.verticalLayout_12.addWidget(self.label_21)
        self.horizontalLayout_8.addLayout(self.verticalLayout_12)
        self.textEdit_10 = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_10.setMinimumSize(QtCore.QSize(250, 0))
        self.textEdit_10.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textEdit_10.setAcceptRichText(False)
        self.textEdit_10.setObjectName("textEdit_10")
        self.horizontalLayout_8.addWidget(self.textEdit_10)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_15 = QtWidgets.QLabel(self.groupBox_3)
        self.label_15.setMinimumSize(QtCore.QSize(70, 30))
        self.label_15.setMaximumSize(QtCore.QSize(70, 30))
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_16.addWidget(self.label_15)
        self.comboBox_3 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_3.setMinimumSize(QtCore.QSize(100, 30))
        self.comboBox_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.comboBox_3.setObjectName("comboBox_3")
        self.horizontalLayout_16.addWidget(self.comboBox_3)
        self.comboBox_4 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_4.setMinimumSize(QtCore.QSize(150, 30))
        self.comboBox_4.setMaximumSize(QtCore.QSize(16777215, 30))
        self.comboBox_4.setObjectName("comboBox_4")
        self.horizontalLayout_16.addWidget(self.comboBox_4)
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_3.setMinimumSize(QtCore.QSize(0, 30))
        self.checkBox_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout_16.addWidget(self.checkBox_3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem4)
        self.checkBox_10 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_10.setMinimumSize(QtCore.QSize(0, 30))
        self.checkBox_10.setMaximumSize(QtCore.QSize(16777215, 30))
        self.checkBox_10.setObjectName("checkBox_10")
        self.horizontalLayout_16.addWidget(self.checkBox_10)
        self.checkBox_11 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_11.setMinimumSize(QtCore.QSize(0, 30))
        self.checkBox_11.setMaximumSize(QtCore.QSize(16777215, 30))
        self.checkBox_11.setObjectName("checkBox_11")
        self.horizontalLayout_16.addWidget(self.checkBox_11)
        self.checkBox_12 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_12.setMinimumSize(QtCore.QSize(0, 30))
        self.checkBox_12.setMaximumSize(QtCore.QSize(16777215, 30))
        self.checkBox_12.setChecked(True)
        self.checkBox_12.setObjectName("checkBox_12")
        self.horizontalLayout_16.addWidget(self.checkBox_12)
        self.verticalLayout_4.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem5)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_4.setMinimumSize(QtCore.QSize(120, 30))
        self.pushButton_4.setMaximumSize(QtCore.QSize(120, 30))
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_17.addWidget(self.pushButton_4)
        self.label_17 = QtWidgets.QLabel(self.groupBox_3)
        self.label_17.setMinimumSize(QtCore.QSize(0, 30))
        self.label_17.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_17.addWidget(self.label_17)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_8.setMinimumSize(QtCore.QSize(40, 30))
        self.lineEdit_8.setMaximumSize(QtCore.QSize(40, 30))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.horizontalLayout_17.addWidget(self.lineEdit_8)
        self.label_18 = QtWidgets.QLabel(self.groupBox_3)
        self.label_18.setMinimumSize(QtCore.QSize(0, 30))
        self.label_18.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_17.addWidget(self.label_18)
        self.lineEdit_9 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_9.setMinimumSize(QtCore.QSize(40, 30))
        self.lineEdit_9.setMaximumSize(QtCore.QSize(40, 30))
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.horizontalLayout_17.addWidget(self.lineEdit_9)
        self.label_19 = QtWidgets.QLabel(self.groupBox_3)
        self.label_19.setMinimumSize(QtCore.QSize(0, 30))
        self.label_19.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_17.addWidget(self.label_19)
        self.lineEdit_10 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_10.setMinimumSize(QtCore.QSize(40, 30))
        self.lineEdit_10.setMaximumSize(QtCore.QSize(40, 30))
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.horizontalLayout_17.addWidget(self.lineEdit_10)
        self.verticalLayout_4.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_16 = QtWidgets.QLabel(self.groupBox_3)
        self.label_16.setMinimumSize(QtCore.QSize(70, 30))
        self.label_16.setMaximumSize(QtCore.QSize(70, 30))
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_18.addWidget(self.label_16)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(300, 30))
        self.lineEdit_4.setMaximumSize(QtCore.QSize(300, 30))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_18.addWidget(self.lineEdit_4)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem6)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_5.setMinimumSize(QtCore.QSize(170, 30))
        self.pushButton_5.setMaximumSize(QtCore.QSize(170, 30))
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_18.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_6.setMinimumSize(QtCore.QSize(120, 30))
        self.pushButton_6.setMaximumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_18.addWidget(self.pushButton_6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_8.addLayout(self.verticalLayout_4)
        self.verticalLayout_11.addLayout(self.horizontalLayout_8)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.verticalLayout_2.setStretch(0, 2)
        self.verticalLayout_2.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 3)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "AI写作"))
        self.label.setText(_translate("Form", "选择行业"))
        self.label_2.setText(_translate("Form", "选择栏目"))
        self.groupBox.setTitle(_translate("Form", "关键词/文章标题(一行一个)"))
        self.label_6.setText(_translate("Form", "共有0个关键词"))
        self.pushButton_7.setText(_translate("Form", "导入关键词"))
        self.groupBox_2.setTitle(_translate("Form", "内容配置"))
        self.label_3.setText(_translate("Form", "角色定义"))
        self.label_4.setText(_translate("Form", "内容语料"))
        self.label_5.setText(_translate("Form", "标题语料"))
        self.comboBox_5.setItemText(0, _translate("Form", "双标题"))
        self.comboBox_5.setItemText(1, _translate("Form", "三标题"))
        self.label_7.setText(_translate("Form", "字数"))
        self.lineEdit.setText(_translate("Form", "1000"))
        self.label_14.setText(_translate("Form", "新旧标题分割"))
        self.lineEdit_2.setText(_translate("Form", "（"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "前"))
        self.lineEdit_3.setText(_translate("Form", "）"))
        self.lineEdit_3.setPlaceholderText(_translate("Form", "后"))
        self.checkBox_5.setText(_translate("Form", "启用内容配置"))
        self.pushButton_3.setText(_translate("Form", "内容配置"))
        self.groupBox_3.setTitle(_translate("Form", "请求配置"))
        self.label_20.setText(_translate("Form", "Key"))
        self.label_21.setText(_translate("Form", "每行一个"))
        self.label_15.setText(_translate("Form", "模型"))
        self.checkBox_3.setText(_translate("Form", "启用外部接口"))
        self.checkBox_10.setText(_translate("Form", "去除p标签"))
        self.checkBox_11.setText(_translate("Form", "违禁词处理"))
        self.checkBox_12.setText(_translate("Form", "失败自动重试"))
        self.pushButton_4.setText(_translate("Form", "检测Key"))
        self.label_17.setText(_translate("Form", "超时(秒)"))
        self.lineEdit_8.setText(_translate("Form", "20"))
        self.label_18.setText(_translate("Form", "线程"))
        self.lineEdit_9.setText(_translate("Form", "1"))
        self.label_19.setText(_translate("Form", "重试"))
        self.lineEdit_10.setText(_translate("Form", "3"))
        self.label_16.setText(_translate("Form", "请求API"))
        self.pushButton_5.setText(_translate("Form", "打开文章文件夹"))
        self.pushButton_6.setText(_translate("Form", "开始任务"))
