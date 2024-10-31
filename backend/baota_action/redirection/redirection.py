from frontend.baota_action.redirection.redirection import Ui_Form
from tools.frontend_tools.LineEditValidator import FixedPartValidator
from PyQt5.QtCore import *
import requests
import logging
from backend.baota_action.redirection.set_table import SetTable
from PyQt5.QtWidgets import *
import tldextract
import time
import json


class Redirection(Ui_Form):
    def __init__(self, page, parent_ui, main_page):
        super().setupUi(page)
        self.page = page
        self.parent_ui = parent_ui
        self.main_page = main_page
        # self.lineEdit_2.setValidator(FixedPartValidator(['http://', 'https://']))
        self.lineEdit_2.setText('http://')
        SetTable(self.tableWidget, self.tableWidget_2, self.main_page).main()
        self.connect_slot()

    def search_redirection_list(self):
        if self.main_page.bt_sign:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
            if self.parent_ui.current_bt_cate_sites_info:
                if not self.parent_ui.files_search_sign:  # 仅没搜索过的情况下去再搜索一遍，分类更变后重置
                    print(99999999, self.parent_ui.current_bt_cate_sites_info)
                    self.get_redirection_list()
                    # self.default_path = self.parent_ui.current_bt_cate_sites_info[0]['path']
                    # self.get_redirection_list()
                else:
                    self.main_page.return_msg_update('分类已切换！请重新搜索！')
            else:
                self.main_page.return_msg_update('该分类下无网站！')
        else:
            self.main_page.return_msg_update('请先登录宝塔！')

    def get_redirection_list(self):
        self.pushButton_2.setText("获取中...")
        self.pushButton_2.setEnabled(False)
        self.main_page.return_msg_update("搜索该分类下域名重定向完毕！")
        self.t_get_redirection_list = GetRedirectionListThread(self, self.main_page, self.parent_ui.current_bt_cate_sites_info)
        self.t_get_redirection_list.start()
        self.t_get_redirection_list.finished_trigger.connect(self.return_redirection_list)
        self.t_get_redirection_list.msg_trigger.connect(self.main_page.return_msg_update)

    def return_redirection_list(self, redirection_list, domain_refer_d):
        self.redirection_list = redirection_list
        self.domain_site_refer_d = domain_refer_d

        print(111111111, self.redirection_list)
        print(222222222, self.domain_site_refer_d)
        self.pushButton_2.setText("刷新")
        self.pushButton_2.setEnabled(True)
        self.update_available_domain_format()
        self.table_insertion_1()
        self.table_insertion_2()

    def table_insertion_1(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(self.redirection_list))
        for row, redirection_info in enumerate(self.redirection_list):
            redirect_urls_w = QTableWidgetItem(','.join(redirection_info['redirectdomain']))
            if redirection_info['domainorpath'] == 'domain':
                to_url_path_w = QTableWidgetItem(redirection_info['tourl'])
                redirect_type_w = QTableWidgetItem('域名')
            else:
                to_url_path_w = QTableWidgetItem(redirection_info['redirectpath'])
                redirect_type_w = QTableWidgetItem('路径')
            redirection_way_w = QTableWidgetItem(redirection_info['redirecttype'])

            self.tableWidget.setItem(row, 0, redirect_urls_w)
            self.tableWidget.setItem(row, 1, redirect_type_w)
            self.tableWidget.setItem(row, 2, redirection_way_w)
            self.tableWidget.setItem(row, 3, to_url_path_w)

            self.center(redirect_urls_w)
            self.center(to_url_path_w)
            self.center(redirect_type_w)
            self.center(redirection_way_w)


    def table_insertion_2(self):
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.clearContents()
        self.tableWidget_2.setRowCount(len(self.domain_site_refer_d))
        row = 0
        for domain, sub_domain_l in self.domain_site_refer_d.items():
            row_w = QTableWidgetItem()
            row_w.setData(Qt.DisplayRole, row + 1)
            domain_w = QTableWidgetItem(domain)
            sub_domain_w = QTableWidgetItem(','.join(sub_domain_l))
            self.tableWidget_2.setItem(row, 0, row_w)
            self.tableWidget_2.setItem(row, 1, domain_w)
            self.tableWidget_2.setItem(row, 2, sub_domain_w)

            self.center(row_w)
            self.center(domain_w)
            self.center(sub_domain_w)
            row += 1


    def update_available_domain_format(self):
        self.comboBox_3.clear()
        domain_url_l = []
        format_url_l = []
        for k, v in self.domain_site_refer_d.items():
            domain_url_l += v
        # for ele in self.parent_ui.current_bt_cate_sites_info:
        #     domain_url_l += [ele['name']]
        # print(777777777777777, domain_url_l)
        for url in domain_url_l:
            extracted = tldextract.extract(url)
            format_url = f'{extracted.subdomain}._.{extracted.suffix}'.strip('.')          # 如果没有subdomain, 前边儿就不会有'.'
            if format_url not in format_url_l:
                format_url_l.append(format_url)
        print(77777777, format_url_l)
        self.comboBox_3.addItems(format_url_l)

    def center(self, value):
        # font = QFont()
        # font.setFamily("微软雅黑")
        value.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)  # 对齐
        # value.setFont(font)

    def connect_slot(self):
        self.pushButton.clicked.connect(self.add_redirection)
        self.pushButton_2.clicked.connect(self.search_redirection_list)


    def add_redirection(self):
        if self.main_page.bt_sign:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
            if self.parent_ui.current_bt_cate_sites_info:
                if not self.parent_ui.files_search_sign:  # 仅没搜索过的情况下去再搜索一遍，分类更变后重置
                    print(self.parent_ui.current_bt_cate_sites_info)
                    self.t_create_redirection = CreateRedirectionThread(self)
                    self.t_create_redirection.start()
                    self.t_create_redirection.msg_trigger.connect(self.main_page.return_msg_update)
                    # self.get_redirection_list()
                    # self.default_path = self.parent_ui.current_bt_cate_sites_info[0]['path']
                    # self.get_redirection_list()
                else:
                    self.main_page.return_msg_update('分类已切换！请重新搜索！')
            else:
                self.main_page.return_msg_update('该分类下无网站！')
        else:
            self.main_page.return_msg_update('请先登录宝塔！')

    # def get_params(self):

        # default_params = {'type': 1, 'holdpath': 1, 'domainorpath': '', 'redirecttype': 301, 'tourl': '',
        # 'redirectdomain': [], 'sitename': '', 'redirectname': int(time.time() * 1000)}
        # target_format = self.comboBox_3.currentText()
        # redirect_type = 301 if self.comboBox_2.currentIndex() else 302
        # if self.comboBox.currentIndex() == 0:
        # for site_info in self.parent_ui.current_bt_cate_sites_info:



class CreateRedirectionThread(QThread):
    msg_trigger = pyqtSignal(str)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        domains_d = self.get_pid_id()
        format_url = self.ui.comboBox_3.currentText()
        requests_url_d = self.get_requests_url_list(format_url, domains_d)
        domain_or_path = 'path' if self.ui.comboBox.currentIndex() else 'domain'
        redirect_type = '302' if self.ui.comboBox_2.currentIndex() else '301'
        target_url = self.ui.lineEdit_2.text()
        print(111111111, requests_url_d)
        for domain, url in requests_url_d.items():

            domain_target_url = target_url.replace("_", tldextract.extract(url).domain)
            params = {'type': 1, 'holdpath': 1, 'domainorpath': domain_or_path, 'redirecttype': redirect_type, 'tourl': domain_target_url,
                      'redirectdomain': json.dumps([url]), 'sitename': domain, 'redirectpath': ''}
            try:
                res = self.ui.main_page.bt.create_redirection_list(params)
                print(22222222, res)
            except Exception as e:
                logging.error(e, exc_info=True)
            else:
                if res.get('status'):
                    msg = f'{domain} 添加重定向规则成功！{url} -> {domain_target_url}'
                    self.msg_trigger.emit(msg)
                else:
                    self.msg_trigger.emit(f'{domain} 添加重定向规则失败！{res["msg"]}')

    def get_requests_url_list(self, format_url, domains_d):
        requests_url_l = {}
        for domain in domains_d:
            for url in domains_d[domain]:
                print(444444444, domain, url)
                extracted = tldextract.extract(url)
                print(5555, format_url, extracted.subdomain, extracted.suffix)
                if format_url == f'{extracted.subdomain}._.{extracted.suffix}'.strip("."):
                    requests_url_l[domain] = url
        return requests_url_l

    def get_pid_id(self):           # 获取这个域名id下的所有domains
        domains_l = {}
        for site_info in self.ui.parent_ui.current_bt_cate_sites_info:
            for _ in range(3):
                try:
                    pid_id = site_info['id']
                    site_name = site_info['name']
                    res = self.ui.main_page.bt.get_db_data({'table': 'domain', 'list': True, 'search': pid_id})
                except Exception as e:
                    logging.error(e, exc_info=True)
                else:
                    domains_l[site_name] = [ele['name'] for ele in res['message']]
                    break
        print(domains_l)
        return domains_l


class GetRedirectionListThread(QThread):
    msg_trigger = pyqtSignal(str)
    finished_trigger = pyqtSignal(list, dict)

    def __init__(self, ui, main_page, bt_cate_site_info):
        super().__init__()
        self.ui = ui
        self.main_page = main_page
        self.bt_cate_site_info = bt_cate_site_info
        self.return_redirection_list = []

    def run(self):
        for site_info in self.bt_cate_site_info:
            for _ in range(3):
                try:
                    site_redirection_res = self.main_page.bt.get_redirection_list({'sitename': site_info['name']})
                    print(8888888888, site_redirection_res)
                except Exception as e:
                    logging.error(e, exc_info=True)
                else:
                    print(site_redirection_res)
                    if self.main_page.bt_patch:
                        self.return_redirection_list += site_redirection_res['message']
                    else:
                        self.return_redirection_list += site_redirection_res
                    break
            else:
                self.msg_trigger.emit(f'{site_info["name"]}获取重定向列表失败！')
        domain_l = self.get_pid_id()
        self.finished_trigger.emit(self.return_redirection_list, domain_l)

    def get_pid_id(self):           # 获取这个域名id下的所有domains
        domains_l = {}
        for site_info in self.ui.parent_ui.current_bt_cate_sites_info:
            for _ in range(3):
                try:
                    pid_id = site_info['id']
                    site_name = site_info['name']
                    res = self.ui.main_page.bt.get_db_data({'table': 'domain', 'list': True, 'search': pid_id})
                    print(3333333333, res)
                except Exception as e:
                    logging.error(e, exc_info=True)
                else:
                    if self.main_page.bt_patch:
                        domains_l[site_name] = [ele['name'] for ele in res['message']]
                    else:
                        domains_l[site_name] = [ele['name'] for ele in res]
                    break
        print(domains_l)
        return domains_l