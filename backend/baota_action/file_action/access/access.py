from frontend.baota_action.file_action.access.access import Ui_Form
from api_requests.BtAPI import Bt
from model.utils import my_logger
import datetime
from PyQt5.QtCore import *
import logging


class Access(Ui_Form):
    def __init__(self, page, parent_ui, main_page):
        super().setupUi(page)
        self.page = page
        self.parent_ui = parent_ui
        self.main_page = main_page
        self.connect_slot()

    def get_3_access_code(self):
        sum_code = self.get_access_code(self.checkBox_2, self.checkBox_3, self.checkBox_4) + self.get_access_code(self.checkBox_5, self.checkBox_6, self.checkBox_7) + self.get_access_code(self.checkBox_8, self.checkBox_9, self.checkBox_10)
        # 权限码
        return sum_code

    def get_access_code(self, cb_0, cb_1, cb_2):
        if cb_0.isChecked() and cb_1.isChecked() and cb_2.isChecked():
            return "7"
        elif cb_0.isChecked() and cb_1.isChecked() and not cb_2.isChecked():
            return "6"
        elif cb_0.isChecked() and not cb_1.isChecked() and cb_2.isChecked():
            return "5"
        elif not cb_0.isChecked() and cb_1.isChecked() and cb_2.isChecked():
            return "3"
        elif cb_0.isChecked() and not cb_1.isChecked() and not cb_2.isChecked():
            return "4"
        elif not cb_0.isChecked() and cb_1.isChecked() and not cb_2.isChecked():
            return "2"
        elif not cb_0.isChecked() and not cb_1.isChecked() and cb_2.isChecked():
            return "1"
        else:
            return "0"

    def update_access(self):
        code = self.get_3_access_code()
        filename = self.comboBox.currentText()
        if filename:
            son_path = True if self.checkBox.isChecked() else False      # 应用到子目录

            if self.parent_ui.current_bt_cate_sites_info:
                self.t_access = UpdateAccess(self, code, son_path, filename)
                self.t_access.start()
                self.t_access.msg_trigger.connect(self.main_page.return_msg_update)

                # self.t_rename = RenameThread(self, path_folder_file, new_file_name)
                # self.t_rename.start()
                # self.t_rename.msg_trigger.connect(self.main_page.return_msg_update)
                # self.t_rename.finished.connect(self.refresh_path)
                # # self.rename_file(self.comboBox_2.currentText(), new_file_name)
            else:
                self.main_page.return_msg_update("未获取到分类下属站点信息，请稍后再试！")
        else:
            self.main_page.return_msg_update("请确认文件路径！")


    def check_box_changed(self):
        self.lineEdit_2.setText(str(self.get_3_access_code()))

    # def code_changed(self):
    #     code_str = self.lineEdit_2.text()
    #     print(1111, code_str)
    #     try:
    #         code = int(code_str)
    #     except Exception as e:
    #         my_logger.error(e)
    #     else:
    #         l = [[self.checkBox_8, self.checkBox_9, self.checkBox_10],
    #              [self.checkBox_5, self.checkBox_6, self.checkBox_7],
    #              [self.checkBox_2, self.checkBox_3, self.checkBox_4]]
    #         for i in range(3):
    #             res = code % 10
    #             print(22222, res)
    #             if res:
    #                  self.set_check_box(l[i][0], l[i][1], l[i][2], res)

    # def set_check_box(self, cb1, cb2, cb3, num):
    #    if num == 7:
    #        cb1.setChecked(True)
    #        cb2.setChecked(True)
    #        cb3.setChecked(True)
    #    elif num == 6:
    #        cb1.setChecked(True)
    #        cb2.setChecked(True)
    #        cb3.setChecked(False)
    #    elif num == 5:
    #        cb1.setChecked(True)
    #        cb2.setChecked(False)
    #        cb3.setChecked(True)
    #    elif num == 3:
    #        cb1.setChecked(False)
    #        cb2.setChecked(True)
    #        cb3.setChecked(True)
    #    elif num == 4:
    #        cb1.setChecked(True)
    #        cb2.setChecked(False)
    #        cb3.setChecked(False)
    #    elif num == 2:
    #        cb1.setChecked(False)
    #        cb2.setChecked(True)
    #        cb3.setChecked(False)
    #    elif num == 1:
    #        cb1.setChecked(False)
    #        cb2.setChecked(False)
    #        cb3.setChecked(True)
    #    elif num == 0:
    #        cb1.setChecked(False)
    #        cb2.setChecked(False)
    #        cb3.setChecked(False)

    def connect_slot(self):
        self.pushButton.clicked.connect(self.update_access)
        self.pushButton_2.clicked.connect(self.get_default_init_path)
        self.checkBox_2.toggled.connect(self.check_box_changed)
        self.checkBox_3.toggled.connect(self.check_box_changed)
        self.checkBox_4.toggled.connect(self.check_box_changed)
        self.checkBox_5.toggled.connect(self.check_box_changed)
        self.checkBox_6.toggled.connect(self.check_box_changed)
        self.checkBox_7.toggled.connect(self.check_box_changed)
        self.checkBox_8.toggled.connect(self.check_box_changed)
        self.checkBox_9.toggled.connect(self.check_box_changed)
        self.checkBox_10.toggled.connect(self.check_box_changed)
        # self.lineEdit_2.textChanged.connect(self.code_changed)

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
    #     print(self.current_path)
    #     print(res)
    #     if res.get('dir'):
    #         for ele in res['dir']:
    #             if not ele['nm'].startswith("/"):
    #                 ele['nm'] = "/" + ele['nm']
    #         self.finish_trigger.emit(res)
    #     else:
    #         self.msg_trigger.emit("未找到相关目录下的文件")


class UpdateAccess(QThread):
    msg_trigger = pyqtSignal(str)

    def __init__(self, ui, code, son_path, file_path):
        super().__init__()
        self.ui = ui
        self.code = code
        self.son_path = son_path
        self.file_path = file_path

    def run(self):
        for site_info in self.ui.parent_ui.current_bt_cate_sites_info:
            current_path = site_info['path'] + "/" + self.file_path
            try:
                params = {'filename': current_path, 'user': 'www', 'access': self.code, 'all': self.son_path}
                print(params)
                res = self.ui.main_page.bt.set_file_access(params)
                my_logger.info(current_path + res['msg'])
            except Exception as e:
                my_logger.error(e)
            else:
                self.msg_trigger.emit(current_path + res['msg'])
        self.msg_trigger.emit("所有任务执行完毕！")

