



from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class SetTable:
    def __init__(self, tableWidget, tableWidget_2, main_page):
        self.tableWidget = tableWidget
        self.tableWidget_2 = tableWidget_2
        self.main_page = main_page

    def main(self):
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().hide()  # 隐藏行号

        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['被重定向', '重定向类型', '重定向方式', '重定向到'])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setIconSize(QSize(100, 150))
        self.tableWidget.setColumnWidth(0, 200)  # 设置列宽(第几列， 宽度)
        self.tableWidget.setColumnWidth(1, 70)  # 设置列宽(第几列， 宽度)
        self.tableWidget.setColumnWidth(2, 70)  # 设置列宽(第几列， 宽度)
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


        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().hide()  # 隐藏行号

        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setHorizontalHeaderLabels(['序列号', '域名', '子域名'])
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.setIconSize(QSize(100, 150))
        self.tableWidget_2.setColumnWidth(0, 50)  # 设置列宽(第几列， 宽度)
        self.tableWidget_2.setColumnWidth(1, 200)  # 设置列宽(第几列， 宽度)
        # self.tableWidget_2.setColumnWidth(2, 70)  # 设置列宽(第几列， 宽度)
        # self.tableWidget.setColumnWidth(2, 40)  # 设置列宽(第几列， 宽度)
        # header = self.tableWidget.horizontalHeader()
        # header.setSectionResizeMode(0, QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        if self.main_page.scale_factor == 1:
            self.tableWidget_2.setStyleSheet(
                'QTableWidget{border:none;}QHeaderView::section {background-color:#f8f8f8;border:none;height:35px;border-bottom:1px solid #dfdeda;border-top:1px solid #dfdeda;font:11pt "微软雅黑";}')
        elif self.main_page.scale_factor == 1.5:
            self.tableWidget_2.setStyleSheet(
                'QTableWidget{border:none;}QHeaderView::section {background-color:#f8f8f8;border:none;height:35px;border-bottom:1px solid #dfdeda;border-top:1px solid #dfdeda;font:8pt "微软雅黑";}')
