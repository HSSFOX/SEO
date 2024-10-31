import copy

from frontend.auto_publish.platforms_management.batch_edit.batch_edit import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from api_requests.TokenAPI import Token
import json
from model.utils import auto_publish_logger as my_logger
from PyQt5.QtWidgets import QMessageBox, QAction
from PyQt5.QtCore import *
import logging
from PyQt5.QtGui import *
from urllib.parse import urlparse
import tldextract
from api_requests.RedisAPI import RedisDb
import datetime
import string
import random


class BatchEdit(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent_ui, checked_l):
        super().__init__()
        self.setupUi(self)
        # self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowStaysOnTopHint|Qt.WindowCloseButtonHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowCloseButtonHint)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            }
        self.parent_ui = parent_ui
        self.checked_l = checked_l
        self.token_api = Token()
        self.ftp_l = []
        self.parent_ui.main_page.show_loading_label()
        self.redis = RedisDb()
        self.get_remote_ftp()
        self.connect_slot()
        self.create_loading_label()

    def radio_box_exclusive(self, checked_radio_box, radio_boxes_l):
        if checked_radio_box in radio_boxes_l and checked_radio_box.isChecked():
            radio_boxes_l.remove(checked_radio_box)
            for radio_box in radio_boxes_l:
                radio_box.setChecked(False)

    def radio_auto_exclusive(self, radio_button):
        if radio_button.isChecked():
            if radio_button == self.radioButton or radio_button == self.radioButton_2 or radio_button == self.radioButton_3:
                self.radio_box_exclusive(radio_button, [self.radioButton, self.radioButton_2, self.radioButton_3])
            elif radio_button == self.radioButton_6 or radio_button == self.radioButton_4 or radio_button == self.radioButton_5 or radio_button == self.radioButton_7:
                self.radio_box_exclusive(radio_button, [self.radioButton_6, self.radioButton_4, self.radioButton_5, self.radioButton_7])
            elif radio_button == self.radioButton_9 or radio_button == self.radioButton_11 or radio_button == self.radioButton_8 or radio_button == self.radioButton_10:
                self.radio_box_exclusive(radio_button, [self.radioButton_9, self.radioButton_11, self.radioButton_8, self.radioButton_10])
            elif radio_button == self.radioButton_12 or radio_button == self.radioButton_13 or radio_button == self.radioButton_21:            # 密码修改
                self.radio_box_exclusive(radio_button, [self.radioButton_12, self.radioButton_13, self.radioButton_21])
            elif radio_button == self.radioButton_14 or radio_button == self.radioButton_15 or radio_button == self.radioButton_16:
                self.radio_box_exclusive(radio_button, [self.radioButton_14, self.radioButton_15, self.radioButton_16])
            elif radio_button == self.radioButton_17 or radio_button == self.radioButton_18:            # 域名前缀
                self.radio_box_exclusive(radio_button, [self.radioButton_17, self.radioButton_18])
            elif radio_button == self.radioButton_19 or radio_button == self.radioButton_20:            # 后台url修改
                self.radio_box_exclusive(radio_button, [self.radioButton_19, self.radioButton_20])
            elif radio_button == self.radioButton_23 or radio_button == self.radioButton_24:            # 文章数量修改
                self.radio_box_exclusive(radio_button, [self.radioButton_23, self.radioButton_24])
            elif radio_button == self.radioButton_25 or radio_button == self.radioButton_26:            # 文章发布时间修改
                self.radio_box_exclusive(radio_button, [self.radioButton_25, self.radioButton_26])

        else:           # 确认在一个自定义范围内的radio button不可以被直接点掉导致无radio button被选择
            if radio_button == self.radioButton or radio_button == self.radioButton_2 or radio_button == self.radioButton_3:
                self.check_rest_uncheck(radio_button, [self.radioButton, self.radioButton_2, self.radioButton_3])
            elif radio_button == self.radioButton_6 or radio_button == self.radioButton_4 or radio_button == self.radioButton_5 or radio_button == self.radioButton_7:
                self.check_rest_uncheck(radio_button, [self.radioButton_6, self.radioButton_4, self.radioButton_5, self.radioButton_7])
            elif radio_button == self.radioButton_9 or radio_button == self.radioButton_11 or radio_button == self.radioButton_8 or radio_button == self.radioButton_10:
                self.check_rest_uncheck(radio_button, [self.radioButton_9, self.radioButton_11, self.radioButton_8, self.radioButton_10])
            elif radio_button == self.radioButton_12 or radio_button == self.radioButton_13 or radio_button == self.radioButton_21:
                self.check_rest_uncheck(radio_button, [self.radioButton_12, self.radioButton_13, self.radioButton_21])
            elif radio_button == self.radioButton_14 or radio_button == self.radioButton_15 or radio_button == self.radioButton_16:
                self.check_rest_uncheck(radio_button, [self.radioButton_14, self.radioButton_15, self.radioButton_16])
            elif radio_button == self.radioButton_17 or radio_button == self.radioButton_18:
                self.check_rest_uncheck(radio_button, [self.radioButton_17, self.radioButton_18])
            elif radio_button == self.radioButton_19 or radio_button == self.radioButton_20:            # 后台url修改
                self.check_rest_uncheck(radio_button, [self.radioButton_19, self.radioButton_20])

            elif radio_button == self.radioButton_23 or radio_button == self.radioButton_24:            # 文章数量修改
                self.check_rest_uncheck(radio_button, [self.radioButton_23, self.radioButton_24])
            elif radio_button == self.radioButton_25 or radio_button == self.radioButton_26:            # 文章发布时间修改
                self.check_rest_uncheck(radio_button, [self.radioButton_25, self.radioButton_26])

    def check_rest_uncheck(self, radio_button, radio_button_l):
        for r in radio_button_l:
            if r.isChecked():
                break
        else:
            radio_button.setChecked(True)

    def connect_slot(self):
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
        self.radioButton_11.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_11))
        self.radioButton_12.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_12))
        self.radioButton_13.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_13))
        self.radioButton_14.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_14))
        self.radioButton_15.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_15))
        self.radioButton_16.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_16))
        self.radioButton_17.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_17))
        self.radioButton_18.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_18))
        self.radioButton_19.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_19))
        self.radioButton_20.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_20))
        self.radioButton_21.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_21))         # 密码随机修改

        self.radioButton_23.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_23))
        self.radioButton_24.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_24))  # 文章数修改

        self.radioButton_25.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_25))
        self.radioButton_26.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_26))  # 文章发布时间数修改

        self.pushButton.clicked.connect(self.update_token_api)
        self.pushButton_2.clicked.connect(self.save)
        self.pushButton_3.clicked.connect(self.cancel)

    def save(self):

        run_sign, return_data, change_password_d, tdk_data = self.get_batch_config()
        if run_sign:
            self.pushButton_2.setText("保存中...")
            self.pushButton_2.setEnabled(False)
            self.show_loading_label()
            filter_sign = not self.comboBox.currentIndex() == 0             # 如果有FTP 筛选=True
            if filter_sign:
                domain_l = self.get_domain()
            else:
                domain_l = []
            if self.ftp_l:
                ftp_setting = self.ftp_l[self.comboBox.currentIndex() - 1]
                self.t_save = SaveThread(self, self.checked_l, domain_l, ftp_setting, filter_sign, return_data, change_password_d, tdk_data)
                self.t_save.start()
                self.t_save.single_update_trigger.connect(self.update_table)
                self.t_save.finished_trigger.connect(self.return_finish)
                self.t_save.msg_trigger.connect(self.parent_ui.main_page.return_msg_update)
                self.t_save.pc_hash_trigger.connect(self.close_message_box)

    def close_message_box(self):
        msg_box = QMessageBox()
        msg_box.setWindowFlags(Qt.WindowStaysOnTopHint)

        reply = msg_box.information(None, 'Message', 'PC_HASH验证失败，请登录后重试！确认是否重新登录？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            self.parent_ui.main_page.close()

    def update_table(self, info, return_data):          # info来自于里边儿的item
        for row, item in enumerate(self.parent_ui.current_web_l):
            if item['domain'] == info['domain']:
                if return_data.get('data[baidu_rule]'):
                    self.parent_ui.current_web_l[row]['baidu_rule'] = return_data.get('data[baidu_rule]')
                if return_data.get('data[order]'):
                    self.parent_ui.current_web_l[row]['order'] = return_data.get('data[order]')
                if return_data.get('data[release]'):
                    self.parent_ui.current_web_l[row]['baidu_rule'] = return_data.get('data[baidu_rule]')
                if return_data.get('data[backstage][]'):
                    self.parent_ui.current_web_l[row]['backstage'] = json.dumps(return_data.get('data[backstage][]'))
                if return_data.get('data[api]'):
                    self.parent_ui.current_web_l[row]['api'] = return_data.get('data[api]')
                if return_data.get('data[domain]'):
                    self.parent_ui.current_web_l[row]['domain'] = return_data.get('data[domain]')
                if return_data.get('data[num]'):
                    self.parent_ui.current_web_l[row]['num'] = return_data.get('data[num]')
                if return_data.get('data[start_time]'):
                    self.parent_ui.current_web_l[row]['start_time'] = return_data.get('data[start_time]')
                if return_data.get('data[start_times]'):
                    self.parent_ui.current_web_l[row]['start_times'] = return_data.get('data[start_times]')

    def return_finish(self):
        self.parent_ui.filter_insert()
        self.hide_loading_label()
        if self.radioButton_20.isChecked():
            # 确认手动更新宝塔后台文件名
            reply = QMessageBox.information(None, '', "请手动配置宝塔文件名！", QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                self.close()
        else:
            self.close()

    def get_batch_config(self):
        run_sign = True
        return_data = {}
        change_password_d = {}
        tdk_data = {}
        if self.radioButton_2.isChecked() or self.radioButton_3.isChecked():
            baidu_rule = self.check_radio_button([self.radioButton_2, self.radioButton_3])
            return_data['data[baidu_rule]'] = str(baidu_rule)

        if self.radioButton_5.isChecked() or self.radioButton_6.isChecked() or self.radioButton_7.isChecked():
            order = self.check_radio_button([self.radioButton_5, self.radioButton_6, self.radioButton_7])
            return_data['data[order]'] = str(order + 1)

        if self.radioButton_9.isChecked() or self.radioButton_10.isChecked() or self.radioButton_11.isChecked():
            release = self.check_radio_button([self.radioButton_9, self.radioButton_10, self.radioButton_11])
            return_data['data[release]'] = str(release)

        if self.radioButton_24.isChecked():
            try:
                num = int(self.lineEdit_3.text())
            except Exception as e:
                QMessageBox.warning(None, '站群批量编辑', '请确认文章数量格式为数字且不包含空格等特殊符号！')
                run_sign = False
            else:
                return_data['data[num]'] = str(num)

        if self.radioButton_26.isChecked():
            start_time = str(self.timeEdit.time().toPyTime())
            end_time = str(self.timeEdit_2.time().toPyTime())
            return_data['data[start_time]'] = start_time
            return_data['data[start_times]'] = end_time

        if self.radioButton_16.isChecked():
            tdk_data['is_https'] = '2'
        elif self.radioButton_15.isChecked():
            tdk_data['is_https'] = '1'

        if self.radioButton_18.isChecked():
            tdk_data['is_www'] = '1'

        if self.radioButton_21.isChecked():
            change_password_d['change_password'] = self.generate_random_string(random.randint(5, 16))
        elif self.radioButton_13.isChecked() and self.lineEdit.text():        # 是否自定义
            custom_password = self.lineEdit.text()
            change_password_d['change_password'] = custom_password


        if self.radioButton_20.isChecked() and self.lineEdit_2.text():
            custom_backstage_url = self.lineEdit_2.text()
            change_password_d['change_backstage_url'] = custom_backstage_url

        return run_sign, return_data, change_password_d, tdk_data

    def generate_random_string(self, length):
        # 字符集包括小写字母、大写字母和数字
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def cancel(self):
        self.close()

    def update_token_api(self):
        self.show_loading_label()
        self.parent_ui.update_token()
        # 添加一个 是否关闭窗口
        # self.close_application()

    def close_application(self):
        msg_box = QMessageBox()
        msg_box.setWindowFlags(Qt.WindowStaysOnTopHint)

        reply = msg_box.information(None, 'Message', '更新Token已完成，是否关闭窗口？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

    def check_radio_button(self, radio_button_l):           # 返回被check的radio_button在同一list中radio_button的index
        for i, r in enumerate(radio_button_l):
            if r.isChecked():
                return i
        else:
            return 0            # 没有的话返回默认的0

    def get_remote_ftp(self):
        url = f'{self.parent_ui.main_page.domain}/index.php?m=automatic&c=oauth&a=json_RDS'
        try:
            self.ftp_l = requests.get(url).json()
            print("ftp_l", self.ftp_l)
        except Exception as e:
            my_logger.error(e)
            logging.error(e, exc_info=True)
            self.ftp_l = []
        finally:
            self.comboBox.addItems([''] + [i['id'] for i in self.ftp_l])

    def get_domain(self):
        sum_l = []
        # for ftp_setting in self.ftp_l:
        ftp_setting = self.ftp_l[self.comboBox.currentIndex() - 1]
        ftp_path = ftp_setting['analyzed']
        for url in ftp_path.split("\n"):
            domain = tldextract.extract(url).registered_domain
            sum_l.append(domain)
        return sum_l

    # def get_url_without_domain(self, url):
    #     domain = tldextract.extract(url).registered_domain
    #     return domain

    def closeEvent(self, event):
        self.parent_ui.main_page.hide_loading_label()
        event.accept()                      # 允许正常关闭

    def create_loading_label(self):
        self.loading_label = QtWidgets.QLabel(self)
        self.loading_label.showMaximized()
        width = self.size().width()
        height = self.size().height()
        # self.loading_label.setGeometry(QtCore.QRect(0, 0, width//2, height//2))
        self.loading_label.setStyleSheet("background-color: rgba(255, 255, 255, 180)")
        self.loading_label.setMinimumSize(QtCore.QSize(width, height))
        self.loading_label.setMaximumSize(QtCore.QSize(width, height))
        self.loading_label.setAlignment(QtCore.Qt.AlignCenter| QtCore.Qt.AlignVCenter)
        self.loading_label.setObjectName("label")
        self.loading_label.setText("正在更新中...")
        self.loading_label.setStyleSheet("QLabel{font-size: 30px;background-color: #F5F5F5;}")
        # self.movie = QMovie("./docs/image/loading.gif")
        # self.movie = QMovie("")
        # self.movie.setCacheMode(QMovie.CacheAll)
        # self.loading_label.setMovie(self.movie)
        # self.movie.start()
        self.loading_label.hide()

    def hide_loading_label(self):
        if self.loading_label.isHidden() is False:
            self.loading_label.hide()

    def show_loading_label(self):
        if self.loading_label.isVisible() is False:
            width = self.size().width()
            height = self.size().height()
            self.loading_label.setMinimumSize(QtCore.QSize(width, height))
            self.loading_label.setMaximumSize(QtCore.QSize(width, height))
            self.loading_label.show()


class SaveThread(QThread):
    msg_trigger = pyqtSignal(str)
    finished_trigger = pyqtSignal()
    pc_hash_trigger = pyqtSignal()
    single_update_trigger = pyqtSignal(dict, dict)

    def __init__(self, parent_ui, check_list, domain_l, ftp_setting, filter_sign, return_data, change_password_d, tdk_data):
        super().__init__()
        self.parent_ui = parent_ui
        self.check_list = check_list
        self.domain_l = domain_l
        self.ftp_setting = ftp_setting
        self.filter_sign = filter_sign
        self.return_data = return_data
        self.change_password_d = change_password_d
        self.tdk_data = tdk_data
        self.token_api = Token()

    def run(self):
        redis_update_d = {}
        if self.check_pc_hash_valid():
            self.get_ftp_prefix()
            for item in self.check_list:
                update_data = copy.deepcopy(self.return_data)
                print(999999999999, item)
                if self.filter_sign:
                    self.filter_url_upload_ftp(item)
                if self.change_password_d.get('change_password'):
                    # 改密码
                    status, password = self.change_password_submit(item, self.change_password_d)            # 网站端改密码（非后台）
                    if status:
                        self.msg_trigger.emit(f"{item['domain']} 密码修改成功")
                        backstage_info = json.loads(item['backstage'])
                        # if self.change_password_d.get("change_backstage_url"):
                        #     backstage_info[0] = self.change_password_d['change_backstage_url']
                        backstage_info[2] = password
                        update_data['data[backstage][]'] = backstage_info
                        item['backstage'] = json.dumps(backstage_info)      # 变为string 作为tdk时可能用到的参数
                    else:
                        self.msg_trigger.emit(f"{item['domain']} 密码修改失败")

                if self.change_password_d.get("change_backstage_url"):
                    backstage_info = json.loads(item['backstage'])
                    backstage_info[0] = item['domain'] + self.change_password_d['change_backstage_url']
                    update_data['data[backstage][]'] = backstage_info
                    item['backstage'] = json.dumps(backstage_info)  # 变为string 作为tdk时可能用到的参数

                if self.tdk_data:
                    status, url = self.update_web_tdk(item, self.tdk_data)
                    if status:
                        redis_update_d[item['domain']] = url
                        self.msg_trigger.emit(f"{item['domain']} 网站TDK修改成功")
                        update_data = self.butterfly_after_tdk(url, item, update_data)
                    else:
                        self.msg_trigger.emit(f"{item['domain']} 网站TDK修改失败，请检查网络或确认域名是否解析！")
                if update_data:
                    print(111111111, item)
                    print(222222222, update_data)
                    submit_status = self.submit(item, update_data)
                    if submit_status:
                        if update_data.get('data[num]'):
                            item['num'] = update_data['data[num]']
                        if update_data.get('data[start_time]') and update_data['data[start_times]']:
                            item['start_time'] = update_data['data[start_time]']
                            item['start_times'] = update_data['data[start_times]']
                        print("传出去前的item: ", item)
                        # self.single_update_trigger.emit(item, update_data)             # 单行数据更新
            if redis_update_d:
                self.check_redis_update_domain(redis_update_d)
            self.finished_trigger.emit()            # 返回并更新表
        else:
            self.msg_trigger.emit("PC_HASH验证失败，请检查是否已登录！")
            self.pc_hash_trigger.emit()

    def butterfly_after_tdk(self, url, web_data, update_data):
        new_domain = tldextract.extract(url).registered_domain

        update_data['data[api]'] = url + "jiekou.php"
        backstage_info = json.loads(web_data['backstage'])
        backstage_info[0] = url + "myadmin/index.php"
        update_data['data[backstage][]'] = backstage_info
        update_data['data[domain]'] = url
        if web_data['mobile']:
            mobile_info = json.loads(web_data['mobile'])
            if '://www.' in url:
                mobile_info[0] = url.replace("://www.", "://m.")
            else:
                mobile_info[0] = url.replace(new_domain, 'm.' + new_domain)
            update_data['data[mobile][]'] = mobile_info
        return update_data

    def check_redis_update_domain(self, redis_update_d):
        redis_data = self.parent_ui.redis.handle_redis_token(f"jw_refer_d")
        if redis_data:
            combin_d = json.loads(redis_data)
            web_refer_sector_d = combin_d['web_refer_sector_d']
            for domain, new_domain in redis_update_d.items():
                if domain == new_domain:
                    continue
                else:
                    web_refer_sector_d[new_domain] = web_refer_sector_d[domain]
            combin_d['web_refer_sector_d'] = web_refer_sector_d
            self.parent_ui.redis.handle_redis_token(f"jw_refer_d", json.dumps(combin_d), self.get_current_to_tmr_seconds())

    def get_current_to_tmr_seconds(self):
        now = datetime.datetime.now()
        # 获取明天的0点时间
        tomorrow_start = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        # 计算相差的秒数
        seconds_until_midnight = (tomorrow_start - now).seconds
        return seconds_until_midnight

    def swap_http_https(self, v, domain):       # v from tdk_data['is_https']  v = 1 or 2
        if v == '1':
            if 'http://' in domain:
                return domain
            else:
                return domain.replace("https://", "http://")
        elif v == '2':
            if 'https://' in domain:
                return domain
            else:
                return domain.replace("http://", "https://")
        else:
            return domain

    def update_web_tdk(self, web_data, tdk_data):
        client = self.token_api.generateToken(web_data['token'])    # 初始值为空
        client['model'] = 'site'
        # client['name'] = web_data['domain']
        client['domain'] = web_data['domain']
        if tdk_data.get("is_https"):
            client['is_https'] = tdk_data['is_https']
        if tdk_data.get("is_www"):
            client['is_www'] = tdk_data['is_www']
        try:
            response = self.token_api.sendPostRequestWithToken(web_data['api'], client)
            if response.get('status'):
                return True, response['msg']['url']
            else:
                return False, ''
        except Exception as e:
            logging.error(e)
            msg = f"{web_data['name']} 网站TDK设置更新失败 失败原因: {str(e)}"
            self.msg_trigger.emit(msg)
            return False, ''

    def filter_url_upload_ftp(self, item):
        save_sign = False
        if self.domain_l:
            domain_url = tldextract.extract(item['domain']).registered_domain
            if domain_url in self.domain_l:
                save_sign = True
            if save_sign:
                self.update_ftp(item, self.ftp_setting)
            else:
                self.msg_trigger.emit(f"域名{item['domain']} 附件地址未解析, 修改失败")
        else:
            self.msg_trigger.emit(f"域名{item['domain']} 附件地址未解析, 修改失败")

    def update_ftp(self, web_data, ftp_setting):
        try:
            domain = tldextract.extract(web_data['domain']).registered_domain.strip('\r')
            client = self.token_api.generateToken(web_data['token'])
            client['model'] = 'RDS'
            client['setconfig'] = {'ftp_enable': ftp_setting['ftp_enable'],
                                   'ftp_pasv': ftp_setting['ftp_pasv'],
                                   'ftp_host': ftp_setting['ftp_host'],
                                   'ftp_user': ftp_setting['ftp_user'],
                                   'ftp_password': ftp_setting['ftp_password'],
                                   'ftp_port': ftp_setting['ftp_port'],
                                   'ftp_path': "/" + domain.replace(".", "_") + "/",
                                   'ftp_upload_url': self.prefix_d[domain] + domain if self.prefix_d.get(domain) else "//img." + domain,
                                   }

            response = self.token_api.sendPostRequestWithToken(web_data['api'], client)
            if response.get('status'):
                self.msg_trigger.emit(f"域名{web_data['domain']}, {response['msg']}")
                return True
            else:
                self.msg_trigger.emit(f"域名{web_data['domain']}, {response['msg']}")
                return False
        except Exception as e:
            logging.error(e)
            msg = f"{web_data['domain']} 远程FTP设置失败 失败原因: {str(e)}"
            self.msg_trigger.emit(msg)
            return False

    def get_ftp_prefix(self):
        self.prefix_d = {}
        for domain_line in self.ftp_setting['analyzed'].split("\n"):
            if "---------" not in domain_line:              # 如果这一行是域名
                domain = tldextract.extract(domain_line).registered_domain          # 获取域名
                if domain:
                    prefix = domain_line.replace(domain, "").strip('\r')
                    self.prefix_d[domain] = prefix

    def change_password_submit(self, info, change_password_d):
        backstage_info = json.loads(info['backstage'])
        client = self.token_api.generateToken(info['token'])
        client['model'] = 'ChangePassword'
        client['userid'] = '1'
        client['old_password'] = backstage_info[2]
        if change_password_d.get('change_password'):
            client['new_password'] = change_password_d['change_password']
        try:
            response = self.token_api.sendPostRequestWithToken(info['api'], client)
        except Exception as e:
            my_logger.error(e)
            logging.error(e, exc_info=True)
            self.msg_trigger.emit(f"{info['domain']}访问错误: {str(e)}")
            return False, str(e)
        else:
            return response.get('status'), response.get('msg')

    def submit(self, info, return_data):
        url = f'{self.parent_ui.parent_ui.main_page.domain}/index.php?m=automatic&c=automatic_admin&json=1&a=edit&id={info["id"]}'
        try:
            return_data['pc_hash'] = self.parent_ui.parent_ui.main_page.pc_hash
            return_data['dosubmit'] = ''
            print(return_data)
            response = requests.post(url, headers=self.parent_ui.headers, cookies=self.parent_ui.parent_ui.main_page.cookies, data=return_data).json()
            print("站点批量编辑提交返回: ", response)
        except Exception as e:
            logging.error(e, exc_info=True)
            self.msg_trigger.emit(f"{info['domain']}访问错误: {str(e)}")
            return False
        else:
            if response.get('msg') == '成功！':
                self.msg_trigger.emit(f"{info['domain']} 提交成功")
                return True
            else:
                self.msg_trigger.emit(f"{info['domain']} 提交失败")
                return False

    def get_domain(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc


    def check_pc_hash_valid(self):
        url = f'{self.parent_ui.parent_ui.main_page.domain}/index.php?m=admin&c=index&json=1'
        try:
            # return_data['pc_hash'] = self.parent_ui.parent_ui.main_page.pc_hash
            response = requests.post(url, headers=self.parent_ui.headers, cookies=self.parent_ui.parent_ui.main_page.cookies).json()
            return False
        except Exception as e:
            # logging.error(e, exc_info=True)
            return True