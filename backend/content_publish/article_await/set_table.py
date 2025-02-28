



from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



class SetTable:
    def __init__(self, tableWidget, main_page):
        self.tableWidget = tableWidget
        self.main_page = main_page

    def main(self):
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.verticalHeader().hide()  # 隐藏行号

        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['栏目', '文章数量'])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setIconSize(QSize(100, 150))
        self.tableWidget.setColumnWidth(0, 250)  # 设置列宽(第几列， 宽度)
        self.tableWidget.setColumnWidth(1, 100)  # 设置列宽(第几列， 宽度)
        # self.tableWidget.setColumnWidth(2, 40)  # 设置列宽(第几列， 宽度)
        # header = self.tableWidget.horizontalHeader()
        # header.setSectionResizeMode(0, QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        if self.main_page.scale_factor == 1:
            self.tableWidget.setStyleSheet(
                'QTableWidget{border:none;}QHeaderView::section {background-color:#f8f8f8;border:none;height:35px;border-bottom:1px solid #dfdeda;border-top:1px solid #dfdeda;font:11pt "微软雅黑";}')
        elif self.main_page.scale_factor == 1.5:
            self.tableWidget.setStyleSheet(
                'QTableWidget{border:none;}QHeaderView::section {background-color:#f8f8f8;border:none;height:35px;border-bottom:1px solid #dfdeda;border-top:1px solid #dfdeda;font:8pt "微软雅黑";}')
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)

