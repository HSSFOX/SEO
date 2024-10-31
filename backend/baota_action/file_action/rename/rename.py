from frontend.baota_action.file_action.rename.rename import Ui_Form
from api_requests.BtAPI import Bt
from model.utils import my_logger
import datetime
import logging
from PyQt5.QtCore import *
import os


class Rename(Ui_Form):
    def __init__(self, page, parent_ui, main_page):
        super().setupUi(page)
        self.page = page
        self.parent_ui = parent_ui
        self.main_page = main_page
        self.default_path = ''
        self.connect_slot()

    def rename(self):
        if self.lineEdit_2.text().strip() != "":     # 文件名重命名
            if self.parent_ui.current_bt_cate_sites_info:
                new_file_name = self.lineEdit_2.text()
                path_folder_file = self.comboBox_2.currentText()
                self.t_rename = RenameThread(self, path_folder_file, new_file_name)
                self.t_rename.start()
                self.t_rename.msg_trigger.connect(self.main_page.return_msg_update)
                self.t_rename.finished.connect(self.refresh_path)
                # self.rename_file(self.comboBox_2.currentText(), new_file_name)
            else:
                self.main_page.return_msg_update("未获取到分类下属站点信息，请稍后再试！")
        else:
            self.main_page.return_msg_update("请填入有效路径！")

    def rename_file(self, orl_file_name, new_file_name):
        basename = os.path.basename(orl_file_name)
        params = {'sfile': f'{orl_file_name}', 'dfile': f'{orl_file_name.replace(basename, new_file_name)}', 'rename': True}
        print(params)
        res = self.main_page.bt.move_file(params)
        print(res)
        return res

    def refresh_path(self):
        self.parent_ui.files_search_sign = False
        self.get_default_init_path()                # 更新一遍路径

    def get_current_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def connect_slot(self):
        self.pushButton.clicked.connect(self.rename)
        self.pushButton_2.clicked.connect(self.get_default_init_path)
        self.comboBox.currentIndexChanged.connect(self.update_path_by_folders_files)

    def update_path_by_folders_files(self):
        self.comboBox_2.clear()
        if self.comboBox.currentIndex() == 0:
            self.comboBox_2.addItems(self.parent_ui.folder_l)
        else:
            self.comboBox_2.addItems(self.parent_ui.file_l)
        # if self.main_page.bt_sign:
        #     print(self.parent_ui.files_search_sign, self.comboBox.currentIndex())
        #     if self.comboBox.currentIndex() and self.parent_ui.files_search_sign:
        #         self.comboBox_2.clear()
        #         self.comboBox_2.addItems(self.parent_ui.file_l)
        #     elif not self.comboBox.currentIndex() and self.parent_ui.files_search_sign:
        #         self.comboBox_2.clear()
        #         self.comboBox_2.addItems(self.parent_ui.folder_l)
        #     else:
        #         self.main_page.return_msg_update("请先重新搜索文件夹更新路径！")
        # else:
        #     self.main_page.return_msg_update('请先登录宝塔！')

    def get_default_init_path(self):
        if self.main_page.bt_sign:
            if self.parent_ui.current_bt_cate_sites_info:
                self.default_path = self.parent_ui.current_bt_cate_sites_info[0]['path']
                print("?????", self.default_path)
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
    #         self.finish_trigger.emit(res)
    #     else:
    #         self.msg_trigger.emit("未找到相关目录下的文件")


class RenameThread(QThread):
    msg_trigger = pyqtSignal(str)

    def __init__(self, ui, path_folder_file, file_name):
        super().__init__()
        self.ui = ui
        self.path_folder_file = path_folder_file
        self.file_name = file_name

    def run(self):
        for site_info in self.ui.parent_ui.current_bt_cate_sites_info:
            current_path = site_info['path'] + "/" + self.path_folder_file
            res = self.ui.rename_file(current_path, self.file_name)
            if res.get('status'):
                self.msg_trigger.emit(f"{site_info['name']} 重命名成功！")
            else:
                self.msg_trigger.emit(f"{site_info['name']} 重命名失败！错误消息: {res['msg']}")

        self.msg_trigger.emit(f"所有任务已执行完毕！")