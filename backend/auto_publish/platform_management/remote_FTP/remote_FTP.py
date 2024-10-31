from PyQt5.QtWidgets import *
from frontend.auto_publish.platforms_management.remote_FTP.remote_FTP import Ui_Form
from PyQt5.QtCore import QTime
import requests
import json




class RemoteFTP(QWidget, Ui_Form):
    def __init__(self, main_page, ui):
        super().__init__()
        self.setupUi(self)
        self.main_page = main_page          # 总主页面
        self.ui = ui                        # 父页面 just in case

    # def get_ftp_setting(self):
        # url = 'http://192.168.110.12:5001/index.php?m=automatic&c=automatic_admin&a=RDS_edit&id=1'







