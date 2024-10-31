from frontend.baota_action.file_action.upload.upload import Ui_Form
from api_requests.BtAPI import Bt
import tkinter as tk
from tkinter import filedialog, Tk
from os import startfile
import os
from model.utils import my_logger
import datetime
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import logging


class Upload(Ui_Form):
    def __init__(self, page, parent_ui, main_page):
        super().setupUi(page)
        self.page = page
        self.parent_ui = parent_ui
        self.main_page = main_page
        self.default_path = ''
        self.connect_slot()

    def upload_single_file(self):
        try:
            file = self.lineEdit.text()            # 文件上传 文件名
            if not os.path.exists(file):
                self.main_page.return_msg_update(f"请确认该文件 {file} 是否存在！")
                return
            path_path = self.comboBox.currentText()
        except Exception as e:
            my_logger.log(e)
            self.main_page.return_msg_update(str(e))
        else:
            self.upload_by_api([file], path_path, cover=self.checkBox.isChecked())

    def batch_upload_files(self):
        if self.main_page.bt_sign:
            if self.parent_ui.files_search_sign:
                try:
                    file = self.lineEdit_2.text()
                    if not os.path.exists(file):
                        self.main_page.return_msg_update(f"请确认该文件 {file} 是否存在！")
                        return
                    path_path = self.comboBox.currentText()
                    files_list, folders_list = self.dfs([], [], file)          # 获取这个文件夹下所有的文件, 如果还有文件夹就继续搜索文件
                except Exception as e:
                    my_logger.log(e)
                    self.main_page.return_msg_update("非有效路径")
                else:
                    folder_path = file
                    self.upload_by_api(files_list, path_path, folder_path, cover=self.checkBox.isChecked())
            else:
                self.main_page.return_msg_update("请先重新搜索文件夹更新路径！")
        else:
            self.main_page.return_msg_update("请先登录宝塔！")

    def upload_by_api(self, file_list, target_path, folder_path='', cover=True):        # params为单个param组成的list
        if self.parent_ui.current_bt_cate_sites_info:
            self.upload_files_t = UploadThread(self, self.main_page, file_list, target_path, folder_path, cover)
            self.upload_files_t.start()
            self.upload_files_t.msg_trigger.connect(self.main_page.return_msg_update)
            self.upload_files_t.finished_trigger.connect(self.return_upload_thread_finished_trigger)
            self.pushButton.setEnabled(False)       # ban掉上传按钮，避免重复点击导致同一QThread多开导致的Crash
            self.pushButton_2.setEnabled(False)
        else:
            self.main_page.return_msg_update("未获取到分类下属站点信息，请稍后再试！")

    def return_upload_thread_finished_trigger(self):
        self.main_page.return_msg_update("全部执行完毕！")
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.parent_ui.files_search_sign = False
        self.get_default_init_path()                # 更新一遍路径

    def get_current_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def connect_slot(self):
        self.pushButton.clicked.connect(self.upload_single_file)
        self.pushButton_2.clicked.connect(self.batch_upload_files)       # 暂无upload files api
        self.pushButton_3.clicked.connect(self.open_file)
        self.pushButton_4.clicked.connect(self.open_folder)
        self.pushButton_5.clicked.connect(self.get_default_init_path)

    def get_folders(self, root_path, folders_list):
        l = []
        for folder_path in folders_list:
            l.append(root_path + folder_path.split("/")[-1])
        return l

    def open_file(self):
        root = Tk()
        root.withdraw()  # 隐藏主窗口，因为不需要显示整个窗口，只显示文件选择对话框
        file_path = filedialog.askopenfilename()  # 用户选择文件后，文件路径会被存储在file_path变量中
        if file_path:  # 如果用户选择了文件
            self.lineEdit.setText(file_path)

    def open_folder(self):          # 打开文件夹使用
        root = Tk()
        root.withdraw()  # 隐藏主窗口，因为不需要显示整个窗口，只显示文件选择对话框
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.lineEdit_2.setText(folder_selected)

    def dfs(self, file_list, folder_list, init_folder):
        for f in os.listdir(init_folder):
            if os.path.isfile(os.path.join(init_folder, f)):
                file_list.append(os.path.join(init_folder, f))
            else:
                folder_list.append(os.path.join(init_folder, f))
                self.dfs(file_list, folder_list, os.path.join(init_folder, f))
        return file_list, folder_list

    def get_default_init_path(self):
        if self.main_page.bt_sign:
            if self.parent_ui.current_bt_cate_sites_info:
                self.default_path = self.parent_ui.current_bt_cate_sites_info[0]['path']
                print(self.default_path)
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
        self.pushButton_3.setEnabled(status)
        self.pushButton_4.setEnabled(status)
        self.pushButton_5.setEnabled(status)
        if status:
            self.pushButton_5.setText("搜索")
        else:
            self.pushButton_5.setText("获取中...")

    def return_finish_from_get_files(self, folder_files):
        self.update_button_status(True)
        self.parent_ui.files_search_sign = True
        self.parent_ui.update_files_check([ele['nm'] for ele in folder_files['dir']], [ele['nm'] for ele in folder_files['files']])


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


class UploadThread(QThread):
    msg_trigger = pyqtSignal(str)
    finished_trigger = pyqtSignal()

    def __init__(self, ui, main_page, file_list, target_path, folder_path, cover):
        super().__init__()
        self.ui = ui
        self.main_page = main_page
        self.file_list = file_list
        self.target_path = target_path
        print(folder_path)
        self.folder_path = folder_path.split("/")[-1]
        self.cover = cover

    def run(self):
        for site_info in self.ui.parent_ui.current_bt_cate_sites_info:
            for file in self.file_list:
                print("file: ", file)
                current_path = site_info['path'] + self.target_path
                print("path: ", current_path)
                if self.folder_path:
                    basename = os.path.basename(file)
                    current_path += "/" + file.split("/")[-1].replace(basename, '').strip("\\").replace("\\", "/")
                params = {'f_path': current_path, 'f_name': os.path.basename(file), 'f_size': os.path.getsize(file), 'f_start': 0, 'blob': file}
                print("params: ", params)
                try:
                    res = self.main_page.bt.upload_file(params, self.cover)
                    print("res: ", res)
                except Exception as e:
                    my_logger.log(str(e))
                else:
                    if isinstance(res, dict):
                        self.msg_trigger.emit(f"{params['f_path']} {params['f_name']}, {str(res['msg'])}")
                    else:
                        self.msg_trigger.emit(f"{params['f_name']} 发布失败！请稍后重试")

        self.finished_trigger.emit()




