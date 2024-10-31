from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from frontend.baota_action.baota_action import Ui_Form
from backend.baota_action.batch_create.batch_create import BatchCreate
from backend.baota_action.file_action.file_action import FileAction
from backend.baota_action.static_rules.static_rules import StaticRules
from backend.baota_action.SSL_setting.SSL_setting import SSLSetting
from backend.baota_action.redirection.redirection import Redirection
from backend.baota_action.ip_ban.ip_ban import IPBan
import requests
from api_requests.BtAPI import Bt
from api_requests.BtAPIv2 import BtV2
from model.utils import my_logger
import datetime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import re
import time
import logging
import configparser


class BaotaAction(Ui_Form):
    def __init__(self, page, main_page):
        super().setupUi(page)
        self.main_page = main_page

        self.page = page
        self.panel, self.key = '', ''
        self.baota_account_l = []
        self.current_ip = ''
        self.site_cate_l = []
        self.bt = None
        # 获取网站分类
        #
        # self.create_loading_label()
        # self.show_loading_label()
        # self.get_sites()
        # self.comboBox.setCurrentIndex(2)
        # self.get_cate_all_sites()

        self.bt_patch = 0
        self.current_bt_login_account = -1
        self.init_file_action = False
        self.init_static_rules = False
        self.init_SSL_setting = False
        self.init_redirection = False
        self.init_ip_ban = False
        self.batch_create = BatchCreate(self.tab, self, self.main_page)

        self.files_search_sign = False
        self.redirection_search_sign = False
        self.current_bt_cate_sites_info = None
        self.folder_l = []
        self.file_l = []
        self.bt_cate_sites_d = {}
        self.connect_slot()

    def update_files_check(self, dirs, files):
        if self.init_file_action:
            self.folder_l = dirs
            self.file_l = files

            self.file_action.create_page.comboBox.clear()
            self.file_action.create_page.comboBox.addItems([''] + dirs)

            self.file_action.upload_page.comboBox.clear()
            self.file_action.upload_page.comboBox.addItems([''] + dirs)

            self.file_action.rename_page.comboBox_2.clear()
            if self.file_action.rename_page.comboBox.currentIndex() == 0:
                self.file_action.rename_page.comboBox_2.addItems(dirs)
            else:
                self.file_action.rename_page.comboBox_2.addItems(files)

            self.file_action.access_page.comboBox.clear()
            self.file_action.access_page.comboBox.addItems(files)

            self.file_action.delete_page.comboBox_2.clear()
            if self.file_action.delete_page.comboBox.currentIndex() == 0:
                self.file_action.delete_page.comboBox_2.addItems(dirs)
            else:
                self.file_action.delete_page.comboBox_2.addItems(files)

            self.file_action.sub_page.comboBox.clear()
            self.file_action.sub_page.comboBox.addItems(files)

    def initializeTabContent(self, tab_index):
        if tab_index == 1:
            if not self.init_file_action:
                self.file_action = FileAction(self.tab_2, self, self.main_page)
                self.init_file_action = True
        elif tab_index == 2:
            if not self.init_static_rules:
                self.static_rules = StaticRules(self.tab_3, self, self.main_page)
                self.init_static_rules = True
        # elif tab_index == 3:
        #     if not self.init_SSL_setting:
        #         self.SSL_setting = SSLSetting(self.tab_4, self, self.main_page)
        #         self.init_SSL_setting = True
        elif tab_index == 3:
            if not self.init_redirection:
                self.redirection = Redirection(self.tab_5, self, self.main_page)
                self.init_redirection = True
        # elif tab_index == 5:
        #     if not self.init_ip_ban:
        #         self.ip_ban = IPBan(self.tab_6)
        #         self.init_ip_ban = True

    # def get_sites(self):            # 获取所有分类
    #     # get_site_cat
    #     self.all_cates = self.main_page.bt.get_site_cat()
    #     for i in self.all_cates:
    #         self.comboBox.addItem(i['name'])
    #
    # def get_cate_all_sites(self):           # 获取分类中所有网站
    #     current_index = self.comboBox.currentIndex()
    #     if current_index != -1:
    #         current_id = self.all_cates[current_index]
    #         params = {'page': 1, 'limit': 100, 'search': '', 'type': f'{current_id}', 'table': 'sites'}
    #         # res = self.main_page.bt.select_cat(params)
    #     else:
    #         self.main_page.bt_login = False
    #
    # def get_current_cate_sites(self):
    #     if self.comboBox.currentIndex() != -1:
    #         self.bt = Bt(self.panel, self.key)          # 应在登录宝塔后直接初始化
    #         res = self.bt.select_cat()

    def gain_bt_account_l(self):
        self.listWidget.clear()
        self.t_get_bt_account = GetBtAccount(self)
        self.t_get_bt_account.start()
        self.t_get_bt_account.msg_trigger.connect(self.main_page.return_msg_update)
        self.t_get_bt_account.finish_trigger.connect(self.return_get_bt_account)

    def return_get_bt_account(self, bt_account_l):
        self.bt_cate_sites_d = {}
        self.baota_account_l = bt_account_l
        for row, item in enumerate(self.baota_account_l):
            self.listWidget.addItem(QtWidgets.QListWidgetItem(str(item['names'])))
        self.main_page.bt_login = True

    def get_current_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def bt_login(self):
        self.t_bt_login = BaotaLogin(self)
        self.t_bt_login.start()
        self.t_bt_login.msg_trigger.connect(self.main_page.return_msg_update)
        self.t_bt_login.qmsg_trigger.connect(self.return_qmsg_trigger)
        self.t_bt_login.finish_trigger.connect(self.return_bt_login_finished)

    def return_qmsg_trigger(self, title, msg):
        QMessageBox.information(None, title, msg)

    def return_bt_login_finished(self, cate_list):
        self.bt_cate_sites_d = {}
        self.comboBox.clear()
        self.site_cate_l = cate_list
        if type(self.site_cate_l) is list:
            self.comboBox.addItems([str(ele['name']) for ele in self.site_cate_l])

    def connect_slot(self):
        self.tabWidget.currentChanged.connect(self.initializeTabContent)
        self.comboBox.currentIndexChanged.connect(self.update_folder_search_sign)
        self.listWidget.doubleClicked.connect(self.bt_login)
        self.pushButton.clicked.connect(self.gain_bt_account_l)
        # self.pushButton_3.clicked.connect(self.reset_key)
        self.radioButton.toggled.connect(self.bt_patch_change_rb1)
        self.radioButton_2.toggled.connect(self.bt_patch_change_rb2)
        self.checkBox.toggled.connect(self.bt_proxy_change_cb)

    def bt_patch_change_rb1(self):
        if self.radioButton.isChecked():
            self.bt_patch = 0
            self.main_page.bt_patch = 0
            self.checkBox.setChecked(False)
        else:
            if not self.radioButton_2.isChecked():
                self.radioButton.setChecked(True)
                self.checkBox.setChecked(False)
                self.bt_patch = 0
                self.main_page.bt_patch = 0
                self.bt_sign = False
                self.main_page.return_msg_update("宝塔面板已切换 请重新登录！")

    def bt_patch_change_rb2(self):
        if self.radioButton_2.isChecked():
            self.bt_patch = 1
            self.main_page.bt_patch = 1
        else:
            if not self.radioButton.isChecked():
                self.radioButton_2.setChecked(True)
                self.bt_patch = 1
                self.main_page.bt_patch = 1
                self.bt_sign = False
                self.main_page.return_msg_update("宝塔面板已切换 请重新登录！")

    def bt_proxy_change_cb(self):
        if self.checkBox.isChecked():
            self.radioButton_2.setChecked(True)
        if self.radioButton_2.isChecked():
            self.main_page.bt_sign = False
            self.main_page.return_msg_update("代理选项已切换 请重新登录！")


    def update_folder_search_sign(self):
        self.files_search_sign = False
        # self.redirection_search_sign = False
        if self.comboBox.currentIndex() != -1:
            self.file_actions_toggled()
            self.redirect_actions_toggled()

    def redirect_actions_toggled(self):
        if self.init_redirection:
            self.redirection.tableWidget.clearContents()
            self.redirection.tableWidget.setRowCount(0)
            self.redirection.comboBox.setCurrentIndex(-1)
            self.redirection.comboBox_2.setCurrentIndex(-1)
            self.redirection.comboBox_3.clear()

    def file_actions_toggled(self):         # 当comboBox变化时, file_actions的改动
        cate_index = self.comboBox.currentIndex()
        site_cate_info = self.site_cate_l[cate_index]
        bt_cate_id = site_cate_info['id']
        self.current_bt_cate_sites_info = None
        if not self.bt_cate_sites_d.get(bt_cate_id):  # 仅没获取的时候去拿
            self.t_get_bt_cate_sites = GetBtCateSites(self, bt_cate_id)
            self.t_get_bt_cate_sites.start()
            self.t_get_bt_cate_sites.msg_trigger.connect(self.main_page.return_msg_update)
            self.t_get_bt_cate_sites.finished_trigger.connect(self.return_t_get_bt_cate_sites)
        else:
            self.current_bt_cate_sites_info = self.bt_cate_sites_d.get(bt_cate_id)

    def return_t_get_bt_cate_sites(self, sites_info_d):
        self.bt_cate_sites_d.update(sites_info_d)
        self.current_bt_cate_sites_info = list(sites_info_d.values())[0]


class BaotaLogin(QThread):
    msg_trigger = pyqtSignal(str)
    finish_trigger = pyqtSignal(list)
    qmsg_trigger = pyqtSignal(str, str)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        row = self.ui.listWidget.currentRow()
        account_info = self.ui.baota_account_l[row]
        url = account_info['url'].replace('//', "|").split("/")[0].replace("|", "//")       # 完美绕后！
        panel, key = url, account_info['key']
        print(44444444, self.ui.radioButton.isChecked())
        if self.ui.checkBox.isChecked():
            status, proxy_type, proxy = self.read_proxy()
            if not status:
                self.qmsg_trigger.emit('错误提示', f'请先配置代理！')
                self.msg_trigger.emit(f'"请先配置代理！"')
                return
        else:
            proxy = None
        print(proxy)


        if self.ui.radioButton.isChecked():
            self.ui.bt = Bt(panel, key)
        else:
            self.ui.bt = BtV2(panel, key, proxy)
        self.ui.main_page.bt = self.ui.bt
        self.ui.main_page.bt_sign = True           # yes i am bt
        try:
            bt_info = self.ui.bt.get_public_config()
            print(bt_info)
        except Exception as e:
            my_logger.error(e)
        else:
            if bt_info.get('error'):
                self.msg_trigger.emit('无法访问！')
                # self.main_page.return_msg_update('无法访问！')
            else:
                if not bt_info.get('status'):
                    self.qmsg_trigger.emit('宝塔配置', f'{bt_info["msg"]} ！请手动添加本机IP入白名单')
                    self.msg_trigger.emit(f'{bt_info["msg"]} ！请手动添加本机IP入白名单')
                else:
                    self.msg_trigger.emit(f'{account_info["names"]} 登录成功！')
        try:
            site_cate_l = self.ui.main_page.bt.get_site_cat()
            if self.ui.bt_patch:        # 宝塔英文版v2更新
                if site_cate_l.get('status'):
                    site_cate_l = site_cate_l['message']

            print(2222, site_cate_l)
            self.finish_trigger.emit(site_cate_l)
        except Exception as e:
            my_logger.error(e)
            self.msg_trigger.emit(f'{account_info["names"]} 登录失败！请检查此服务器是否可用！')

    def read_proxy(self):
        config = configparser.ConfigParser()
        try:
            config.read('config/config.ini')  # 读取 config.ini 文件
            if config.has_section('Proxy'):
                proxy_type = config.get('Proxy', 'type')
                host = config.get('Proxy', 'host')
                port = config.get('Proxy', 'port')
                username = config.get('Proxy', 'username')
                password = config.get('Proxy', 'password')
                if proxy_type == 'http':
                    if username and password:
                        proxies = {
                            "http": f"http://{username}:{password}@{host}:{port}",
                            "https": f"http://{username}:{password}@{host}:{port}",
                        }
                    else:
                        proxies = {
                            "http": f"http://{host}:{port}",
                            "https": f"http://{host}:{port}",
                        }
                    return True, 'http', proxies
                elif proxy_type == 'socks':
                    if username and password:
                        proxies = {
                            "http": f"socks5://{username}:{password}@{host}:{port}",
                            "https": f"socks5://{username}:{password}@{host}:{port}",
                        }
                    else:
                        proxies = {
                            "http": f"socks5://{host}:{port}",
                            "https": f"socks5://{host}:{port}",
                        }
                    return True, 'socks', proxies
                else:
                    return False, '', None
            else:
                return False, '', None
        except Exception as e:
            logging.error(e, exc_info=True)
            return False, '', None


class GetBtAccount(QThread):
    msg_trigger = pyqtSignal(str)
    finish_trigger = pyqtSignal(list)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        url = f'{self.ui.main_page.domain}/?m=bt&c=oauth&a=list_json'
        try:
            baota_account_l = requests.get(url, headers=self.ui.main_page.headers,
                                                cookies=self.ui.main_page.cookies).json()
            print(baota_account_l)
        except Exception as e:
            my_logger.error(e)
            self.msg_trigger.emit("无法连接至服务器，请检查网络连接！")
        else:
            self.finish_trigger.emit(baota_account_l)


class GetBtCateSites(QThread):
    msg_trigger = pyqtSignal(str)
    finished_trigger = pyqtSignal(dict)

    def __init__(self, ui, bt_cate_id):
        super().__init__()
        self.ui = ui
        self.bt_cate_id = bt_cate_id

    def run(self):
        try:
            response = self.ui.main_page.bt.select_cat({'type': self.bt_cate_id})
            print(response)
        except Exception as e:
            logging.error(e, exc_info=True)
        else:
            if not response.get('data'):
                self.msg_trigger.emit("该分类下无网站！")
            else:
                self.finished_trigger.emit({self.bt_cate_id: response['data']})