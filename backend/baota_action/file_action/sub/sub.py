from frontend.baota_action.file_action.sub.sub import Ui_Form
from model.utils import my_logger
import datetime
import logging
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Sub(Ui_Form):
    def __init__(self, page, parent_ui, main_page):
        super().setupUi(page)
        self.page = page
        self.parent_ui = parent_ui
        self.main_page = main_page
        self.connect_slot()

    def get_default_init_path(self):
        if self.main_page.bt_sign:
            if self.parent_ui.current_bt_cate_sites_info:
                if not self.parent_ui.files_search_sign:  # 仅没搜索过的情况下去再搜索一遍，分类更变后重置
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

    def start_sub(self):
        if self.main_page.bt_sign:
            if self.parent_ui.files_search_sign:
                if self.parent_ui.current_bt_cate_sites_info:
                    # content = self.textEdit.toPlainText()
                    # file_name = self.lineEdit.text()
                    # path_location = self.comboBox.currentText()
                    # self.t_start_task = CreateFileThread(self.main_page, content, file_name, path_location, self)
                    # self.t_start_task.start()
                    # self.t_start_task.finish_trigger.connect(self.main_page.return_msg_update)
                    # self.t_start_task.finished.connect(self.refresh_search)

                    original_content = self.textEdit.toPlainText().strip()
                    sub_content = self.textEdit_2.toPlainText()
                    path_location = self.comboBox.currentText()

                    if original_content:
                        reply = QMessageBox.question(None, '文本替换', '替换后将无法撤回，请问是否确认替换该字段？',
                                                     QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            self.t_start_sub = SubThread(self, original_content, sub_content, path_location, self.checkBox.isChecked())
                            self.t_start_sub.start()
                            self.t_start_sub.msg_trigger.connect(self.main_page.return_msg_update)
                    else:
                        self.main_page.return_msg_update('内容文本不可为空或者为空格！请输入要替换的文件内容文本！')
                else:
                    self.main_page.return_msg_update("未获取到分类下属站点信息，请稍后再试！")
            else:
                self.main_page.return_msg_update("请先重新搜索文件夹更新路径！")
        else:
            self.main_page.return_msg_update("请先登录宝塔！")

    def connect_slot(self):
        self.pushButton.clicked.connect(self.get_default_init_path)
        self.pushButton_2.clicked.connect(self.start_sub)


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


class SubThread(QThread):
    msg_trigger = pyqtSignal(str)

    def __init__(self, ui, original_content, sub_content, path, replace_all_flag):
        super().__init__()
        self.ui = ui
        self.main_page = ui.main_page
        self.original_content = original_content
        self.sub_content = sub_content
        self.path = path
        self.replace_all_flag = replace_all_flag

    def run(self):
        for site_info in self.ui.parent_ui.current_bt_cate_sites_info:
            current_path = site_info['path'] + self.path
            params = {'path': current_path}
            get_res = self.main_page.bt.get_file_body(params)
            print(get_res)
            if get_res.get('status'):
                if get_res['data']:
                    if self.original_content in get_res['data']:
                        new_content = self.replace_content(get_res['data'])
                        print(get_res['st_mtime'])
                        params = {'path': current_path, 'data': new_content, 'encoding': 'utf-8', 'force': 1}
                        save_res = self.main_page.bt.save_file_body(params)
                        if save_res.get('status'):
                            self.msg_trigger.emit(site_info['path'] + "文件内容替换成功！")
                        else:
                            self.msg_trigger.emit(site_info['path'] + save_res.get('msg'))
                    else:
                        self.msg_trigger.emit(site_info['path'] + "文件无匹配内容！")
                else:
                    self.msg_trigger.emit(site_info['path'] + "文件无内容！")
            else:
                self.msg_trigger.emit(site_info['path'] + get_res.get('msg'))

    def replace_content(self, content):
        if self.replace_all_flag:
            return content.replace(self.original_content, self.sub_content)
        else:
            return content.replace(self.original_content, self.sub_content, 1)