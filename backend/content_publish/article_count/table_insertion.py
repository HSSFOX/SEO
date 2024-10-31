


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import *


class TableInsertion:
    def __init__(self, tableWidget):
        self.tableWidget = tableWidget

    def table_main(self, task_info_l):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(task_info_l))
        for row, task_info in enumerate(task_info_l):
            # print(task_info)
            if not task_info['web']:
                name_w = QTableWidgetItem(str(task_info['catid'] + task_info['name']))
            else:
                name_w = QTableWidgetItem(str(task_info['name']))
            left_count_w = QTableWidgetItem(task_info['left_count'])
            # left_count_w.setData(Qt.DisplayRole, int(task_info['left_count']))

            count_w = QTableWidgetItem()
            count_w.setData(Qt.DisplayRole, int(task_info['count']))

            self.tableWidget.setItem(row, 0, name_w)
            self.tableWidget.setItem(row, 1, left_count_w)
            self.tableWidget.setItem(row, 2, count_w)

            self.center(name_w)
            self.center(left_count_w)
            self.center(count_w)

    def center(self, value):
        # font = QFont()
        # font.setFamily("微软雅黑")
        value.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)  # 对齐
        # value.setFont(font)