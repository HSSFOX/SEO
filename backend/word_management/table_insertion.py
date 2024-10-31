


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class TableInsertion:
    def __init__(self, tableWidget):
        self.tableWidget = tableWidget

    def table_main(self, task_info_l):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(task_info_l))
        all_header_combobox = []
        for row, task_info in enumerate(task_info_l):
            self.tableWidget.setRowHeight(row, 60)
            checkBox = QCheckBox()
            checkBox.setCheckState(Qt.Unchecked)
            cb_layout = QHBoxLayout()
            cb_layout.addWidget(checkBox)
            cb_widget = QWidget()
            cb_widget.checkbox = checkBox

            cb_widget.checkState = checkBox.checkState
            cb_widget.setLayout(cb_layout)
            all_header_combobox.append(checkBox)
            serial_no_w = QTableWidgetItem(str(row + 1))
            keyword_w = QTableWidgetItem(str(task_info['keyword']))
            pinqyin_w = QTableWidgetItem(str(task_info['pinyin']))
            long_tail_w = QTableWidgetItem('')
            if task_info['typeid'] == '54':
                cate_w = QTableWidgetItem("主关键词")
            elif task_info['typeid'] == '59':
                cate_w = QTableWidgetItem("长尾词")
            else:
                cate_w = QTableWidgetItem("主关键词")
            add_time_w = QTableWidgetItem(str(datetime.datetime.fromtimestamp(int(task_info['addtime']))))
            self.tableWidget.setCellWidget(row, 0, cb_widget)
            self.tableWidget.setItem(row, 1, serial_no_w)
            self.tableWidget.setItem(row, 2, keyword_w)
            self.tableWidget.setItem(row, 3, pinqyin_w)
            self.tableWidget.setItem(row, 4, long_tail_w)
            self.tableWidget.setItem(row, 5, cate_w)
            self.tableWidget.setItem(row, 6, add_time_w)

            self.center(serial_no_w)
            self.center(keyword_w)
            self.center(pinqyin_w)
            self.center(long_tail_w)
            self.center(cate_w)
            self.center(add_time_w)

        self.tableWidget.headerBox.clicked.connect(lambda: self.tableWidget.change_state(all_header_combobox))  # 行表头复选框单击信号与槽

    def center(self, value):
        # font = QFont()
        # font.setFamily("微软雅黑")
        value.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)  # 对齐
        # value.setFont(font)