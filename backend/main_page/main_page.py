

from PyQt5 import QtCore, QtGui, QtWidgets
from frontend.main_page.main_page import Ui_Form
from backend.baota_action.baota_action import BaotaAction
from backend.content_publish.content_publish import ContentPublish
from backend.AI_write.AI_write import AIWrite
from backend.word_management.word_management import WordManagement
from backend.SEO_setting.SEO_setting import SEOSetting
from backend.auto_publish.auto_publish import AutoPublish
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from api_requests.BtAPI import Bt
from backend.setting.proxy.proxy import Proxy
import datetime
import requests
from urllib3.exceptions import InsecureRequestWarning
import warnings
from backend.setting.redis_setting.redis_setting import RedisSetting
from backend.model_management.model_management import ModelManagement
import configparser
import logging
import time
import base64
from PyQt5.QtGui import *
import redis
import os
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
# QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

# QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)


class MainPage(QtWidgets.QWidget, Ui_Form):
    def __init__(self, username='123',
                 auth_l=["content", "admin", "ai", "keywords", "seoconfig", "bt", "automatic", "attachment"],
                 cookies={},
                 pc_hash='',
                 domain='',
                 scale_factor=1):
        super(MainPage, self).__init__()
        super().setupUi(self)
        # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        MAIN_SIZE_MAX = QSize(16777215, 16777215)
        self.setMaximumSize(MAIN_SIZE_MAX)
        # self.showMaximized()
        # self.page = page
        self.pc_hash = pc_hash
        self.domain = domain
        self.username = username
        icon = self.get_icon()
        self.setWindowIcon(icon)
        print(auth_l)
        if auth_l == ['all']:
            self.auth_l = ["content", "admin", "ai", "keywords", "seoconfig", "bt", "automatic", "attachment", "templates"]         # 全部权限
        else:
            self.auth_l = auth_l
        self.scale_factor = scale_factor
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, False)
        panel, key = '', ''
        self.bt_sign = False
        self.bt_patch = 0     # 默认0为国内宝塔，1为英文宝塔v2
        self.bt = Bt(panel, key)
        self.cookies = cookies
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                        }
        self.create_loading_label()
        self.need_init_page = True
        # public_config = self.bt.get_public_config()

        self.init_baota_page = True
        self.init_content_publish = False
        self.init_ai_write = False
        self.init_word_management = False
        self.init_seo_setting = False
        self.init_auto_publish = False
        self.init_model_management = False

        self.bt_login = False
        # self.get_screen_scale_factor()
        self.auth_refer()               # 比较权限
        self.set_dropdown_menu()
        self.init_check_redis_setting()
        self.connect_slot()

    def initializeTabContent(self, tab_index):
        if tab_index == 0:
            if not self.init_baota_page:
                self.baota_page = BaotaAction(self.tab, self)
                self.init_baota_page = True
        elif tab_index == 1:
            if not self.init_content_publish:
                self.content_publish = ContentPublish(self.tab_2, self)
                self.init_content_publish = True
        elif tab_index == 2:
            if not self.init_ai_write:
                self.ai_write = AIWrite(self.tab_3, self)
                self.init_ai_write = True
        elif tab_index == 3:
            if not self.init_word_management:
                self.word_management = WordManagement(self.tab_4, self)
                self.init_word_management = True
        elif tab_index == 4:
            if not self.init_seo_setting:
                self.seo_setting = SEOSetting(self.tab_5, self)
                self.init_seo_setting = True
        elif tab_index == 5:
            if not self.init_auto_publish:
                self.auto_publish = AutoPublish(self.tab_6, self)
                self.init_auto_publish = True
        elif tab_index == 6:
            if not self.init_model_management:
                self.model_management = ModelManagement(self.tab_7, self)
                self.init_model_management = True

    def auth_refer(self):
        if 'bt' not in self.auth_l:
            self.tabWidget.setTabEnabled(0, False)
            self.tabWidget.tabBar().setTabVisible(0, False)
        elif self.need_init_page:         # 判断是否需要一个初始化页面
            self.baota_page = BaotaAction(self.tab, self)           # 在有权限情况下的首页
            self.need_init_page = False

        if 'content' not in self.auth_l:
            self.tabWidget.setTabEnabled(1, False)
            self.tabWidget.tabBar().setTabVisible(1, False)
        elif self.need_init_page:
            self.content_publish = ContentPublish(self.tab_2, self)
            self.need_init_page = False
            self.init_content_publish = True

        if 'ai' not in self.auth_l:
            self.tabWidget.tabBar().setTabVisible(2, False)
            self.tabWidget.setTabEnabled(2, False)
        elif self.need_init_page:
            self.ai_write = AIWrite(self.tab_3, self)
            self.init_ai_write = True
            self.need_init_page = False

        if 'keywords' not in self.auth_l:
            self.tabWidget.tabBar().setTabVisible(3, False)
            self.tabWidget.setTabEnabled(3, False)
        elif self.need_init_page:
            self.word_management = WordManagement(self.tab_4, self)
            self.init_word_management = True
            self.need_init_page = False

        if 'seoconfig' not in self.auth_l:
            self.tabWidget.tabBar().setTabVisible(4, False)
            self.tabWidget.setTabEnabled(4, False)
        elif self.need_init_page:
            self.seo_setting = SEOSetting(self.tab_5, self)
            self.init_seo_setting = True
            self.need_init_page = False

        if 'automatic' not in self.auth_l:
            self.tabWidget.tabBar().setTabVisible(5, False)
            self.tabWidget.setTabEnabled(5, False)
        elif self.need_init_page:
            self.auto_publish = AutoPublish(self.tab_6, self)         # 在有权限时, 自动开启
            self.init_auto_publish = True
            self.need_init_page = False
        # else:            #  test
        #     self.auto_publish = AutoPublish(self.tab_6, self)         # 在有权限时, 自动开启, 但不作为初始页面

        if 'templates' not in self.auth_l:
            self.tabWidget.tabBar().setTabVisible(6, False)
            self.tabWidget.setTabEnabled(6, False)
        elif self.need_init_page:
            self.model_management = ModelManagement(self.tab_7, self)
            self.init_model_management = True
            self.need_init_page = False

    def get_icon(self):
        # img_data = base64.b64decode(self.icon_image_base64)

        # self.setWindowIcon
        # 将字节流转换为QPixmap
        pixmap = QPixmap("images/icon.jpg")
        # pixmap.loadFromData(img_data)

        # 将QPixmap转换为QIcon
        icon = QIcon(pixmap)
        return icon

    def connect_slot(self):
        self.tabWidget.currentChanged.connect(self.initializeTabContent)

    def set_dropdown_menu(self):
        menu_items = [
            '代理设置',
            '缓存设置',
        ]
        menu = QMenu(self.tab)
        action = QtWidgets.QAction("代理设置", self)
        action.setIconVisibleInMenu(False)
        action.triggered.connect(self.open_proxy)
        menu.addAction(action)

        action_2 = QtWidgets.QAction("缓存设置", self)
        action_2.setIconVisibleInMenu(False)
        action_2.triggered.connect(self.open_redis_setting)
        menu.addAction(action_2)
        self.toolButton.setMenu(menu)

    def closeEvent(self, event):
        # self.auto_publish.auto_publishment_page.ui_auto_publish_window
        event.accept()
        os.system('taskkill /im chromedriver.exe /F')               # 有用！可以清除chrome driver内存！
        # self.hide()

    def open_proxy(self):
        self.proxy_window = Proxy()
        self.proxy_window.show()

    def open_redis_setting(self):
        self.redis_setting_ui = RedisSetting()
        self.redis_setting_ui.show()

    def init_check_redis_setting(self):
        self.t_check_redis = InitCheckRedis()
        self.t_check_redis.start()
        self.t_check_redis.finish_trigger.connect(self.return_check_redis_setting)

    def return_check_redis_setting(self, status):
        if status:
            reply = QMessageBox.warning(self, "提示", "检测到未添加Redis设置，请前往设置中添加Redis！", QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                self.open_redis_setting()

    def get_current_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def return_msg_update(self, msg):
        self.textEdit.append(self.get_current_datetime() + ": " + str(msg))
        # self.textEdit.textChanged.connect(self.textEdit.moveCursor().End)
        self.textEdit.textChanged.connect(self.scrollToBottom)

    def scrollToBottom(self):
        cursor = self.textEdit.textCursor()
        self.textEdit.moveCursor(cursor.End)
        # self.textEdit.setTextCursor(cursor)
        # self.textEdit.ensureCursorVisible()

    def create_loading_label(self):
        self.loading_label = QtWidgets.QLabel(self)
        self.loading_label.showMaximized()
        width = self.size().width()
        height = self.size().height()
        # self.loading_label.setGeometry(QtCore.QRect(0, 0, width//2, height//2))
        self.loading_label.setStyleSheet("background-color: rgba(255, 255, 255, 180)")
        self.loading_label.setMinimumSize(QtCore.QSize(width, height))
        self.loading_label.setMaximumSize(QtCore.QSize(width, height))
        self.loading_label.setAlignment(QtCore.Qt.AlignCenter| QtCore.Qt.AlignVCenter)
        self.loading_label.setObjectName("label")

        # self.movie = QMovie("./docs/image/loading.gif")
        # self.movie = QMovie("")
        # self.movie.setCacheMode(QMovie.CacheAll)
        # self.loading_label.setMovie(self.movie)
        # self.movie.start()
        self.loading_label.hide()

    def hide_loading_label(self):
        if self.loading_label.isHidden() is False:
            self.loading_label.hide()

    def show_loading_label(self):
        if self.loading_label.isVisible() is False:
            width = self.size().width()
            height = self.size().height()
            self.loading_label.setMinimumSize(QtCore.QSize(width, height))
            self.loading_label.setMaximumSize(QtCore.QSize(width, height))
            self.loading_label.show()


class InitCheckRedis(QThread):
    finish_trigger = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    def run(self):
        config = configparser.ConfigParser()
        try:
            config.read('config/config.ini')  # 读取 config.ini 文件
            if not config.has_section('RedisSetting'):
                print(3333)
                self.finish_trigger.emit(True)          # True为需要设置redis
            else:
                host = config.get('RedisSetting', 'Host')
                port = config.get('RedisSetting', 'port')
                password = config.get('RedisSetting', 'password')
                redis_client = redis.StrictRedis(host=host, port=port,
                                                 password=password, socket_timeout=2,
                                                 decode_responses=True)
                try:
                    if redis_client.ping():
                        self.finish_trigger.emit(False)
                        print("成功连接到Redis服务器")
                    else:
                        self.finish_trigger.emit(True)
                        print("无法连接到Redis服务器")
                except Exception as e:
                    logging.error(e, exc_info=True)
                    self.finish_trigger.emit(True)

        except Exception as e:
            logging.error(e, exc_info=True)
            self.finish_trigger.emit(True)