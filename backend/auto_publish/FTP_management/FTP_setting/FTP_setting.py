from frontend.auto_publish.FTP_management.FTP_setting.FTP_setting import Ui_Form
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests


class FtpSetting(QWidget, Ui_Form):
    def __init__(self, ui, ftp_setting, add=False):
        super().__init__()
        self.setupUi(self)
        self.ui = ui
        self.ftp_setting = ftp_setting
        self.add_sign = add
        self.set_default_value()

        # {	'ftp_enable': '1',
        # 	'ftp_host': '182.106.136.175',
        # 	'ftp_password': '7sPmwJDyscym5GBA',
        # 	'ftp_pasv': '0',
        # 	'ftp_path': '/',
        # 	'ftp_port': '21',
        # 	'ftp_user': 'Updowns',
        # 	'id': '1',
        # 	'siteid': '1'}
        self.connect_slot()

    def set_default_value(self):
        self.textEdit.setReadOnly(True)
        if not self.add_sign:
            if self.ftp_setting['ftp_enable'] == '1':
                self.radioButton.setChecked(True)
            else:
                self.radioButton_2.setChecked(True)
            if self.ftp_setting['ftp_pasv'] == '0':
                self.radioButton_4.setChecked(True)
            else:
                self.radioButton_3.setChecked(True)

            self.lineEdit.setText(self.ftp_setting['ftp_host'])
            self.lineEdit_2.setText(self.ftp_setting['ftp_user'])
            self.lineEdit_3.setText(self.ftp_setting['ftp_password'])
            self.lineEdit_4.setText(self.ftp_setting['ftp_port'])
            self.lineEdit_5.setText(self.ftp_setting['ftp_path'])
            self.textEdit.setText(self.ftp_setting['analyzed'])

    def check_radio_button(self, radio_button_l):           # 返回被check的radio_button在同一list中radio_button的index
        for i, r in enumerate(radio_button_l):
            if r.isChecked():
                return i
        else:
            return 0            # 没有的话返回默认的0

    def radio_auto_exclusive(self, radio_button):
        if radio_button.isChecked():
            if radio_button == self.radioButton or radio_button == self.radioButton_2:
                self.radio_box_exclusive(radio_button, [self.radioButton, self.radioButton_2])
            elif radio_button == self.radioButton_3 or radio_button == self.radioButton_4:
                self.radio_box_exclusive(radio_button, [self.radioButton_3, self.radioButton_4])
        else:           # 确认在一个自定义范围内的radio button不可以被直接点掉导致无radio button被选择
            if radio_button == self.radioButton or radio_button == self.radioButton_2:
                self.check_rest_uncheck(radio_button, [self.radioButton, self.radioButton_2])
            elif radio_button == self.radioButton_3 or radio_button == self.radioButton_4:
                self.check_rest_uncheck(radio_button, [self.radioButton_3, self.radioButton_4])

    def radio_box_exclusive(self, checked_radio_box, radio_boxes_l):
        if checked_radio_box in radio_boxes_l and checked_radio_box.isChecked():
            radio_boxes_l.remove(checked_radio_box)
            for radio_box in radio_boxes_l:
                radio_box.setChecked(False)

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
        self.pushButton.clicked.connect(self.save_ftp)

    def save_ftp_setting_in_thread(self):
        try:
            if self.add_sign:
                url = f'{self.ui.main_page.domain}/index.php?m=automatic&c=automatic_admin&a=RDS_ADD&id={self.ftp_setting["id"]}&json=1'
            else:
                url = f'{self.ui.main_page.domain}/index.php?m=automatic&c=automatic_admin&a=RDS_edit&id={self.ftp_setting["id"]}&json=1'
            params = {'dosubmit': '', 'pc_hash': self.ui.main_page.pc_hash}
            params.update(self.get_ftp_setting())
            res = requests.post(url, headers=self.ui.main_page.headers, cookies=self.ui.main_page.cookies, data=params).json()
            print(res)
            if '成功！' in res['msg']:
                return True
            else:
                return False
        except Exception as e:
            return False

    def save_ftp(self):
        self.t_save_ftp_setting = SaveThread(self)
        self.t_save_ftp_setting.start()
        self.t_save_ftp_setting.msg_trigger.connect(self.ui.main_page.return_msg_update)
        self.t_save_ftp_setting.finished.connect(self.return_finish_save_ftp)

    def return_finish_save_ftp(self):
        self.close()
        self.ui.search_all()

    def get_ftp_setting(self):
        ftp_d = {}
        ftp_d['data[ftp_enable]'] = '1' if self.radioButton.isChecked() else '0'
        ftp_d['data[ftp_pasv]'] = '1' if self.radioButton_3.isChecked() else '0'
        ftp_d['data[ftp_host]'] = self.lineEdit.text()
        ftp_d['data[ftp_user]'] = self.lineEdit_2.text()
        ftp_d['data[ftp_password]'] = self.lineEdit_3.text()
        ftp_d['data[ftp_port]'] = self.lineEdit_4.text() if self.lineEdit_4.text() else '21'
        ftp_d['data[ftp_path]'] = self.lineEdit_5.text() if self.lineEdit_5.text() else '/'
        ftp_d['data[analyzed]'] = self.textEdit.toPlainText()
        return ftp_d


class SaveThread(QThread):
    msg_trigger = pyqtSignal(str)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        status = self.ui.save_ftp_setting_in_thread()
        if status:
            self.msg_trigger.emit("FTP设置修改成功！")
        else:
            self.msg_trigger.emit("FTP设置修改失败！")
