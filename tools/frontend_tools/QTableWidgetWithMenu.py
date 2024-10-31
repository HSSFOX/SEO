from PyQt5.QtWidgets import QApplication, QTableWidget, QMenu, QAction
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


class TableWidgetWithMenu(QTableWidget):
    def __init__(self, parent=None):
        super(TableWidgetWithMenu, self).__init__(parent)
        self.popup_menu = QMenu(self)
        # self.action1 = QAction("修改", self)  # 生成一个选项
        # self.action2 = QAction("删除", self)
        self.row = 0
        # self.action2.setVisible(False)

    def contextMenuEvent(self, event):
        # 创建右键菜单
        # self.popup_menu.addAction(self.action1)  # 将选项添加到菜单中
        # self.popup_menu.addAction(self.action2)  # 将选项添加到菜单中

        # self.action2.setVisible(False)

        # 将菜单显示在鼠标点击的位置

        self.popup_menu.exec_(QCursor.pos())

        # # 响应菜单项的点击事件
        # action = menu.exec_()
        # if action == add_item:
        #     print("添加菜单项被点击")
        #     menu.close()
        # # elif action == remove_item:
        # #     print("删除菜单项被点击")
        # self.action1.triggered.

    def mousePressEvent(self, event):  # 重写mousePressEvent
        if event.button() == Qt.RightButton:
            # 获取点击的单元格位置
            self.row = self.rowAt(event.y())  # 行
            # self.column = self.columnAt(event.x())  # 列
            super().mousePressEvent(event)  # 调用父类的mousePressEvent处理其他事件

            # 显示右键菜单
            # self.popup_menu.exec_(event.globalPos())
        else:
            super().mousePressEvent(event)  # 调用父类的mousePressEvent处理其他事件


