

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime
import webbrowser


class TableInsertion:
    def __init__(self, tableWidget):
        self.tableWidget = tableWidget
        self.tableWidget.cellDoubleClicked.connect(self.open_web_url)


    def main(self, task_info_l):

        for rP in range(0, self.tableWidget.rowCount())[::-1]:
            self.tableWidget.removeRow(rP)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(task_info_l))
        all_header_combobox = []
        for row, task_info in enumerate(task_info_l):
            print("插入时候的row: ", row, task_info)
            self.tableWidget.setRowHeight(row, 60)
            checkBox = QCheckBox()
            # checkBox.setStyleSheet("QCheckBox::indicator {\n"
            #                        "\n"
            #                        "}\n"
            #                        "QCheckBox::indicator:unchecked {\n"
            #                        "image:url(docs/image/未勾选.png)\n"
            #                        "}\n"
            #                        "QCheckBox::indicator:checked {\n"
            #                        "image:url(docs/image/已勾选.png)\n"
            #                        "}\n")
            checkBox.setCheckState(Qt.Unchecked)
            cb_layout = QHBoxLayout()
            cb_layout.addWidget(checkBox)
            cb_widget = QWidget()
            cb_widget.checkbox = checkBox

            cb_widget.checkState = checkBox.checkState
            cb_widget.setLayout(cb_layout)
            all_header_combobox.append(checkBox)


            serial_no = QTableWidgetItem()
            serial_no.setData(Qt.DisplayRole, row + 1)
            web_w = QTableWidgetItem(str(task_info['domain']))
            token_w = QTableWidgetItem(str(task_info['token']))
            num_w = QTableWidgetItem(str(task_info['num']))
            mobile_w = QTableWidgetItem('是') if task_info['mobile'] else QTableWidgetItem("否")
            start_time_w = QTableWidgetItem(str(task_info['start_time']))
            end_time_w = QTableWidgetItem(str(task_info['start_times']))
            time_w = QTableWidgetItem(str(datetime.datetime.fromtimestamp(int(task_info['time']))))
            self.tableWidget.setCellWidget(row, 0, cb_widget)
            self.tableWidget.setItem(row, 1, serial_no)
            self.tableWidget.setItem(row, 2, web_w)
            self.tableWidget.setItem(row, 3, token_w)
            self.tableWidget.setItem(row, 4, num_w)
            self.tableWidget.setItem(row, 5, mobile_w)
            self.tableWidget.setItem(row, 6, start_time_w)
            self.tableWidget.setItem(row, 7, end_time_w)
            self.tableWidget.setItem(row, 8, time_w)
            # self.tableWidget.setItem(row, 6, QTableWidgetItem(str(task_info['baidu_token'])))

            self.center(serial_no)
            self.center(web_w)
            self.center(token_w)
            self.center(num_w)
            self.center(mobile_w)
            self.center(start_time_w)
            self.center(end_time_w)
            self.center(time_w)
            # self.double_clicked_open_url(row, 2, task_info)

        self.tableWidget.headerBox.clicked.connect(lambda: self.tableWidget.change_state(all_header_combobox))  # 行表头复选框单击信号与槽

    def center(self, value):
        # font = QFont()
        # font.setFamily("微软雅黑")
        value.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)  # 对齐
        # value.setFont(font)

    # def double_clicked_open_url(self, row, column, task_info):
    #     self.tableWidget.cellDoubleClicked.connect(self.open_web_url)

    def open_web_url(self, row, column):
        print(11111111, row, column)
        if column == 2:
            web_url = self.tableWidget.item(row, column).text()

            webbrowser.open(web_url)

