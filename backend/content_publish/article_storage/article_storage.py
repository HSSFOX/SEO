import time
from PyQt5 import QtCore
from frontend.content_publish.article_storage.article_storage import Ui_Form
import requests
from backend.content_publish.article_storage.set_table import SetTable
from backend.content_publish.article_storage.table_insertion import TableInsertion
import os
from model.utils import content_publish_logger as my_logger
import random
import re
import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from collections import OrderedDict
import json
from PyQt5.QtNetwork import *
import webbrowser
import os
import logging
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from tools.backend_tools.ChromeDriverDownload import ChromeDriverDownloadDetect
from chromedriver_autoinstaller import install
# 检测Chrome浏览器版本并下载相应版本的ChromeDriver
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox"
os.environ['__GL_THREADED_OPTIMIZATIONS'] = '1'

class ArticleStorage(Ui_Form):
    def __init__(self, ui, parent_ui):
        super().__init__()
        self.setupUi(ui)
        self.ui = ui
        self.parent_ui = parent_ui
        self.page = 0
        self.max_page = 0
        self.row_limit = 100
        self.content_count = 0
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.tableWidget.action1 = QAction("修改")
        self.tableWidget.popup_menu.addAction(self.tableWidget.action1)
        SetTable(self.tableWidget, self.parent_ui.main_page).main()
        self.init_table_delete_button()
        self.chrome_view = SeleniumBrowser(self, self.parent_ui.main_page)
        # self.tableWidget.action2.setVisible(True)
        self.get_table_content_title()
        self.connect_slot()

    def get_table_content_title(self, turn_page=False):
        if not turn_page:
            self.page = 0
            self.max_page = 0
            self.update_labels()
        else:
            pass
        try:
            choose_cate_id = self.parent_ui.comboBox_6.currentIndex() + 1           # 栏目 or 域名
            cate_linkage_id = ''
            if choose_cate_id == 1:
                cate_index = self.parent_ui.comboBox.currentIndex()
                if cate_index >= 0:
                    cate_linkage_id = self.parent_ui.cate_l[cate_index]['linkageid']
            else:
                cate_index = self.parent_ui.comboBox_7.currentIndex()
                if cate_index >= 0:
                    cate_linkage_id = self.parent_ui.lanum_d_under_web[cate_index]['refer_id']
            url = f'{self.parent_ui.main_page.domain}/index.php?m=automatic&c=oauth&a=json_content&catid={choose_cate_id}&linkageid={cate_linkage_id}&page={self.page+1}'
            response = requests.get(url, headers=self.parent_ui.headers, cookies=self.parent_ui.cookies).json()
            self.content_l = response['content']
            self.content_count = int(response['number'])
        except Exception as e:
            my_logger.error(e)
            logging.error(e, exc_info=True)
        else:
            if response.get('status'):
                self.max_page = self.content_count // self.row_limit
                TableInsertion(self.tableWidget).table_2_main(self.content_l)
                self.update_labels()

    def init_table_delete_button(self):
        self.delete_action_button = QAction('删除', self.tableWidget)
        self.tableWidget.popup_menu.addAction(self.delete_action_button)

    def update_labels(self):
        if self.page == 0:
            self.pushButton_2.setEnabled(False)
        else:
            self.pushButton_2.setEnabled(True)
        if self.page == self.max_page:
            self.pushButton_3.setEnabled(False)
        else:
            self.pushButton_3.setEnabled(True)
        self.label_2.setText(f"当前第{self.page + 1}页")

    def next_page(self):
        self.page += 1
        self.get_table_content_title(turn_page=True)

    def prev_page(self):
        self.page -= 1
        self.get_table_content_title(turn_page=True)

    def connect_slot(self):
        self.pushButton.clicked.connect(self.get_table_content_title)
        self.pushButton_2.clicked.connect(self.prev_page)
        self.pushButton_3.clicked.connect(self.next_page)

        self.tableWidget.action1.triggered.connect(self.action_trigger)
        self.delete_action_button.triggered.connect(self.delete_action)
        self.tableWidget.itemDoubleClicked.connect(self.row_double_clicked)
        self.tableWidget.itemSelectionChanged.connect(self.current_select_row_changed)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:  # Qt.Key_Return 对应 Enter 键
            self.delete_action()

    def action_trigger(self):
        try:
            content_info = self.content_l[self.tableWidget.row]
            pc_hash = self.parent_ui.main_page.pc_hash
            self.load_article_edit_url(content_info)
        except Exception as e:
            my_logger.error(e)
            logging.error(e, exc_info=True)

    def delete_action(self):
        try:
            content_info = self.content_l[self.tableWidget.currentRow()]
            self.delete_article(content_info)
        except Exception as e:
            my_logger.error(e)
            logging.error(e, exc_info=True)

    def delete_article(self, content_info):
        reply = QMessageBox.question(QWidget(), '文章删除确认', '是否删除该文章？',
                                     QMessageBox.Yes| QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.confirm_delete(content_info)

    def confirm_delete(self, content_info):
        choose_cate_id = self.parent_ui.comboBox_6.currentIndex() + 1           # 栏目 或者 域名
        url = f'{self.parent_ui.main_page.domain}/index.php?m=content&c=content&a=delete&dosubmit=1&catid={choose_cate_id}&steps=0&json=1'
        id_v = content_info['url'].split("id=")[-1]
        params = {'ids[]': id_v, 'pc_hash': self.parent_ui.main_page.pc_hash}
        print(url, params)
        res = requests.post(url, headers=self.parent_ui.headers, cookies=self.parent_ui.cookies, data=params).json()
        print(res)
        if '操作成功' in res['msg']:
            self.parent_ui.main_page.return_msg_update(f"文章{content_info['title']}删除成功！")
            self.get_table_content_title()
        else:
            self.parent_ui.main_page.return_msg_update(f"文章{content_info['title']}删除失败！")

    def row_double_clicked(self):
        try:
            content_info = self.content_l[self.tableWidget.row]
            pc_hash = self.parent_ui.main_page.pc_hash
            self.load_article_view_url(content_info)
        except Exception as e:
            my_logger.error(e)
            print(str(e))

    def current_select_row_changed(self):
        # 获取当前选中的行，如果没有选中的行，返回-1
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            try:
                content_info = self.content_l[selected_row]
                print("content info: ", content_info)
                self.load_article_view_url(content_info)
            except Exception as e:
                my_logger.error(e)
                print(str(e))

    def cookies_convert(self, cookies_d):
        str_cookies = ""
        for k, v in cookies_d.items():
            str_cookies += f"{k}={v}; "
        return str_cookies

    def load_article_edit_url(self, content_info):
        try:
            pc_hash = self.parent_ui.main_page.pc_hash
            content_url = f'{self.parent_ui.main_page.domain}/' + content_info['edit'] + f'&pc_hash={pc_hash}'
            # for key, value in cookieDict.items():
            #     cookie = QNetworkCookie(QByteArray(key.encode()), QByteArray(value.encode()))
            #     # print(self.url,cookie,key,value)
            #     # self.parent_ui.webEngineView.page().profile().cookieStore().setCookie(cookie, QUrl(content_url))
            #     self.parent_ui.page.profile().cookieStore().setCookie(cookie, QUrl(content_url))
            # self.parent_ui.page.setUrl(QUrl(content_url))
            self.chrome_view.load_url(content_url)



        except Exception as e:
            logging.error(e, exc_info=True)

    def load_article_view_url(self, content_info):
        try:
            pc_hash = self.parent_ui.main_page.pc_hash
            content_url = f'{self.parent_ui.main_page.domain}' + content_info['url'] + f'&pc_hash={pc_hash}'
            print(content_url)
            # cookieDict = self.parent_ui.main_page.cookies
            self.chrome_view.load_url(content_url)
            # for key, value in cookieDict.items():
            #     cookie = QNetworkCookie(QByteArray(key.encode()), QByteArray(value.encode()))
            #     # print(self.url,cookie,key,value)
            #     self.parent_ui.webEngineView.page().profile().cookieStore().setCookie(cookie, QUrl(content_url))
            # self.parent_ui.page.setUrl(QUrl(content_url))
            # self.parent_ui.webEngineView.load(QUrl(content_url))


        except Exception as e:
            logging.error(e, exc_info=True)


class SeleniumBrowser:
    def __init__(self, ui, main_page):
        # 设置Chrome浏览器驱动程序的路径
        self.ui = ui
        self.main_page = main_page
        chrome_driver_path = "config/chromedriver-win64/chromedriver.exe"
        self.login_url = f'{main_page.domain}/index.php?m=admin&c=index&pc_hash={main_page.pc_hash}'
        self.login_sign = False
        if not os.path.exists(chrome_driver_path):
            self.main_page.return_msg_update("未检测到ChromeDriver控件，请稍等，正在为您下载...")
            self.ui.tableWidget.setEnabled(False)
            self.t_download_driver_by_chrome_version = ChromeInstallerThread()
            self.t_download_driver_by_chrome_version.start()
            self.t_download_driver_by_chrome_version.finished_trigger.connect(self.return_download_chrome)
            self.t_download_driver_by_chrome_version.msg_trigger.connect(self.main_page.return_msg_update)
        else:
            self.options = webdriver.ChromeOptions()
            self.options.add_experimental_option('detach', True)
            self.service = Service(os.path.abspath(chrome_driver_path))
            # print(os.path.abspath(chrome_driver_path))
            # self.browser = webdriver.Chrome(service=self.service, options=self.options)


    def load_url(self, url):
        try:
            if not self.login_sign:
                self.browser.get(self.login_url)
                for k, v in self.main_page.cookies.items():
                    self.browser.add_cookie({'name': k, 'value': v})
                self.login_sign = True
            self.browser.get(url)
            # time.sleep(5)
            # self.browser.quit()
        except Exception as e:
            self.browser = webdriver.Chrome(service=self.service, options=self.options)
            # self.browser = webdriver.Chrome(options=self.options)

            self.login_sign = False
            self.load_url(url)


    def return_download_chrome(self):
        self.main_page.return_msg_update("ChromeDriver控件下载完成，请重试！")
        self.ui.tableWidget.setEnabled(True)
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('detach', True)
        chrome_driver_path = "config/chromedriver-win64/chromedriver.exe"
        self.service = Service(os.path.abspath(chrome_driver_path))
        # print(os.path.abspath(chrome_driver_path))
        # self.browser = webdriver.Chrome(service=self.service, options=self.options)
        self.login_url = f'{self.main_page.domain}/index.php?m=admin&c=index&pc_hash={self.main_page.pc_hash}'
        self.login_sign = False


class ChromeInstallerThread(QThread):
    msg_trigger = pyqtSignal(str)
    finished_trigger = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        ChromeDriverDownloadDetect(self.msg_trigger).main()
        self.finished_trigger.emit()
        # path = install()
        # print("路径: ", path)
        # if not path:
        #     self.msg_trigger.emit("请确认本机器上已安装Chrome浏览器！")


