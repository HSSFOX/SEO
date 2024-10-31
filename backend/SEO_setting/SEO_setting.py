from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from frontend.SEO_setting.SEO_setting import Ui_Form
from backend.SEO_setting.platform_setting.platform_setting import PlatformSetting
from backend.SEO_setting.set_table import SetTable
import requests
from model.utils import seo_logger as my_logger
import datetime
from backend.SEO_setting.table_insertion import TableInsertion
import json
import re


class SEOSetting(Ui_Form):
    def __init__(self, page, main_page):
        super().setupUi(page)
        self.page = page
        self.main_page = main_page
        self.cookies = main_page.cookies
        self.headers = main_page.headers
        self.tableWidget.action1 = QAction("修改")
        self.tableWidget.popup_menu.addAction(self.tableWidget.action1)
        self.platform_setting_page = PlatformSetting(self.tab, self, self.main_page)
        # self.programe_setting_page = ProgramSetting(self.tab_2)

        SetTable(self.tableWidget, main_page).main()
        self.main()
        # self.get_config()

        self.connect_slot()

    def main(self):
        self.t_init = InitThread(self)
        self.t_init.start()
        self.t_init.msg_trigger.connect(self.return_msg_trigger)
        self.t_init.trigger.connect(self.return_finish_init_trigger)

    def return_msg_trigger(self, msg):
        self.main_page.return_msg_update(msg)

    def return_finish_init_trigger(self, seo_setting_l, sector_l):
        self.comboBox.clear()
        self.total_seo_setting_l = seo_setting_l
        self.sector_l = sector_l

        self.comboBox.addItems([ele['name'] for ele in self.sector_l])
        self.refresh_table()

    def table_insert(self):
        TableInsertion(self.tableWidget).main(self.seo_setting_l)

    def get_current_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_config(self):
        self.sec_words_d_l = {}
        url1 = f'{self.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_type&mode=seoconfig'
        # url2 = 'http://192.168.110.12:5001/index.php?m=seoconfig&c=oauth&a=json_submenu&keyid={parent_id}'
        try:
            seo_setting_config = requests.get(url1, headers=self.headers, cookies=self.cookies).json()
            # self.lanmu_l = requests.get(url2, headers=self.headers, cookies=self.cookies).json()
            # print(json.loads(self.seo_setting_l))
            # self.seo_setting_l = self.seo_setting_l.json()
        except Exception as e:
            my_logger.error(e)
            self.main_page.return_msg_update(str(e))
        else:
            for d in seo_setting_config:
                res = self.get_words(d['typeid'])
                if d['name'] == '修饰词':
                    self.sec_words_d_l[d['name']] = res
                elif d['name'] == '业务词':
                    self.sec_words_d_l[d['name']] = res
                elif d['name'] == '品牌词':
                    self.sec_words_d_l[d['name']] = res
                elif d['name'] == '地区':
                    self.sec_words_d_l[d['name']] = res

    def get_words(self, type_id):
        parent_id = self.sector_l[self.comboBox.currentIndex()]['typeid']
        url = f'{self.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_seoconfig_ke&sectorid={parent_id}&typeid={type_id}'
        try:
            res = requests.get(url, headers=self.headers, cookies=self.cookies).json()

        except Exception as e:
            my_logger.error(e)
            self.main_page.return_msg_update(str(e))
        else:
            return res

    def action_trigger(self):
        current_row_seo_info = self.seo_setting_l[self.tableWidget.row]
        self.refresh_setting_page(current_row_seo_info)
        self.platform_setting_page.from_outside = True

    def refresh_setting_page(self, seo_info):
        self.platform_setting_page.lineEdit_10.setText(seo_info['name'])
        content = json.loads(seo_info['content'])
        self.platform_setting_page.lineEdit.setText(content['title'])               # 标题
        self.platform_setting_page.lineEdit_2.setText(content['keywords'])          # 关键词
        if content.get('description'):
            self.platform_setting_page.lineEdit_3.setText(content['description'])       # 描述
        else:
            self.platform_setting_page.checkBox.setChecked(True)
        self.platform_setting_page.lineEdit_4.setText(content['lanmu'])             # 栏目数量
        self.platform_setting_page.lineEdit_5.setText(content['guanjianci'])        # 关键词
        self.platform_setting_page.lineEdit_6.setText(content['xiushici'])          # 修饰词
        self.platform_setting_page.lineEdit_7.setText(content['yewuci'])            # 业务词
        self.platform_setting_page.lineEdit_8.setText(content['pingpaici'])         # 品牌词
        self.platform_setting_page.lineEdit_9.setText(content['diquci'])            # 地区词
        self.platform_setting_page.seo_info = seo_info

    def connect_slot(self):
        # self.pushButton.clicked.connect(self.get_config)
        self.tableWidget.action1.triggered.connect(self.action_trigger)
        self.comboBox.currentIndexChanged.connect(self.refresh_table)
        self.pushButton.clicked.connect(self.main)

    def refresh_table(self):
        self.seo_setting_l = [ele for ele in self.total_seo_setting_l if json.loads(ele['content'])['typeid'] == self.sector_l[self.comboBox.currentIndex()]['typeid']]
        self.table_insert()


class InitThread(QThread):
    msg_trigger = pyqtSignal(str)
    trigger = pyqtSignal(list, list)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        try:
            try:
                url1 = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_seoconfig'
                seo_setting_l = requests.get(url1, headers=self.ui.headers, cookies=self.ui.cookies).json()

                url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_type&mode=sector'  # 获取行业， 放入comboBox中
                upper_cate_url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_init'

                sector_l = requests.get(url, headers=self.ui.headers, cookies=self.ui.cookies, timeout=5).json()
                upper_cate_l = requests.get(upper_cate_url, headers=self.ui.headers, cookies=self.ui.cookies,
                                            timeout=5).json()
                for ele in sector_l:
                    ele['upper_cate_info'] = []
                    for item in upper_cate_l:
                        if ele['typeid'] == item['typeid']:
                            ele['upper_cate_info'].append(item)
            except Exception as e:
                my_logger.error(e)
                self.msg_trigger.emit(self.ui.get_current_datetime() + ": " + "无法连接至服务器")
                sector_l = []
                seo_setting_l = []
            self.trigger.emit(seo_setting_l, sector_l)
        except Exception as e:
            my_logger.error(e)
            print("无法连接至服务器！")


class LanmuThread(QThread):
    trigger = pyqtSignal(list)

    def __init__(self, ui, parent_id):
        super().__init__()
        self.ui = ui
        self.parent_id = parent_id

    def run(self):
        try:
            url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_submenu&keyid={self.parent_id}'
            cate_l = requests.get(url, headers=self.ui.headers, cookies=self.ui.cookies).json()
            self.trigger.emit(cate_l)
        except Exception as e:
            my_logger.error(e)
            print("无法连接至服务器！")

