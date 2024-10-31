

from frontend.setting.redis.redis import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
import configparser
import redis
from PyQt5.QtWidgets import QMessageBox


class RedisSetting(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.setEnabled(False)
        self.set_init_values()
        self.connect_slot()

    def get_current_info(self):
        host = self.lineEdit.text()
        port = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        return {'host': host, 'port': port, 'password': password}

    def check_connection(self):
        connection_info = self.get_current_info()

        redis_client = redis.StrictRedis(host=connection_info['host'], port=connection_info['port'], password=connection_info['password'], socket_timeout=2, decode_responses=True)
        try:
            if redis_client.ping():
                self.pushButton.setEnabled(True)
                print("成功连接到Redis服务器")
            else:
                print("无法连接到Redis服务器")
        except Exception as e:
            QMessageBox.information(None, '连接测试', '连接失败，请检查！')
        else:
            QMessageBox.information(None, '连接测试', '连接成功！')


    def save(self):
        connection_info = self.get_current_info()
        config = configparser.ConfigParser()
        try:
            config.read('config/config.ini')  # 读取 config.ini 文件
            if not config.has_section('RedisSetting'):
                config.add_section('RedisSetting')
        except Exception as e:
            print(str(e))
        finally:
            # 设置键值对
            config.set('RedisSetting', 'host', connection_info['host'])
            config.set('RedisSetting', 'port', connection_info['port'])
            config.set('RedisSetting', 'password', connection_info['password'])

        with open('config/config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)

        self.close()

    def set_init_values(self):
        config = configparser.ConfigParser()
        try:
            config.read('config/config.ini')  # 读取 config.ini 文件
            if config.has_section('RedisSetting'):
                self.lineEdit.setText(config.get('RedisSetting', 'host'))
                self.lineEdit_2.setText(config.get('RedisSetting', 'port'))
                self.lineEdit_3.setText(config.get('RedisSetting', 'password'))
        except Exception as e:
            print(str(e))

    def info_changed(self):
        if self.pushButton.isEnabled():
            self.pushButton.setEnabled(False)

    def connect_slot(self):
        self.pushButton.clicked.connect(self.save)
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.check_connection)

        self.lineEdit.textChanged.connect(self.info_changed)
        self.lineEdit_2.textChanged.connect(self.info_changed)
        self.lineEdit_3.textChanged.connect(self.info_changed)


