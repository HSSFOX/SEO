from frontend.baota_action.file_action.create.create import Ui_Form
import requests
import json
import time
from model.utils import my_logger
import datetime
import logging
from PyQt5.QtCore import *


class Create(Ui_Form):
    def __init__(self, page, parent_ui, main_page):
        super().setupUi(page)
        self.page = page
        self.parent_ui = parent_ui
        self.main_page = main_page
        self.default_path = ''
        # self.get_default_init_path()
        self.connect_slot()

    def start_task(self):
        if self.main_page.bt_sign:
            if self.parent_ui.files_search_sign:
                if self.parent_ui.current_bt_cate_sites_info:
                    content = self.textEdit.toPlainText()
                    file_name = self.lineEdit.text()
                    path_location = self.comboBox.currentText()
                    self.t_start_task = CreateFileThread(self.main_page, content, file_name, path_location, self)
                    self.t_start_task.start()
                    self.t_start_task.finish_trigger.connect(self.main_page.return_msg_update)
                    self.t_start_task.finished.connect(self.refresh_search)
                else:
                    self.main_page.return_msg_update("未获取到分类下属站点信息，请稍后再试！")
            else:
                self.main_page.return_msg_update("请先重新搜索文件夹更新路径！")
        else:
            self.main_page.return_msg_update("请先登录宝塔！")

    def refresh_search(self):
        self.parent_ui.files_search_sign = False
        self.get_default_init_path()

    def get_current_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_file_content(self, content, full_file_path):
        timestamp = int(time.time())
        params = {'path': full_file_path, 'data': content, 'encoding': 'utf-8', 'st_mtime': timestamp, 'force': 1}
        res = self.main_page.bt.save_file_body(params)
        self.main_page.return_msg_update(full_file_path + " : " + res['msg'])
        my_logger.info(res['msg'])

    def create_file(self, file_name, root_path):
        params = {'path': root_path, 'file_name': file_name}
        print(params)
        res = self.main_page.bt.new_file(params)
        self.main_page.return_msg_update(root_path + file_name + " : " + res['msg'])
        my_logger.info(res['msg'])

    def connect_slot(self):
        self.pushButton.clicked.connect(self.start_task)
        self.pushButton_2.clicked.connect(self.get_default_init_path)
        # self.comboBox.currentIndexChanged.connect(self.comboBoxChanges)

    def get_default_init_path(self):
        if self.main_page.bt_sign:
            if self.parent_ui.current_bt_cate_sites_info:
                if not self.parent_ui.files_search_sign:                    # 仅没搜索过的情况下去再搜索一遍，分类更变后重置
                    self.default_path = self.parent_ui.current_bt_cate_sites_info[0]['path']
                    self.get_files_under_path()
            else:
                self.main_page.return_msg_update('该分类下无网站！')
        else:
            self.main_page.return_msg_update('请先登录宝塔！')

    def get_files_under_path(self):
        try:
            self.update_button_status(False)
            current_path = self.default_path
            self.t_get_files_under_path = GetFilesUnderPathThread(self.main_page, current_path)
            self.t_get_files_under_path.start()
            self.t_get_files_under_path.msg_trigger.connect(self.main_page.return_msg_update)
            self.t_get_files_under_path.finish_trigger.connect(self.return_finish_from_get_files)
        except Exception as e:
            logging.error(e, exc_info=True)

    def update_button_status(self, status):
        self.pushButton.setEnabled(status)
        self.pushButton_2.setEnabled(status)
        if status:
            self.pushButton_2.setText("搜索")
        else:
            self.pushButton_2.setText("获取中...")

    def return_finish_from_get_files(self, folder_files):
        self.update_button_status(True)
        self.parent_ui.files_search_sign = True
        self.parent_ui.update_files_check([ele['nm'] for ele in folder_files['dir']], [ele['nm'] for ele in folder_files['files']])
        # self.parent_ui.folder_l = [''] + [ele['nm'] for ele in folder_files['dir']]
        # self.parent_ui.file_l = [''] + [ele['nm'] for ele in folder_files['files']]


class GetFilesUnderPathThread(QThread):
    finish_trigger = pyqtSignal(dict)
    msg_trigger = pyqtSignal(str)

    def __init__(self, main_page, current_path):
        super().__init__()
        self.main_page = main_page
        self.current_path = current_path
        self.page_limit = 2000
        self.search_sign = True

    def run(self):
        return_dl = {'dir': [], 'files': [], 'path': ''}
        page = 1
        while self.search_sign:
            if self.main_page.bt_patch:
                dir_files_dl = self.search_btv2(page)
            else:
                dir_files_dl = self.search_btV1(page)
            if (not dir_files_dl.get('dir') and not dir_files_dl.get('files')) or len(dir_files_dl['dir']) + len(dir_files_dl['files']) < 2000:
                self.search_sign = False
            else:
                page += 1
            return_dl['dir'] += dir_files_dl['dir']
            return_dl['files'] += dir_files_dl['files']
            return_dl['path'] = dir_files_dl['path']
        if not return_dl['dir'] and not return_dl['files']:
            self.msg_trigger.emit("未找到相关目录下的文件")
        self.finish_trigger.emit(return_dl)

    def search_btv2(self, page):
        return_d = {'dir': [], 'files': [], 'path': ''}
        res = self.main_page.bt.get_dir_files(
            {'path': self.current_path, 'search': '', 'all': True, 'showRow': self.page_limit, 'p': page})
        if res.get('DIR'):
            return_d['dir'] = [{'nm': "/" + ele.split(";")[0]} for ele in res['DIR']]
            return_d['files'] = [{'nm': "/" + ele.split(";")[0]} for ele in res['FILES']]
            return_d['path'] = res['PATH']
        return return_d

    def search_btV1(self, page):
        res = self.main_page.bt.search_file(
            {'path': self.current_path, 'search': '', 'all': True, 'showRow': self.page_limit, 'p': page})
        if res.get('dir'):
            # print(len(res['dir']))
            # print(len(res['files']))
            for ele in res['dir']:
                if not ele['nm'].startswith("/"):
                    ele['nm'] = "/" + ele['nm']
            for ele in res['files']:
                if not ele['nm'].startswith("/"):
                    ele['nm'] = "/" + ele['nm']
        return res
    # def __init__(self, main_page, current_path):
    #     super().__init__()
    #     self.main_page = main_page
    #     self.current_path = current_path
    #
    # def run(self):
    #     res = self.main_page.bt.search_file({'path': self.current_path, 'search': '', 'all': True})
    #     if res.get('dir'):
    #         for ele in res['dir']:
    #             if not ele['nm'].startswith("/"):
    #                 ele['nm'] = "/" + ele['nm']
    #         for ele in res['files']:
    #             if not ele['nm'].startswith("/"):
    #                 ele['nm'] = "/" + ele['nm']
    #         self.finish_trigger.emit(res)
    #     else:
    #         self.msg_trigger.emit("未找到相关目录下的文件")


class CreateFileThread(QThread):
    finish_trigger = pyqtSignal(str)

    def __init__(self, main_page, content, file_name, path_location, ui):
        super().__init__()
        self.main_page = main_page
        self.content = content
        self.file_name = file_name
        self.ui = ui
        self.path_location = path_location

    def run(self):
        for site_info in self.ui.parent_ui.current_bt_cate_sites_info:
            current_path = site_info['path'] + self.path_location + "/"
            print(current_path)
            try:
                self.ui.create_file(self.file_name, current_path)
                self.ui.save_file_content(self.content, current_path + self.file_name)
            except Exception as e:
                logging.error(e, exc_info=True)
        self.finish_trigger.emit("任务已执行完毕！")
