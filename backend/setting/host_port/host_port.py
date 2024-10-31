import os
import re

from frontend.setting.host_port.host_port import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
import configparser
import requests
from model.utils import my_logger
from PyQt5.QtWidgets import *


class HostPort(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui):
        super().__init__()
        self.setupUi(self)
        self.ui = ui
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint|QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.WindowCloseButtonHint)
        self.set_init_values()
        self.pushButton_2.setEnabled(False)
        self.connect_slot()

    def set_init_values(self):
        config = configparser.ConfigParser()
        try:
            config.read('/config/login_config.ini')  # 读取 config.ini 文件
            if config.has_section('Domain'):
                self.lineEdit.setText(config.get('Domain', 'host_port'))
        except Exception as e:
            print(str(e))

    def save(self):
        config = configparser.ConfigParser()
        if not os.path.exists('config'):
            os.makedirs('config')
        try:
            config.read('config/login_config.ini')  # 读取 config.ini 文件
            if not config.has_section('Domain'):
                config.add_section('Domain')
        except Exception as e:
            print(str(e))
        finally:
            # 设置键值对
            host_port = self.lineEdit.text()
            config.set('Domain', 'host_port', host_port + "\\")
        with open('config/login_config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        self.close()
        self.ui.init_detect_connection()            # 重新检测更新

    def check_connection(self):
        host_port = self.lineEdit.text()
        # status = self.check_match(host_port)
        status = self.re_match(host_port)
        if not status:
            QMessageBox.warning(self, '警告', "url不符合规则！", QMessageBox.Ok)
        else:
            try:
                res = requests.get(host_port, timeout=3).json()
                print(res)
            except Exception as e:
                my_logger.error(e)
                QMessageBox.question(self, '连接检测', '连接失败！', QMessageBox.Yes)
            else:
                reply = QMessageBox.question(self, '连接检测', '连接成功！', QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.pushButton_2.setEnabled(True)

    def check_match(self, url):
        #     hostname_regex = r'^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$' # 匹配主机名
        pattern = re.compile(r'^(http|https)://[a-zA-Z0-9\-\.]+\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')
        # pattern = re.compile(r"^(http|https)://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?:/[^/#?]+)+\.(?:com|[0-9]/)$")
        if re.match(pattern, url):
            return True
        else:
            return False

    def re_match(self, url):
        url_regex = r'^(?:http|ftp)s?://'  # 匹配http或https或ftp或ftps开头的字符串
        hostname_regex = r'^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'  # 匹配主机名
        return bool(re.match(url_regex, url, re.IGNORECASE)) or bool(re.match(hostname_regex, url))

    def host_port_changed(self):
        self.pushButton_2.setEnabled(False)

    def connect_slot(self):
        self.pushButton.clicked.connect(self.check_connection)
        self.pushButton_2.clicked.connect(self.save)

        self.lineEdit.textChanged.connect(self.host_port_changed)

