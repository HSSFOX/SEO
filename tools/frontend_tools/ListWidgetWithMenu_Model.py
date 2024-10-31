from PyQt5.QtWidgets import QApplication, QListWidget, QMenu, QAction
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


class ListWidgetWithMenu(QListWidget):
    def __init__(self, parent=None):
        super(ListWidgetWithMenu, self).__init__(parent)
        self.action1 = QAction("添加模板", self)  # 生成一个选项
        self.row = 0

    def contextMenuEvent(self, event):
        # 创建右键菜单
        self.popup_menu = QMenu(self)
        self.popup_menu.addAction(self.action1)  # 将选项添加到菜单中

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

            super().mousePressEvent(event)  # 调用父类的mousePressEvent处理其他事件
            self.row = self.currentRow()  # 行
            # 显示右键菜单
            # self.popup_menu.exec_(event.globalPos())
        else:
            super().mousePressEvent(event)  # 调用父类的mousePressEvent处理其他事件

