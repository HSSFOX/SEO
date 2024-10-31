
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import datetime
import json


class TableInsertion():
    def __init__(self, tableWidget):
        self.tableWidget = tableWidget

    def main(self, task_info_l):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(task_info_l))

        for row, task_info in enumerate(task_info_l):
            content = json.loads(task_info['content'])

            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(task_info['name'])))
            if content.get('description'):
                self.tableWidget.setItem(row, 1, QTableWidgetItem(str(content['description'])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(datetime.datetime.fromtimestamp(int(task_info['time'])))))

    def update_table(self, task_info, status):
        web = task_info['web']
        settle_time = str(task_info['settle_time']).split(" ")[-1]          # 可能需要实时的时间
        for i in range(self.tableWidget.rowCount()):
            web_w = self.tableWidget.item(i, 1).text()
            settle_time_w = self.tableWidget.item(i, 2).text()
            if web_w == web and settle_time_w == settle_time:
                if status:
                    self.tableWidget.item(i, 3).setText("已推送")
                    self.append_tableWidget_2(task_info)
                else:
                    self.tableWidget.item(i, 3).setText("推送失败")

    #
    # def append_tableWidget_2(self, task_info):
    #     rowCount = self.tableWidget_2.rowCount()
    #     self.tableWidget_2.insertRow(rowCount)
    #     self.tableWidget_2.setItem(rowCount, 0, QTableWidgetItem(str(rowCount + 1)))
    #     self.tableWidget_2.setItem(rowCount, 1, QTableWidgetItem(str(task_info['web'])))
    #     self.tableWidget_2.setItem(rowCount, 2, QTableWidgetItem(str(task_info['settle_time']).split(" ")[-1]))
    #     self.tableWidget_2.setItem(rowCount, 4, QTableWidgetItem("已发布"))



