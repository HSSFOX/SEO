from PyQt5.QtCore import *
from frontend.auto_publish.platforms_management.platform_management import Ui_Form
from backend.auto_publish.platform_management.set_table import SetTable
import requests
from model.utils import auto_publish_logger as my_logger
from backend.auto_publish.platform_management.table_insertion import TableInsertion
import datetime
from backend.auto_publish.platform_management.platform_setting.platform_setting import PlatformSetting
from api_requests.TokenAPI import Token
import copy
from backend.auto_publish.platform_management.batch_edit.batch_edit import BatchEdit
from backend.auto_publish.platform_management.remote_FTP.remote_FTP import RemoteFTP
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import logging


class PlatformManagement(Ui_Form):
    def __init__(self, page, parent_ui, main_page):
        super().setupUi(page)
        self.ui = page
        self.main_page = main_page
        self.parent_ui = parent_ui
        self.cookies = main_page.cookies
        self.headers = main_page.headers
        self.job_l = []
        self.auto_publish_list = []
        self.current_web_l = []
        # self.create_loading_label()
        self.tableWidget.action1 = QtWidgets.QAction("修改")
        self.tableWidget.popup_menu.addAction(self.tableWidget.action1)
        SetTable(self.tableWidget, main_page).main()
        self.batch_edit_ui = None
        self.table_insertion_setup = TableInsertion(self.tableWidget)
        self.main()
        # self.table_insertion()

        self.set_default_values()

        self.connect_slot()

    def set_default_values(self):
        self.page = 0
        self.max_page = 0
        self.row_limit = 100
        self.update_labels()

        self.date1 = datetime.datetime(2024, 1, 1).date()
        self.date2 = datetime.datetime.now().date()

        self.dateEdit.setDate(QtCore.QDate(2024, 1, 1))
        self.dateEdit_2.setDate(QtCore.QDate.currentDate())
        self.dateEdit.setMaximumDate(QtCore.QDate.currentDate())
        self.dateEdit_2.setMaximumDate(QtCore.QDate.currentDate())

    def main(self):
        self.t_job_thread = JobThread(self)
        self.t_job_thread.start()
        self.t_job_thread.msg_trigger.connect(self.return_msg)
        self.t_job_thread.trigger.connect(self.return_job_finished)

    def return_job_finished(self, job_l):
        self.job_l = job_l
        self.comboBox.addItems([ele['name'] for ele in self.job_l])

        # if self.comboBox.currentIndex() >= 0:
        #     type_id = self.job_l[self.comboBox.currentIndex()]["typeid"]
        #
        #     self.t_publish = PublishThread(self, type_id)
        #     self.t_publish.start()
        #     self.t_publish.msg_trigger.connect(self.return_msg)
        #     self.t_publish.trigger.connect(self.return_publish_finished)

    def update_datetime(self):
        if self.auto_publish_list:
            min_datetime, max_datetime = min([ele['time'] for ele in self.auto_publish_list]), max([ele['time'] for ele in self.auto_publish_list])
            self.date1 = datetime.datetime.fromtimestamp(int(min_datetime)).date()
            self.date2 = datetime.datetime.fromtimestamp(int(max_datetime)).date() + datetime.timedelta(days=1)

            self.dateEdit.setDate(QtCore.QDate(self.date1.year, self.date1.month, self.date1.day))
            self.dateEdit_2.setDate(QtCore.QDate(self.date2.year, self.date2.month, self.date2.day))

    def return_publish_finished(self, publish_list):
        self.auto_publish_list = publish_list
        print(self.auto_publish_list)
        self.current_web_l = publish_list
        if self.auto_publish_list:
            self.pushButton.setText("刷新")
        self.update_datetime()
        # search_words = self.textEdit.toPlainText().split("\n")
        # for item in self.auto_publish_list[self.page * self.row_limit: (self.page + 1) * self.row_limit]:
        #     if not search_words:
        #         self.current_web_l.append(item)
        #     else:
        #         for word in search_words:
        #             if word in item['domain'] and item not in self.current_web_l:
        #                 self.current_web_l.append(item)
        self.max_page = len(self.current_web_l) // self.row_limit + 1 if len(
            self.current_web_l) % self.row_limit > 0 else len(self.current_web_l) // self.row_limit
        self.table_insertion()

    def return_msg(self, msg):
        self.main_page.return_msg_update(str(msg))

    def get_current_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def filter_insert(self):        # 先过滤再插入
        print("here")
        combo_index = self.comboBox.currentIndex()
        if combo_index >= 0:
            type_id = self.job_l[combo_index]['typeid']
            self.textEdit.clear()               # 清除搜索框
            self.t_publish = PublishThread(self, type_id)
            self.t_publish.start()
            self.t_publish.msg_trigger.connect(self.return_msg)
            self.t_publish.trigger.connect(self.return_publish_finished)

    def table_insertion(self):
        print(333333333, self.current_web_l)
        self.tableWidget.setSortingEnabled(False)
        self.table_insertion_setup.main(self.current_web_l[self.row_limit * self.page: self.row_limit * (self.page + 1)])
        self.tableWidget.setSortingEnabled(True)
        self.update_labels()
        # self.tableWidget.cellDoubleClicked(1,2)

    def action_trigger(self):
        try:
            row = self.tableWidget.row
            domain = self.tableWidget.item(row, 2).text()
            for ele in self.current_web_l:
                if ele['domain'] == domain:
                    current_web_info = ele
                    break
                # else:
                #     current_web_info = self.current_web_l[self.page * self.row_limit + self.tableWidget.row]            # 如果没有找到 用这个

            self.platform_setting_ui = PlatformSetting(self.job_l, current_web_info, self.main_page, self)
            self.platform_setting_ui.show()
        except Exception as e:
            my_logger.error(e)
            logging.error(e, exc_info=True)

    def update_labels(self):
        if self.page == 0:
            self.pushButton_2.setEnabled(False)
        else:
            self.pushButton_2.setEnabled(True)
        if self.page == self.max_page - 1:
            self.pushButton_3.setEnabled(False)
        else:
            self.pushButton_3.setEnabled(True)
        self.label_2.setText(f"当前第{self.page + 1}页")

    def prev_page(self):
        self.page -= 1
        self.table_insertion()

    def next_page(self):
        self.page += 1
        self.table_insertion()

    def search_web(self):
        words = self.textEdit.toPlainText().split("\n")
        self.page = 0
        self.max_page = 0
        start_datetime = self.dateEdit.dateTime().toPyDateTime().timestamp()
        end_datetime = self.dateEdit_2.dateTime().toPyDateTime().replace(hour=23, minute=59, second=59).timestamp()
        self.current_web_l = []
        for item in self.auto_publish_list:
            if not (start_datetime <= int(item['time']) <= end_datetime):
                continue
            if not words:
                self.current_web_l.append(item)
            else:
                for word in words:
                    if word in item['domain']:
                        self.current_web_l.append(item)
        self.max_page = len(self.current_web_l) // self.row_limit + 1 if len(self.current_web_l) % self.row_limit > 0 else len(self.current_web_l) // self.row_limit
        self.table_insertion()

    def connect_slot(self):
        self.pushButton.clicked.connect(self.filter_insert)
        self.pushButton_2.clicked.connect(self.prev_page)
        self.pushButton_3.clicked.connect(self.next_page)
        # self.pushButton_4.clicked.connect(self.update_token)
        self.pushButton_4.clicked.connect(self.batch_edit)
        self.pushButton_5.clicked.connect(self.search_web)
        # self.pushButton_6.clicked.connect(self.open_remote_FTP)
        self.tableWidget.action1.triggered.connect(self.action_trigger)

    def update_token(self):
        if self.current_web_l:
            sum_l = self.get_table_checked_box()
            self.t_update_token = UpdateToken(sum_l, self.main_page)
            self.t_update_token.start()
            self.t_update_token.msg_trigger.connect(self.return_msg)
            self.t_update_token.finished_trigger.connect(self.return_update_finished)
        else:
            if self.__getattribute__('batch_edit_ui'):
                self.batch_edit_ui.hide_loading_label()

    def batch_edit(self):
        if self.current_web_l:
            sum_l = self.get_table_checked_box()
            if sum_l:
                self.batch_edit_ui = BatchEdit(self, sum_l)
                self.batch_edit_ui.show()

    def return_msg(self, msg):
        self.main_page.return_msg_update(msg)

    def return_update_finished(self, token_l, fail_l):
        self.batch_edit_ui.hide_loading_label()
        for ele in token_l:
            row = ele['row']
            update_status = ele.get('update_status')
            if update_status:
                self.current_web_l[row]['token'] = ele['new_token']
        if fail_l:
            reply = QMessageBox.information(None, 'Message', f'以下域名更新失败，请问是否重试？\n{",".join(ele["web"] for ele in fail_l)}',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.reattempt_update_token(fail_l)
            else:
                if self.batch_edit_ui and self.batch_edit_ui.isVisible():
                    self.batch_edit_ui.close_application()
        else:
            if self.batch_edit_ui and self.batch_edit_ui.isVisible():
                self.batch_edit_ui.close_application()
        self.table_insertion()

    def reattempt_update_token(self, fail_l):
        self.show_loading_label()
        self.t_update_token = UpdateToken(fail_l, self.main_page)
        self.t_update_token.start()
        self.t_update_token.msg_trigger.connect(self.return_msg)
        self.t_update_token.finished_trigger.connect(self.return_update_finished)

    def get_table_checked_box(self):
        sum_l = []
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.cellWidget(row, 0).checkbox.isChecked():
                domain = self.tableWidget.item(row, 2).text()
                for ele in self.current_web_l:
                    if ele['domain'] == domain:
                        sum_l.append(ele)
                # serial_no = int(self.tableWidget.item(row, 1).text()) - 1           # 根据排序后的序列号获取
                # row_info = self.current_web_l[self.page * self.row_limit + serial_no]           # 安全一点
                # row_info['row'] = self.page * self.row_limit + serial_no
                # sum_l.append(row_info)
        print(sum_l)
        return sum_l

    def open_remote_FTP(self):
        self.remote_FTP_ui = RemoteFTP(self.main_page, self)
        self.remote_FTP_ui.show()

    def create_loading_label(self):
        self.loading_label = QtWidgets.QLabel(self.ui)
        self.loading_label.showMaximized()
        width = self.main_page.frameGeometry().width()
        height = self.ui.frameGeometry().height()
        # self.loading_label.setGeometry(QtCore.QRect(0, 0, width//2, height//2))
        self.loading_label.setStyleSheet("background-color: rgba(255, 255, 255, 180)")
        self.loading_label.setMinimumSize(QtCore.QSize(width, height))
        self.loading_label.setMaximumSize(QtCore.QSize(width, height))
        self.loading_label.setAlignment(QtCore.Qt.AlignCenter| QtCore.Qt.AlignVCenter)
        self.loading_label.setObjectName("label")
        # self.loading_label.setText("正在加载中...")
        # self.loading_label.setStyleSheet("QLabel{font-size: 30px;background-color: #F5F5F5;}")
        # self.movie = QMovie("./docs/image/loading.gif")
        # self.movie = QMovie("")
        # self.movie.setCacheMode(QMovie.CacheAll)
        # self.loading_label.setMovie(self.movie)
        # self.movie.start()
        # self.loading_label.hide()

    def hide_loading_label(self):
        if self.loading_label.isHidden() is False:
            self.loading_label.hide()

    def show_loading_label(self):
        if self.loading_label.isVisible() is False:
            self.loading_label.show()



class JobThread(QThread):
    msg_trigger = pyqtSignal(str)
    trigger = pyqtSignal(list)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        try:
            url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_type&mode=sector'       # 获取行业， 放入comboBox中

            upper_cate_url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_init'
            job_l = requests.get(url, headers=self.ui.headers, cookies=self.ui.cookies, timeout=5).json()
            upper_cate_l = requests.get(upper_cate_url, headers=self.ui.headers, cookies=self.ui.cookies, timeout=5).json()
            for ele in job_l:
                for item in upper_cate_l:
                    if ele['typeid'] == item['typeid']:
                        if ele.get('upper_cate_info'):
                            ele['upper_cate_info'].append(item)
                        else:
                            ele['upper_cate_info'] = [item]
        except Exception as e:
            my_logger.error(e)
            print("无法连接至服务器！")
            self.msg_trigger.emit("无法连接至服务器！")
            job_l = []
        finally:
            self.trigger.emit(job_l)


class PublishThread(QThread):
    msg_trigger = pyqtSignal(str)
    trigger = pyqtSignal(list)

    def __init__(self, ui, type_id):
        super().__init__()
        self.ui = ui
        self.type_id = type_id

    def run(self):
        url = f'{self.ui.main_page.domain}/index.php?m=automatic&c=oauth&a=json_init&typeid={self.type_id}&sort={self.ui.comboBox_2.currentIndex() + 1}'
        try:
            auto_publish_list = requests.get(url, headers=self.ui.headers, cookies=self.ui.cookies).json()
        except Exception as e:
            my_logger.error(e)
            auto_publish_list = []
            self.msg_trigger.emit("无法连接至服务器！")
        finally:
            self.trigger.emit(auto_publish_list)


class UpdateToken(QThread):
    msg_trigger = pyqtSignal(str)
    finished_trigger = pyqtSignal(list, list)

    def __init__(self, token_l, main_page):
        super().__init__()
        self.main_page = main_page
        self.token_l = token_l
        self.token_api = Token()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            }
        self.session = requests.session()

    def run(self):
        unsuccessful_token_l = []
        for ele in self.token_l:
            if ele.get('token') or ele.get('token') == '':
                token = ele.get('token')
                token_url = ele.get('api')
                domain = ele.get('domain')
                client = self.token_api.generateToken(token)
                client['model'] = 'token'
                client['func'] = 'UpdateToken'
                try:
                    response = self.token_api.sendPostRequestWithToken(token_url, client)
                except Exception as e:
                    my_logger.error(e)
                    self.msg_trigger.emit(str(e))
                    unsuccessful_token_l.append(ele)
                else:
                    if response.get('status'):
                        ele['new_token'] = response.get('msg')
                        self.update_token(ele)
                        self.msg_trigger.emit(f"域名{domain}, Token更新成功！")
                    else:
                        self.msg_trigger.emit(f"域名{domain}, 更新失败, 错误信息: {response.get('msg')}")
            else:
                domain = ele.get('domain')
                self.msg_trigger.emit(f"域名{domain}, 更新失败, 错误信息: 域名: {ele['domain']} - 未检测到Token值")
        self.finished_trigger.emit(self.token_l, unsuccessful_token_l)            # 用于表更新

    def update_token(self, token_d):         # 更新token
        url = f'{self.main_page.domain}/index.php?m=automatic&json=1&c=automatic_admin&a=edit&id={token_d["id"]}'
        data = {}
        data['data[token]'] = token_d['new_token']
        data['dosubmit'] = ''
        data['pc_hash'] = self.main_page.pc_hash
        update_res = self.session.post(url, headers=self.headers, cookies=self.main_page.cookies, data=data).json()
        if update_res.get('msg') == '成功！':
            token_d['update_status'] = True
        else:
            token_d['update_status'] = False


