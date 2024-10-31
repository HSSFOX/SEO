
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



class SetTable:
    def __init__(self, tableWidget, main_page):
        self.tableWidget = tableWidget
        self.main_page = main_page

    def main(self):
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().hide()  # 隐藏行号

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['', '序号', '名称', '拼音', '长尾数量', '分类', '添加时间'])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setIconSize(QSize(100, 150))
        self.tableWidget.setColumnWidth(0, 50)  # 设置列宽(第几列， 宽度)
        self.tableWidget.setColumnWidth(1, 40)  # 设置列宽(第几列， 宽度)
        self.tableWidget.setColumnWidth(2, 300)  # 设置列宽(第几列， 宽度)
        self.tableWidget.setColumnWidth(3, 100)  # 设置列宽(第几列， 宽度)
        self.tableWidget.setColumnWidth(4, 100)  # 设置列宽(第几列， 宽度)
        self.tableWidget.setColumnWidth(5, 100)  # 设置列宽(第几列， 宽度)
        # self.tableWidget.setColumnWidth(6, 500)
        if self.main_page.scale_factor == 1:
            self.tableWidget.setStyleSheet(
                'QTableWidget{border:none;}QHeaderView::section {background-color:#f8f8f8;border:none;height:35px;border-bottom:1px solid #dfdeda;border-top:1px solid #dfdeda;font:11pt "微软雅黑";}')
        elif self.main_page.scale_factor == 1.5:
            self.tableWidget.setStyleSheet(
                'QTableWidget{border:none;}QHeaderView::section {background-color:#f8f8f8;border:none;height:35px;border-bottom:1px solid #dfdeda;border-top:1px solid #dfdeda;font:8pt "微软雅黑";}')

        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
