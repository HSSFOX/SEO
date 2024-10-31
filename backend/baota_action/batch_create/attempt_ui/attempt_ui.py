



from frontend.baota_action.batch_create.attempt_ui.attempt_ui import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from backend.baota_action.batch_create.attempt_ui.set_table import SetTable
from PyQt5.QtWidgets import *
import copy


class AttemptUI(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui, attempt_d):
        super(AttemptUI, self).__init__()
        self.setupUi(self)
        self.ui = ui
        self.attempt_d = attempt_d
        self.handy_close = False

        SetTable(self.tableWidget, self.ui.main_page).main()
        self.table_insert()

        self.pushButton.clicked.connect(self.re_attempt)


    def table_insert(self):
        self.tableWidget.setRowCount(len(self.attempt_d))
        for row, k in enumerate(self.attempt_d):
            item = self.attempt_d[k]
            serial_w = QTableWidgetItem(str(row + 1))
            web_name_w = QTableWidgetItem(str(item['web_data']['name']))
            stage_w = QTableWidgetItem(self.return_stage_string(item))
            self.add_delete_pushbutton(row, k)

            self.tableWidget.setItem(row, 0, serial_w)
            self.tableWidget.setItem(row, 1, web_name_w)
            self.tableWidget.setItem(row, 2, stage_w)

    def return_stage_string(self, item):
        s = ""
        for ele in item['stage_code']:
            if ele == '4':
                s += "静态规则添加&"
            if ele == '0':
                s += "后台栏目添加&"
            if ele == '1':
                s += "网站TDK配置&"
            if ele == '2':
                s += "域名备案配置&"
            if ele == '3':
                s += "后台域名配置&"

        return s.strip("&")

    def delete_item(self, row, item):
        self.tableWidget.hideRow(row)
        self.attempt_d.pop(item)

    def add_delete_pushbutton(self, row, item):
        action_w = QWidget()
        action_button = QPushButton("删除")
        action_button.setMinimumSize(100, 30)
        action_button.setMaximumSize(100, 30)
        action_layout = QHBoxLayout()
        action_layout.addWidget(action_button)
        action_w.setLayout(action_layout)
        action_button.clicked.connect(lambda: self.delete_item(copy.deepcopy(row), item))
        self.tableWidget.setCellWidget(row, 3, action_w)

    def re_attempt(self):
        self.handy_close = True
        self.close()
        self.ui.start_attempt(self.attempt_d)

    def closeEvent(self, event):
        if not self.handy_close:
            self.attempt_d = {}
            self.ui.start_attempt(self.attempt_d)
        event.accept()                      # 允许正常关闭



