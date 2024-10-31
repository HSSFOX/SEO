



from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import datetime
import logging


class TableInsertion():
    def __init__(self, ui, tableWidget, tableWidget_2):
        self.ui = ui
        self.tableWidget = tableWidget
        self.tableWidget_2 = tableWidget_2
        self.row_limit = self.ui.row_limit

    def main(self, task_info_l):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(task_info_l))
        for row, task_info in enumerate(task_info_l):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(task_info['web'])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(datetime.datetime.fromtimestamp(int(task_info['settle_time'])).time())))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(task_info['published'])))

    def main_2(self, task_info_l):
        self.tableWidget_2.clearContents()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setRowCount(len(task_info_l))
        for row, task_info in enumerate(task_info_l):
            if task_info['published'] == '已推送':
                self.tableWidget_2.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                self.tableWidget_2.setItem(row, 1, QTableWidgetItem(str(task_info['web'])))
                self.tableWidget_2.setItem(row, 2, QTableWidgetItem(str(datetime.datetime.fromtimestamp(int(task_info['settle_time'])).time())))
                self.tableWidget_2.setItem(row, 3, QTableWidgetItem(str(task_info['title'])))
                self.tableWidget_2.setItem(row, 4, QTableWidgetItem(str(task_info['published'])))
                self.tableWidget_2.setItem(row, 5, QTableWidgetItem(str(task_info['published_url'])))


    def t1_insertion(self, task_info_l):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(task_info_l))

        for row, task_info in enumerate(task_info_l):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(task_info['web'])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(datetime.datetime.fromtimestamp(int(task_info['settle_time'])).time())))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(task_info['published'])))

    def t2_insertion(self, task_info_l):
        self.tableWidget_2.clearContents()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setRowCount(len(task_info_l))

        for row, task_info in enumerate(task_info_l):
            title_w = task_info['title']
            self.tableWidget_2.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.tableWidget_2.setItem(row, 1, QTableWidgetItem(str(task_info['web'])))
            self.tableWidget_2.setItem(row, 2, QTableWidgetItem(str(datetime.datetime.fromtimestamp(int(task_info['settle_time'])).time())))
            self.tableWidget_2.setItem(row, 2, QTableWidgetItem(str(task_info['title'])))
            self.tableWidget_2.setItem(row, 4, QTableWidgetItem(str(task_info['published'])))

    def update_table(self, task_info, status):
        web = task_info['web']
        settle_time = str(datetime.datetime.fromtimestamp(int(task_info['settle_time'])).time())          # 可能需要实时的时间
        for i in range(self.tableWidget.rowCount()):
            web_w = self.tableWidget.item(i, 1).text()
            settle_time_w = self.tableWidget.item(i, 2).text()
            if web_w == web and settle_time_w == settle_time:
                self.tableWidget.item(i, 3).setText(task_info['published'])

        if status:
            self.append_tableWidget_2(task_info)

        self.tableWidget.viewport().update()

    def append_tableWidget_2(self, task_info):
        try:
            rowCount = self.tableWidget_2.rowCount()
            if rowCount <= self.row_limit:              # 在不翻页的情况下 数据往里加 只有在当前row count不超过100的情况下
                self.tableWidget_2.insertRow(rowCount)
                title_w = task_info['title']
                self.tableWidget_2.setItem(rowCount, 0, QTableWidgetItem(str(rowCount + 1)))
                self.tableWidget_2.setItem(rowCount, 1, QTableWidgetItem(str(task_info['web'])))
                self.tableWidget_2.setItem(rowCount, 2, QTableWidgetItem(
                    str(datetime.datetime.fromtimestamp(int(task_info['settle_time'])).time())))
                self.tableWidget_2.setItem(rowCount, 3, QTableWidgetItem(str(title_w)))
                self.tableWidget_2.setItem(rowCount, 4, QTableWidgetItem(task_info['published']))
                self.tableWidget_2.setItem(rowCount, 5, QTableWidgetItem(task_info['published_url']))
        except Exception as e:
            logging.error(e, exc_info=True)
