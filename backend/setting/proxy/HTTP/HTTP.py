
from frontend.setting.proxy.HTTP.HTTP import Ui_Form
import requests
import webbrowser
from PyQt5.QtWidgets import QMessageBox
import configparser
import logging


class UI_HTTP(Ui_Form):
    def __init__(self, page, proxy_page):
        super().setupUi(page)
        self.page = page
        self.proxy_page = proxy_page

        self.pushButton_2.setEnabled(False)
        self.set_init_values()
        self.connect_slot()

    def get_current_info(self):
        host = self.lineEdit.text()
        port = self.lineEdit_2.text()

        username = self.lineEdit_3.text()
        password = self.lineEdit_4.text()

        return {'host': host, 'port': port, 'username': username, 'password': password}

    def check_connection(self):
        connection_info = self.get_current_info()
        if connection_info['username'] and connection_info['password']:
            proxies = {
                "http": f"http://{connection_info['username']}:{connection_info['password']}@{connection_info['host']}:{connection_info['port']}",
                "https": f"http://{connection_info['username']}:{connection_info['password']}@{connection_info['host']}:{connection_info['port']}",
            }
        else:
            proxies = {
                "http": f"http://{connection_info['host']}:{connection_info['port']}",
                "https": f"http://{connection_info['host']}:{connection_info['port']}",
            }
        print(proxies)
        # proxies = {
        #     "http": f"http://127.0.0.1:33210",
        #     "https": f"http://127.0.0.1:33210",
        # }
        url = self.lineEdit_5.text()
        try:
            response = requests.get(url, proxies=proxies, timeout=10)
            print(response.status_code)
        except Exception as e:
            logging.error(e, exc_info=True)
            QMessageBox.information(None, '连接测试', '连接错误，请重试！')
        else:
            if response.status_code == 200 or response.status_code == 201:
                QMessageBox.information(None, '连接测试', '连接成功')
                self.pushButton_2.setEnabled(True)
                return
            else:
                QMessageBox.information(None, '连接测试', '连接失败')
                return

    def save(self):
        connection_info = self.get_current_info()
        config = configparser.ConfigParser()
        try:
            config.read('config/config.ini')  # 读取 config.ini 文件
            if not config.has_section('Proxy'):
                config.add_section('Proxy')
        except Exception as e:
            print(str(e))
        finally:
            # 设置键值对
            config.set('Proxy', 'type', 'http')
            config.set('Proxy', 'host', connection_info['host'])
            config.set('Proxy', 'port', connection_info['port'])
            config.set('Proxy', 'username', connection_info['username'])
            config.set('Proxy', 'password', connection_info['password'])

        with open('config/config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)

        self.proxy_page.close()

    def set_init_values(self):
        config = configparser.ConfigParser()
        try:
            config.read('config/config.ini')  # 读取 config.ini 文件
            if config.has_section('Proxy') and config.get('Proxy', 'type') == 'http':
                self.lineEdit.setText(config.get('Proxy', 'host'))
                self.lineEdit_2.setText(config.get('Proxy', 'port'))
                self.lineEdit_3.setText(config.get('Proxy', 'username'))
                self.lineEdit_4.setText(config.get('Proxy', 'password'))
        except Exception as e:
            print(str(e))

    def info_changed(self):
        if self.pushButton_2.isEnabled():
            self.pushButton_2.setEnabled(False)

    def connect_slot(self):
        self.pushButton.clicked.connect(self.check_connection)
        self.pushButton_2.clicked.connect(self.save)

        self.lineEdit.textChanged.connect(self.info_changed)
        self.lineEdit_2.textChanged.connect(self.info_changed)
        self.lineEdit_3.textChanged.connect(self.info_changed)
        self.lineEdit_4.textChanged.connect(self.info_changed)

