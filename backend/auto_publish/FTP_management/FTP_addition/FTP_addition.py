
from frontend.auto_publish.FTP_management.FTP_addition.FTP_addition import Ui_Form
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests
import tldextract
import re
import logging
import datetime
import collections


class FtpAddition(QWidget, Ui_Form):
    def __init__(self, ui, ftp_info):
        super().__init__()
        self.setupUi(self)
        self.ui = ui
        self.main_page = self.ui.main_page
        self.ftp_info = ftp_info
        self.default_value()
        self.updated_sign = False
        self.connect_slot()

    def default_value(self):
        self.dateEdit.setMinimumDate(QDate(2024, 9, 4))
        self.dateEdit.setMaximumDate(QDate.currentDate())
        self.dateEdit.setDate(QDate.currentDate())

        subdomains_l = []
        ori_domain_l = self.ftp_info['analyzed'].split("\n")
        for ori_domain in ori_domain_l:
            web_subdomain = tldextract.extract(ori_domain).subdomain
            if web_subdomain and "//" + web_subdomain + "." not in subdomains_l:
                subdomains_l.append("//" + web_subdomain + ".")
        self.comboBox.addItems(subdomains_l)

    def confirm(self):
        domain_lines = self.textEdit.toPlainText()
        addition_date = self.dateEdit.date().toPyDate().strftime("%Y年%m月%d日")
        if domain_lines:
            ori_domain_d = self.get_exist_info()

            domain_l = domain_lines.split('\n')
            for domain in domain_l:
                domain_web = tldextract.extract(domain).registered_domain
                sub_domain = tldextract.extract(domain).subdomain
                if domain_web:
                    if ("//img." + domain_web in self.ftp_info['analyzed'] or domain_web in self.ftp_info['analyzed'] or
                            self.comboBox.currentText() + domain_web in self.ftp_info['analyzed']) or sub_domain + "." + domain_web in self.ftp_info['analyzed']:
                        self.ui.main_page.return_msg_update("域名: " + domain_web + ", 该域名已存在.")
                    else:
                        self.updated_sign = True
                        ori_domain_d = self.check_and_append(sub_domain, domain_web, ori_domain_d, '--------------' + addition_date + '--------------')
            if self.updated_sign:
                update_domain = self.assemble_domain_d(ori_domain_d)
                self.ftp_addition_thread = FtpAdditionThread(self, self.get_update_info(update_domain))
                self.ftp_addition_thread.msg_trigger.connect(self.ui.main_page.return_msg_update)
                self.ftp_addition_thread.start()
                self.ftp_addition_thread.finished.connect(self.return_finished_update)
            else:
                self.close()
        else:
            self.close()

    def return_finished_update(self):
        self.close()
        self.ui.search_all()

    def assemble_domain_d(self, ori_domain_d):            # 超兽武装！合体！
        assemble_str = ''
        for k in ori_domain_d:
            assemble_str += k + "\n"
            for v in ori_domain_d[k]:
                assemble_str += v + "\n"
        return assemble_str.strip()

    def check_and_append(self, sub_domain, domain_web, ori_domain_d, addition_date):
        if sub_domain:
            confirmed_domain = "//" + sub_domain + "." + domain_web
        else:
            confirmed_domain = self.comboBox.currentText() + domain_web
        if addition_date in ori_domain_d:
            ori_domain_d[addition_date].append(confirmed_domain)
        else:
            ori_domain_d[addition_date] = [confirmed_domain]
        return ori_domain_d

    def get_exist_info(self):
        ori_domain_l = self.ftp_info['analyzed'].split("\n")
        ori_domain_d = collections.OrderedDict()
        current_date = ''
        for ori_domain in ori_domain_l:
            domain_web = tldextract.extract(ori_domain).registered_domain
            if not domain_web:      # 日期
                current_date = ori_domain
                ori_domain_d[current_date] = []
            else:
                ori_domain_d[current_date].append(ori_domain)
        return ori_domain_d

    def connect_slot(self):
        self.pushButton.clicked.connect(self.confirm)


    def get_date_str(self, format_string):
        pattern = re.compile(r'(?<=--------------).*?(?=--------------)')
        matches = re.findall(pattern, format_string)
        if matches:
            return matches[0]

    def get_update_info(self, update_domain):
        ftp_d = {}
        ftp_d['data[ftp_enable]'] = self.ftp_info['ftp_enable']
        ftp_d['data[ftp_pasv]'] = self.ftp_info['ftp_pasv']
        ftp_d['data[ftp_host]'] = self.ftp_info['ftp_host']
        ftp_d['data[ftp_user]'] = self.ftp_info['ftp_user']
        ftp_d['data[ftp_password]'] = self.ftp_info['ftp_password']
        ftp_d['data[ftp_port]'] = self.ftp_info['ftp_port']
        ftp_d['data[ftp_path]'] = self.ftp_info['ftp_path']
        ftp_d['data[analyzed]'] = update_domain
        return ftp_d


class FtpAdditionThread(QThread):
    msg_trigger = pyqtSignal(str)

    def __init__(self, ui, ftp_info):
        super().__init__()
        self.ui = ui
        self.ftp_info = ftp_info

    def run(self):
        try:
            url = f"{self.ui.main_page.domain}/index.php?m=automatic&c=automatic_admin&a=RDS_edit&id={self.ui.ftp_info['id']}&json=1"
            params = {'dosubmit': '', 'pc_hash': self.ui.main_page.pc_hash}
            params.update(self.ftp_info)
            res = requests.post(url, headers=self.ui.main_page.headers, cookies=self.ui.main_page.cookies, data=params).json()
            if "成功" in res['msg']:
                self.msg_trigger.emit("添加成功！")
            else:
                self.msg_trigger.emit(res['msg'])
        except Exception as e:
            logging.error(e, exc_info=True)
            self.msg_trigger.emit("添加失败，请检查网络连接！")