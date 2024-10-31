from PyQt5.QtWidgets import *
from selenium.webdriver.common.by import By

from frontend.auto_publish.platforms_management.platform_setting.platform_setting import Ui_Form
from PyQt5.QtCore import QTime
import requests
import json
import webbrowser
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from model.utils import auto_publish_logger as my_logger
from PyQt5.QtCore import *
import logging


class PlatformSetting(QWidget, Ui_Form):
    def __init__(self, sector_l, platform_setting_info, main_page, ui):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowStaysOnTopHint|Qt.WindowCloseButtonHint)

        self.platform_setting_info = platform_setting_info
        self.sector_l = sector_l
        self.ui = ui
        self.append_sector_l()
        self.main_page = main_page
        self.main_page.show_loading_label()
        self.connect_slot()
        self.set_info()

    def append_sector_l(self):
        self.comboBox.clear()
        self.comboBox.addItems([i['name'] for i in self.sector_l])

    def set_info(self):
        self.get_sector()
        print(11111111111111111, self.platform_setting_info)
        mobile_l = json.loads((self.platform_setting_info['mobile'])) if self.platform_setting_info['mobile'] else ['', '']
        backstage_l = json.loads(self.platform_setting_info['backstage']) if self.platform_setting_info['backstage'] else ['', '', '']
        self.lineEdit.setText(self.platform_setting_info['domain'])
        self.lineEdit_2.setText(self.platform_setting_info['api'])
        self.lineEdit_3.setText(self.platform_setting_info['baidu_token'])
        self.lineEdit_4.setText(self.platform_setting_info['num'])
        self.lineEdit_7.setText(self.platform_setting_info['token'])
        s_hr, s_min, s_sec = self.return_hr_min_sec(self.platform_setting_info['start_time'])
        e_hr, e_min, e_sec = self.return_hr_min_sec(self.platform_setting_info['start_times'])
        self.textEdit.setText(self.platform_setting_info['remarks'])
        self.timeEdit.setTime(QTime(s_hr, s_min, s_sec))
        self.timeEdit_2.setTime(QTime(e_hr, e_min, e_sec))
        if self.platform_setting_info['mobile']:
            self.radioButton_9.setChecked(True)
            self.radioButton_10.setChecked(False)
            self.lineEdit_5.setText(mobile_l[0])
            self.lineEdit_6.setText(mobile_l[1])
        else:
            self.radioButton_9.setChecked(False)
            self.radioButton_10.setChecked(True)
        self.lineEdit_8.setText(backstage_l[0])
        self.lineEdit_9.setText(backstage_l[1])
        self.lineEdit_10.setText(backstage_l[2])


        if str(self.platform_setting_info['baidu_rule']) == '0':
            self.radioButton.setChecked(True)
            self.radioButton_2.setChecked(False)
        else:
            self.radioButton.setChecked(False)
            self.radioButton_2.setChecked(True)

        if str(self.platform_setting_info['order']) == '1':
            self.radioButton_3.setChecked(False)
            self.radioButton_4.setChecked(True)
            self.radioButton_5.setChecked(False)
        elif str(self.platform_setting_info['order']) == '2':
            self.radioButton_3.setChecked(False)
            self.radioButton_4.setChecked(False)
            self.radioButton_5.setChecked(True)
        else:
            self.radioButton_3.setChecked(True)
            self.radioButton_4.setChecked(False)
            self.radioButton_5.setChecked(False)

        if str(self.platform_setting_info['release']) == '0':
            self.radioButton_6.setChecked(True)
            self.radioButton_7.setChecked(False)
        else:
            self.radioButton_6.setChecked(False)
            self.radioButton_7.setChecked(True)

    def get_sector(self):
        sector_id = self.platform_setting_info['typeid']
        for row, item in enumerate(self.sector_l):
            if int(item['typeid']) == int(sector_id):
                self.comboBox.setCurrentIndex(row)
                break

    def return_hr_min_sec(self, str_time):
        l = str_time.split(":")
        return int(l[0]), int(l[1]), int(l[2])

    def radio_box_exclusive(self, checked_radio_box, radio_boxes_l):
        if checked_radio_box in radio_boxes_l and checked_radio_box.isChecked():
            radio_boxes_l.remove(checked_radio_box)
            for radio_box in radio_boxes_l:
                radio_box.setChecked(False)

    def radio_auto_exclusive(self, radio_button):
        if radio_button.isChecked():
            if radio_button == self.radioButton or radio_button == self.radioButton_2:
                self.radio_box_exclusive(radio_button, [self.radioButton, self.radioButton_2])
            elif radio_button == self.radioButton_3 or radio_button == self.radioButton_4 or radio_button == self.radioButton_5:
                self.radio_box_exclusive(radio_button, [self.radioButton_3, self.radioButton_4, self.radioButton_5])
            elif radio_button == self.radioButton_6 or radio_button == self.radioButton_7 or radio_button == self.radioButton_8:
                self.radio_box_exclusive(radio_button, [self.radioButton_6, self.radioButton_7, self.radioButton_8])
            elif radio_button == self.radioButton_9 or radio_button == self.radioButton_10:
                self.radio_box_exclusive(radio_button, [self.radioButton_9, self.radioButton_10])
                self.check_mobile_web()         # 隐藏和显示下属列
        else:
            if radio_button == self.radioButton or radio_button == self.radioButton_2:
                self.check_rest_uncheck(radio_button, [self.radioButton, self.radioButton_2])
            elif radio_button == self.radioButton_3 or radio_button == self.radioButton_4 or radio_button == self.radioButton_5:
                self.check_rest_uncheck(radio_button, [self.radioButton_3, self.radioButton_4, self.radioButton_5])
            elif radio_button == self.radioButton_6 or radio_button == self.radioButton_7 or radio_button == self.radioButton_8:
                self.check_rest_uncheck(radio_button, [self.radioButton_6, self.radioButton_7, self.radioButton_8])
            elif radio_button == self.radioButton_9 or radio_button == self.radioButton_10:
                self.check_rest_uncheck(radio_button, [self.radioButton_9, self.radioButton_10])

    def check_rest_uncheck(self, radio_button, radio_button_l):
        for r in radio_button_l:
            if r.isChecked():
                break
        else:
            radio_button.setChecked(True)

    def check_mobile_web(self):
        if self.radioButton_9.isChecked():
            self.label_13.show()
            self.lineEdit_5.show()
            self.lineEdit_6.show()
        else:
            self.label_13.hide()
            self.lineEdit_5.hide()
            self.lineEdit_6.hide()

    def cancel(self):
        self.close()

    def confirm(self):
        if self.check_pc_hash_valid():
            return_d = self.get_content()
            status = self.submit(return_d)
            print(3333333, status)
            if status:
                if return_d['mobile_enable']:
                    return_d['mobile'] = json.dumps([return_d['mobile_web'], return_d['mobile_token']])
                else:
                    return_d['mobile'] = ''

                if return_d['backstage']:
                    return_d['backstage'] = json.dumps(return_d['backstage'])
                self.ui.current_web_l[self.ui.page * self.ui.row_limit + self.ui.tableWidget.row].update(return_d)
                print(self.ui.page * self.ui.row_limit + self.ui.tableWidget.row)
                print(self.ui.current_web_l[self.ui.page * self.ui.row_limit + self.ui.tableWidget.row])
                print(return_d)
                self.ui.table_insertion()
        else:
            self.close_message_box()

    def close_message_box(self):
        msg_box = QMessageBox()
        msg_box.setWindowFlags(Qt.WindowStaysOnTopHint)

        reply = msg_box.information(None, 'Message', 'PC_HASH验证失败，请登录后重试！确认是否重新登录？',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            self.main_page.close()

    def get_content(self):
        return_d = {}
        typeid = self.sector_l[self.comboBox.currentIndex()]['typeid']
        web = self.lineEdit.text()
        api = self.lineEdit_2.text()
        baidu_token = self.lineEdit_3.text()
        token = self.lineEdit_7.text()
        mobile = self.check_radio_button([self.radioButton_10, self.radioButton_9])
        mobile_web = self.lineEdit_5.text()
        mobile_token = self.lineEdit_6.text()
        backstage = [self.lineEdit_8.text(), self.lineEdit_9.text(), self.lineEdit_10.text()]
        baidu_push_rules = self.check_radio_button([self.radioButton, self.radioButton_2])
        publish_order = self.check_radio_button([self.radioButton_4, self.radioButton_5, self.radioButton_3])
        after_publish = self.check_radio_button([self.radioButton_6, self.radioButton_7, self.radioButton_8])
        num = self.lineEdit_4.text()
        start_time = str(self.timeEdit.dateTime().toPyDateTime().time())
        end_time = str(self.timeEdit_2.dateTime().toPyDateTime().time())
        remark = self.textEdit.toPlainText()

        return_d['typeid'] = typeid
        return_d['web'] = web
        return_d['api'] = api
        return_d['baidu_token'] = baidu_token
        return_d['token'] = token
        return_d['mobile_enable'] = mobile
        return_d['mobile_web'] = mobile_web
        return_d['mobile_token'] = mobile_token
        return_d['baidu_rule'] = baidu_push_rules
        return_d['order'] = publish_order + 1
        return_d['release'] = after_publish
        return_d['num'] = num
        return_d['start_time'] = start_time
        return_d['end_time'] = end_time
        return_d['remarks'] = remark
        return_d['backstage'] = backstage
        return_d['domain'] = web
        return return_d

    def submit(self, return_d):
        url = f'{self.main_page.domain}/index.php?m=automatic&json=1&c=automatic_admin&a=edit&id={self.platform_setting_info["id"]}'

        data = {}
        data['data[typeid]'] = return_d['typeid']
        data['data[domain]'] = return_d['web']
        data['data[token]'] = return_d['token']
        data['dis_type'] = return_d['mobile_enable'] + 1
        if return_d['mobile_enable']:
            mobile_info = [return_d['mobile_web'], return_d['mobile_token']]
            data['data[mobile][]'] = mobile_info
            # data['data[mobile][]'] = json.encoder(a)
        data['data[api]'] = return_d['api']
        data['data[baidu_token]'] = return_d['baidu_token']
        data['data[baidu_rule]'] = str(return_d['baidu_rule'])
        data['data[order]'] = str(return_d['order'])          # 因为规则好像跟另外俩不一样...
        data['data[release]'] = str(return_d['release'])
        data['data[num]'] = str(return_d['num'])
        data['data[start_time]'] = return_d['start_time']
        data['data[start_times]'] = return_d['end_time']
        data['data[remarks]'] = return_d['remarks']
        data['data[backstage][]'] = return_d['backstage']
        data['dosubmit'] = ''
        data['pc_hash'] = self.main_page.pc_hash
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            }
        try:
            print(222222222222, data)
            response = requests.post(url, headers=self.headers, cookies=self.main_page.cookies, data=data).json()
        except Exception as e:
            print(str(e))
            self.main_page.return_msg_update(str(e))
            return False
        else:
            self.close()
            if response.get('msg') == '成功！':
                return True
            else:
                return False

    def check_radio_button(self, radio_button_l):           # 返回被check的radio_button在同一list中radio_button的index
        for i, r in enumerate(radio_button_l):
            if r.isChecked():
                return i
        else:
            return 0            # 没有的话返回默认的0

    def open_backstage_page(self):
        url = self.lineEdit_8.text()
        username = self.lineEdit_9.text()
        password = self.lineEdit_10.text()
        # webbrowser.open(url)
        # 设置Chrome浏览器驱动程序的路径
        chrome_driver_path = "config/chromedriver-win64/chromedriver.exe"

        # 初始化Chrome浏览器
        # browser = webdriver.Chrome(executable_path=chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        # 使用Service对象来指定ChromeDriver路径
        service = Service(chrome_driver_path)
        browser = webdriver.Chrome(service=service, options=options)
        try:
            browser.get(url)
            browser.find_element(by=By.CSS_SELECTOR, value='.ipt:nth-child(3)').send_keys(username)
            browser.find_element(by=By.CSS_SELECTOR, value='.ipt:nth-child(5)').send_keys(password)
            browser.find_element(by=By.CSS_SELECTOR, value='.login_tj_btn').submit()
        except Exception as e:
            pass

    def check_pc_hash_valid(self):
        url = f'{self.main_page.domain}/index.php?m=admin&c=index&json=1'
        try:
            # return_data['pc_hash'] = self.parent_ui.parent_ui.main_page.pc_hash
            response = requests.post(url, headers=self.main_page.headers, cookies=self.main_page.cookies).json()
            return False
        except Exception as e:
            return True

    def connect_slot(self):
        self.pushButton.clicked.connect(self.confirm)
        self.pushButton_2.clicked.connect(self.cancel)
        self.pushButton_3.clicked.connect(self.open_backstage_page)
        self.radioButton.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton))
        self.radioButton_2.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_2))
        self.radioButton_3.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_3))
        self.radioButton_4.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_4))
        self.radioButton_5.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_5))
        self.radioButton_6.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_6))
        self.radioButton_7.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_7))
        self.radioButton_8.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_8))
        self.radioButton_9.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_9))
        self.radioButton_10.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_10))

    def closeEvent(self, event):
        self.main_page.hide_loading_label()
        event.accept()                      # 允许正常关闭