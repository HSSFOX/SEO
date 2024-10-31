
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class CHeaderTable(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.popup_menu = QMenu(self)
        self.headerBox = QCheckBox(self.horizontalHeader())
        # self.action1 = QAction("修改", self)  # 生成一个选项
        self.row = 0
        # self.headerBox.setStyleSheet("QCheckBox::indicator {\n"
        #                           "\n"
        #                           "}\n"
        #                           "QCheckBox::indicator:unchecked {\n"
        #                           "image:url(docs/image/未勾选.png)\n"
        #                           "}\n"
        #                           "QCheckBox::indicator:checked {\n"
        #                           "image:url(docs/image/已勾选.png)\n"
        #                           "}\n")

    def resizeEvent(self, event=None):
        super().resizeEvent(event)
        self.headerBox.setGeometry(QRect(11, 10, 20, 20))

    def change_state(self, all_header_combobox):
        if self.headerBox.checkState() == 2:
            for cb in all_header_combobox[:]:
                try:
                    cb.setChecked(True)
                except:
                    all_header_combobox.remove(cb)
        else:
            for cb in all_header_combobox[:]:
                try:
                    cb.setChecked(False)
                except:
                    all_header_combobox.remove(cb)

    def contextMenuEvent(self, event):
        # 创建右键菜单
        # self.popup_menu.addAction(self.action1)  # 将选项添加到菜单中

        # 将菜单显示在鼠标点击的位置
        self.popup_menu.exec_(QCursor.pos())

    def mousePressEvent(self, event):  # 重写mousePressEvent
        if event.button() == Qt.RightButton:
            # 获取点击的单元格位置
            self.row = self.rowAt(event.y())  # 行
            super().mousePressEvent(event)  # 调用父类的mousePressEvent处理其他事件
        else:
            super().mousePressEvent(event)  # 调用父类的mousePressEvent处理其他事件