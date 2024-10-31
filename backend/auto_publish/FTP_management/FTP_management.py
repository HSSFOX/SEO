

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from frontend.auto_publish.FTP_management.FTP_management import Ui_Form
from backend.auto_publish.FTP_management.set_table import SetTable
from backend.auto_publish.FTP_management.FTP_setting.FTP_setting import FtpSetting
from backend.auto_publish.FTP_management.FTP_addition.FTP_addition import FtpAddition
import datetime
import requests
import logging
import json
import tldextract
import re



class FTP_management(Ui_Form):
    def __init__(self, ui, parent_ui, main_page):
        super(FTP_management, self).__init__()
        self.setupUi(ui)
        self.ui = ui
        self.parent_ui = parent_ui
        self.main_page = main_page
        SetTable(self.tableWidget, self.main_page).main()
        self.tableWidget.action1 = QAction("修改FTP设置")
        self.tableWidget.popup_menu.addAction(self.tableWidget.action1)
        self.tableWidget.action2 = QAction("添加域名")
        self.tableWidget.popup_menu.addAction(self.tableWidget.action2)
        # self.set_default_value()
        self.connect_slot()

    # def set_default_value(self):
    #     today = datetime.datetime.today().date()
    #     self.dateEdit.setDate(QDate(2024, 9, 1))                # 设置日历默认时间
    #     self.dateEdit_2.setDate(QDate(today.year, today.month, today.day))
    #     self.dateEdit.setMaximumDate(QDate(today.year, today.month, today.day))         # 设置日历最高及最低时间
    #     self.dateEdit_2.setMaximumDate(QDate(today.year, today.month, today.day))
    #     self.dateEdit.setMinimumDate(QDate(2024, 9, 1))
    #     self.dateEdit_2.setMinimumDate(QDate(2024, 9, 1))

    def search_all(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()

        self.t_ftp = GetFtpInfoThread(self)
        self.t_ftp.start()
        self.t_ftp.msg_trigger.connect(self.main_page.return_msg_update)
        self.t_ftp.finished_trigger.connect(self.search)

    def search(self, ftp_l):
        print(ftp_l)
        self.ftp_l = ftp_l
        # self.ftp_l = self.ftp_list_convert(ftp_l)
        # print(self.ftp_l)
        # search_text = self.lineEdit.text()
        # search_lower_date = int(self.dateEdit.dateTime().toPyDateTime().timestamp()) * 1000
        # search_upper_date = int((self.dateEdit_2.dateTime().toPyDateTime() + datetime.timedelta(days=1)).timestamp()) * 1000
        # insert_l = []
        # for ele in self.ftp_l:
        #     if search_lower_date <= ele['date'] < search_upper_date:
        #         if search_text:
        #             if search_text in ele['id'] or search_text in ele['domain']or search_text in ele['ftp_host']:
        #                 insert_l.append(ele)
        #         else:
        #             insert_l.append(ele)
        self.table_insertion(ftp_l)

    def open_ftp_setting(self, add=False):
        if not add:
            row = self.tableWidget.currentRow()
            if row != -1:
                ftp_setting_info = self.ftp_l[row]
                self.ftp_setting_ui = FtpSetting(self, ftp_setting_info, add)
                self.ftp_setting_ui.show()
        else:
            ftp_setting_info = {}
            self.ftp_setting_ui = FtpSetting(self, ftp_setting_info, add)
            self.ftp_setting_ui.show()


    def table_insertion(self, insert_l):
        self.tableWidget.setRowCount(len(insert_l))
        for i, ele in enumerate(insert_l):
            # serial_no_w = QTableWidgetItem(str(i + 1))
            site_id_w = QTableWidgetItem(ele['id'])
            # ftp_enable_w = QTableWidgetItem(ele['ftp_enable'])
            ftp_host_w = QTableWidgetItem(ele['ftp_host'])
            # ftp_user_w = QTableWidgetItem(ele['ftp_user'])
            # ftp_password_w = QTableWidgetItem(ele['ftp_password'].replace(ele['ftp_password'][:-4], '*'*len(ele['ftp_password'][:-4])))
            # ftp_dir_w = QTableWidgetItem(ele['ftp_path'])
            # domain_w = QTableWidgetItem(ele['domain'])
            # domain_w = QTableWidgetItem(ele['analyzed'])
            # ftp_date_w = QTableWidgetItem(str(datetime.datetime.fromtimestamp(ele['date'] / 1000).date()))

            # self.tableWidget.setItem(i, 0, serial_no_w)
            self.tableWidget.setItem(i, 0, site_id_w)
            # self.tableWidget.setItem(i, 2, ftp_enable_w)
            self.tableWidget.setItem(i, 1, ftp_host_w)
            # self.tableWidget.setItem(i, 4, ftp_user_w)
            # self.tableWidget.setItem(i, 5, ftp_password_w)
            # self.tableWidget.setItem(i, 6, ftp_dir_w)
            # self.tableWidget.setItem(i, 1, domain_w)
            # self.tableWidget.setItem(i, 2, ftp_date_w)

            # self.center(serial_no_w)
            self.center(site_id_w)
            # self.center(ftp_enable_w)
            self.center(ftp_host_w)
            # self.center(ftp_user_w)
            # self.center(ftp_password_w)
            # self.center(ftp_dir_w)
            # self.center(domain_w)
            # self.center(ftp_date_w)

    def center(self, value):
        # font = QFont()
        # font.setFamily("微软雅黑")
        value.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)  # 对齐
        # value.setFont(font)

    def ftp_list_convert(self, ftp_l):
        l = []
        for ftp_info in ftp_l:
            date_timestamp = 0
            for domain in ftp_info['analyzed'].split("\n"):
                d = {}
                d.update(ftp_info)
                d.pop('analyzed', None)
                domain_web = tldextract.extract(domain).registered_domain
                if not domain_web:
                    date_timestamp = self.get_date_str(domain)
                if domain_web:
                    d['domain'] = domain
                    d['date'] = date_timestamp
                    l.append(d)
        return l

    def get_date_str(self, format_string):
        pattern = re.compile(r'(?<=--------------).*?(?=--------------)')
        matches = re.findall(pattern, format_string)
        if matches:
            return int(datetime.datetime.strptime(matches[0], "%Y年%m月%d日").timestamp() * 1000)
        else:
            return 0

    def get_remote_ftp(self):
        url = f'{self.parent_ui.main_page.domain}/index.php?m=automatic&c=oauth&a=json_RDS'
        try:
            self.ftp_l = requests.get(url).json()
            print("ftp_l", self.ftp_l)
        except Exception as e:
            logging.error(e, exc_info=True)
            self.ftp_l = []
        finally:
            self.comboBox.addItems([''] + [i['id'] for i in self.ftp_l])

    def connect_slot(self):
        self.pushButton.clicked.connect(self.search_all)
        self.pushButton_2.clicked.connect(lambda: self.open_ftp_setting(add=True))
        self.tableWidget.action1.triggered.connect(self.open_ftp_setting)
        self.tableWidget.action2.triggered.connect(self.add_domain)

    def add_domain(self):
        row = self.tableWidget.currentRow()
        if row != -1:
            ftp_setting_info = self.ftp_l[row]
            print(row, ftp_setting_info)
            self.ftp_addition_ui = FtpAddition(self, ftp_setting_info)
            self.ftp_addition_ui.show()


class GetFtpInfoThread(QThread):
    msg_trigger = pyqtSignal(str)
    finished_trigger = pyqtSignal(list)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.main_page = self.ui.main_page

    def run(self):
        url = f'{self.main_page.domain}/index.php?m=automatic&c=oauth&a=json_RDS'
        try:
            ftp_l = requests.get(url).json()
        except Exception as e:
            logging.error(e, exc_info=True)
            ftp_l = []
            self.msg_trigger.emit("获取FTP设置失败！请检查后台以及网络！")
        self.finished_trigger.emit(ftp_l)










