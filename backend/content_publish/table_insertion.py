


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import datetime


class TableInsertion:
    def __init__(self, tableWidget):
        self.tableWidget = tableWidget

    def table_2_main(self, task_info_l):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(task_info_l))

        for row, task_info in enumerate(task_info_l):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(task_info['title'])))
            # self.tableWidget.setItem(row, 3, QTableWidgetItem(str(task_info['num'])))


    def table_main(self, task_info_l):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(task_info_l))


        for row, task_info in enumerate(task_info_l):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(task_info['name'])))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(task_info['count'])))
            # self.tableWidget.setItem(row, 3, QTableWidgetItem(str(task_info['num'])))