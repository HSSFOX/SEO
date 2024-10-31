


from PyQt5.QtCore import *
from PyQt5.QtGui import *



class SetTable:
    def __init__(self, tableWidget, tableWidget_2, main_page):
        self.tableWidget = tableWidget
        self.tableWidget_2 = tableWidget_2
        self.main_page = main_page

    def setfont(self, value):
        value.setFont(QFont('宋体', 9))
        return value

    def main(self):
        # font = QFont('宋体')
        # font.setPointSize(19)
        # # font.setPointSize(10)
        # font.setBold(True)


        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['序列号', '发布域名', '发布时间', '推送状态'])
        # self.tableWidget.horizontalHeader().setFont(font)
        # self.tableWidget.horizontalHeader().setFont(font)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().hide()  # 隐藏行号
        self.tableWidget.setIconSize(QSize(100, 150))
        self.tableWidget.setColumnWidth(0, 80)  # 设置列宽(第几列， 宽度)
        self.tableWidget.setColumnWidth(1, 230)  # 设置列宽(第几列， 宽度)
        self.tableWidget.setColumnWidth(2, 100)  # 设置列宽(第几列， 宽度)
        self.tableWidget.setColumnWidth(3, 70)  # 设置列宽(第几列， 宽度)
        if self.main_page.scale_factor == 1:
            self.tableWidget.setStyleSheet(
                'QTableWidget{border:none;}QHeaderView::section {background-color:#f8f8f8;border:none;height:35px;border-bottom:1px solid #dfdeda;border-top:1px solid #dfdeda;font:11pt "微软雅黑";}')
        elif self.main_page.scale_factor == 1.5:
            self.tableWidget.setStyleSheet(
                'QTableWidget{border:none;}QHeaderView::section {background-color:#f8f8f8;border:none;height:35px;border-bottom:1px solid #dfdeda;border-top:1px solid #dfdeda;font:8pt "微软雅黑";}')

        self.tableWidget_2.setColumnCount(6)
        self.tableWidget_2.setHorizontalHeaderLabels(['序列号', '发布域名', '发布时间', '标题', '是否发布', '发布链接'])
        # self.tableWidget_2.horizontalHeader().setFont(QFont('宋体', 13))
        self.tableWidget_2.verticalHeader().hide()  # 隐藏行号
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.setIconSize(QSize(100, 150))
        self.tableWidget_2.setColumnWidth(0, 60)  # 设置列宽(第几列， 宽度)
        self.tableWidget_2.setColumnWidth(1, 130)  # 设置列宽(第几列， 宽度)
        self.tableWidget_2.setColumnWidth(2, 100)  # 设置列宽(第几列， 宽度)
        self.tableWidget_2.setColumnWidth(3, 130)  # 设置列宽(第几列， 宽度)
        self.tableWidget_2.setColumnWidth(4, 70)  # 设置列宽(第几列， 宽度)
        if self.main_page.scale_factor == 1:
            self.tableWidget_2.setStyleSheet(
                'QTableWidget{border:none;}QHeaderView::section {background-color:#f8f8f8;border:none;height:35px;border-bottom:1px solid #dfdeda;border-top:1px solid #dfdeda;font:11pt "微软雅黑";}')
        elif self.main_page.scale_factor == 1.5:
            self.tableWidget_2.setStyleSheet(
                'QTableWidget{border:none;}QHeaderView::section {background-color:#f8f8f8;border:none;height:35px;border-bottom:1px solid #dfdeda;border-top:1px solid #dfdeda;font:8pt "微软雅黑";}')