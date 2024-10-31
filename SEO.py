
from frontend.login.login import Ui_Form
import time
import random
import string
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QWidget,QMainWindow
from backend.main_page.main_page import MainPage
from PyQt5.QtWidgets import QApplication
from model.utils import my_logger
import sys
import requests
import configparser
import os
import subprocess
from backend.setting.host_port.host_port import HostPort
from PyQt5.QtCore import QSystemSemaphore, QSharedMemory
import logging
import gc
import hashlib
import html
from PyQt5.QtCore import *
import datetime

# from PyQt5.QtGui import QOpenGLContext, QOpenGLFunctions
# 设置环境变量以禁用沙箱模式
os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'


class Login(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.session = requests.session()
        patch = self.get_version_patch()
        self.program_name = os.path.basename(sys.argv[0])
        self.current_patch = patch
        self.domain = self.get_login_config('Domain', 'host_port')
        self.pushButton.clicked.connect(self.login)
        self.msg = {'msg': '登陆失败'}
        self.if_save_name()
        self.init_detect_connection()
        gc.collect()

    def get_version_patch(self):
        url = self.get_login_config('Domain', 'host_port')
        try:
            res = self.session.get(url, timeout=1).json()
        except Exception as e:
            logging.error(e)
            return '1.1.4'
        else:
            if res.get('status'):
                return res['version']
            else:
                return '1.1.4'

    def get_login_config(self, section, name, path='config/login_config.ini'):
        try:
            config = configparser.ConfigParser()
            config.read(path)
            name = config[section][name]
            return name
        except Exception as e:
            logging.error(e)
            return ''

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:  # Qt.Key_Return 对应 Enter 键
            self.login()

    def login(self):                # 登录触发的方法
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if password == '' or username == '':
            QMessageBox.warning(self, '警告', '用户名或密码不能为空！', QMessageBox.Ok)
        else:                   # 进入登录
            dict_dict = {"username": username, "password": password}

            try:
                url = f'{self.domain}/?m=admin&c=index&a=jong&json=1&dosubmit=1'
                response = self.session.post(url, data=dict_dict, timeout=5)
                cookies = response.cookies.get_dict()
                print(cookies)
                print(response.json())

                pc_hash = response.json().get('pc_hash')
                self.msg = response.json()
            except Exception as e:
                my_logger.error(e)
                print(str(e))
                QMessageBox.warning(self, '警告', "无法连接至服务器", QMessageBox.Ok)
            else:
                if self.msg['msg'] == '登录成功！':
                    if self.checkBox.isChecked():
                        try:
                            self.update_config('UserInfo', 'user_name', username)
                        except Exception as e:
                            print(e)
                            my_logger.error(e)
                    if self.checkBox_2.isChecked():
                        try:
                            self.update_config('UserInfo', 'password', password)
                        except Exception as e:
                            print(e)
                            my_logger.error(e)
                    self.open_main_window(response.json()['usrname'], response.json()['role'], cookies, pc_hash, self.domain)
                else:
                    my_logger.error(self.msg)
                    QMessageBox.warning(self, '警告', self.msg['msg'], QMessageBox.Ok)

    # 调用主页面的函数
    def open_main_window(self, usrname, auth_l, cookies, pc_hash, domain):
        my_logger.info(self.msg)
        self.close()  # 关闭主窗口
        if auth_l == 'all':
            auth_l = ["content", "admin", "ai", "keywords", "seoconfig", "bt", "automatic", "attachment", "templates"]
        self.page = MainPage(usrname, auth_l, cookies, pc_hash, domain, scale_factor=1.5)
        self.page.show()

    # 判断是否记住账号名字
    def if_save_name(self):
        name = self.get_login_config('UserInfo', 'user_name')
        pwd = self.get_login_config('UserInfo', 'password')
        if name:
            self.lineEdit.setText(name)
            self.lineEdit_2.setText(pwd)

    def init_detect_connection(self):
        self.t_login = DetectThread()
        self.t_login.start()
        self.t_login.finish_trigger.connect(self.connect_box)

    def connect_box(self, status, client_patch):
        if not status:
            reply = QMessageBox.question(self, '无法连接至服务器', '无法连接至服务器！确认打开域名配置界面',
                                         QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.host_port_ui = HostPort(self)
                self.host_port_ui.show()
        # else:
        #     if self.check_sha256_datetime():                # 检查是否时周五/ 以及是否已更新过
        #         self.check_sha256(client_patch)

    def check_sha256(self, client_path):
        self.t_check_sha256_update = CheckSHA256(self, client_path)
        self.t_check_sha256_update.start()
        self.t_check_sha256_update.finish_trigger.connect(self.return_check_sha256_update)

    def return_check_sha256_update(self, status, r, client_patch):
        if status:
            if not client_patch or (client_patch and client_patch != self.current_patch):
                print("需要更新")
                # update 启动更新程序

                reply = QMessageBox.question(self, '发现新的版本', '请确认更新',
                                             QMessageBox.Yes| QMessageBox.No)
                if reply == QMessageBox.Yes:
                    path = os.path.abspath('')  # 当前路径
                    new_program_name = "." + self.program_name  # 新程序名称
                    # 启动更新程序，安装
                    params = [path, self.program_name, new_program_name, '1']  # source: 0-自启动 1-主程序启动 2-自动发布启动

                    exe_path = "SEO_SSH_update_program.exe"
                    if os.path.exists(exe_path):  # 检查是否有更新程序 有则直接启动, 无则安装
                        # 使用subprocess.Popen启动程序
                        try:
                            subprocess.Popen([exe_path] + params)  # 启动的时候添加参数
                        except Exception as e:
                            my_logger.error(e, exc_info=True)
                        else:
                            self.close()
                    else:
                        url = f"{self.domain}/version/SEO_SSH_update_program.exe"
                        self.t_force_update = DownloadWriteInThread(url, 'SEO_SSH_update_program.exe',
                                                                    1)  # mode = 0 - SHA更新   1 - 下载更新程序
                        self.t_force_update.start()
                        self.t_force_update.finish_trigger.connect(self.finish_download)

                #     exe_path = "SEO_update_program.exe"
                #     # current_folder_path = "SEO.exe"
                #     # params = [current_folder_path]
                #     # 使用subprocess.Popen启动程序
                #     try:
                #         subprocess.Popen(exe_path)           # 启动的时候添加参数
                #     except Exception as e:
                #         my_logger(e)
                #     else:
                #         self.close()
                # else:
                #     self.close()
        else:
            update_url = self.check_url(r)          # 获取更新url
            if update_url:
                # 进行更新 -> 传入软件更新url、当前.exe文件路径
                self.t_force_update = DownloadWriteInThread(update_url, os.path.abspath(self.program_name), 0)          # mode = 0 - SHA更新   1 - 下载更新程序
                self.t_force_update.start()
                self.t_force_update.finish_trigger.connect(self.finish_download)

    def finish_download(self):
        print("下载结束！")
        # self.update_version_patch()             # 更新版本号
        path = os.path.abspath('')      # 当前路径
        new_program_name = "." + self.program_name      # 新程序名称
        # 启动更新程序，安装
        params = [path, self.program_name, new_program_name, '1']         # source: 0-自启动 1-主程序启动 2-自动发布启动(似乎不需要)
        exe_path = "SEO_SSH_update_program.exe"

        if os.path.exists(exe_path):                    # 检查是否有更新程序 有则直接启动, 无则安装
            print("打开！！！", params)
            # 使用subprocess.Popen启动程序
            try:
                subprocess.Popen([exe_path] + params)  # 启动的时候添加参数
            except Exception as e:
                my_logger.error(e, exc_info=True)
            else:
                self.close()
        else:
            url = f"{self.domain}/version/SEO_SSH_update_program.exe"
            self.t_force_update = DownloadWriteInThread(url, 'SEO_SSH_update_program.exe',1)  # mode = 0 - SHA更新   1 - 下载更新程序
            self.t_force_update.start()
            self.t_force_update.finish_trigger.connect(self.finish_download)
        # self.close()

    def update_config(self, section, key, value, path='config/login_config.ini'):
        try:
            config = configparser.ConfigParser()
            if os.path.exists(path):
                config.read(path)
            if not config.has_section(section):
                config.add_section(section)
            config.set(section, key, value)
            with open(path, 'w') as configfile:
                config.write(configfile)
        except Exception as e:
            my_logger.error(e, exc_info=True)

    # 获取节点值
    def get_login_config(self, section, name, path='config/login_config.ini'):
        try:
            config = configparser.ConfigParser()
            config.read(path)
            name = config[section][name]
            return name
        except Exception as e:
            my_logger.error(e)
            return ''

    def check_url(self, response):
        # response['U1'] = 'http://192.168.110.110:501/version/SEO.exe'
        if response.get('MAIN_URL'):                # 主程序就只看MAIN PROGRAM的
            r = self.session.get(response['MAIN_URL'])
            if r.status_code == 200:
                return response['MAIN_URL']
        return None

    def check_sha256_datetime(self):
        today = datetime.datetime.now().date()
        if today.isoweekday() == 4:         # 4=周五
            # 确认今天是否已更新
            config_date = self.get_login_config('SHA256_CHECK_DATE', 'sha256_update_date')
            if config_date == str(today):
                return False
            else:
                return True
        else:
            return False


class DetectThread(QtCore.QThread):
    finish_trigger = QtCore.pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()

    def run(self):
        url = self.get_login_config('Domain', 'host_port')
        try:
            res = requests.get(url, timeout=1).json()
        except Exception as e:
            my_logger.error(e)
            self.finish_trigger.emit(False, '')
        else:
            if res.get('status'):
                self.finish_trigger.emit(True, res['version'])
            else:
                self.finish_trigger.emit(False, '')

    def get_login_config(self, section, name, path='config/login_config.ini'):
        try:
            config = configparser.ConfigParser()
            config.read(path)
            name = config[section][name]
            return name
        except Exception as e:
            my_logger.error(e)
            return ''


class DownloadWriteInThread(QThread):
    progress_bar_trigger = pyqtSignal(int)
    finish_trigger = pyqtSignal()
    msg_trigger = pyqtSignal(str)

    def __init__(self, url, path, mode):
        super().__init__()
        self.url = url
        self.path = path
        self.mode = mode
        print("path: ", self.path)

    def run(self):
        self.downfile(self.url)
        self.finish_trigger.emit()

    def downfile(self, url):
        if self.mode == 0:
            base_name = os.path.basename(self.path)
            new_base_name = "." + base_name                 # 下载的.EXE文件
            path = self.path.replace(base_name, new_base_name)
        else:
            path = self.path
        # print(base_name, new_base_name)
        try:
            response = requests.get(url, stream=True, verify=False)
            # print(url)
            # total_size = int(response.headers['Content-Length'])  # 获取总长
            with open(path, 'wb') as f:           # 下载url，写入本地并以 .basename.exe命名
                iterator = response.iter_content(chunk_size=1024)  # you can adjust the chunk size as needed
                # total_chunks = (total_size + 1023) // 1024  # calculate the number of chunks based on the chunk size
                for chunk in iterator:
                    if chunk:
                        f.write(chunk)
                        # f.flush()           # 直接写入磁盘
                        sys.stdout.flush()
        except Exception as e:
            self.msg_trigger.emit(str(e))


class CheckSHA256(QThread):
    finish_trigger = pyqtSignal(bool, dict, str)

    def __init__(self, ui, client_patch):
        super().__init__()
        self.ui = ui
        self.client_patch = client_patch

    def run(self):
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=5396493280'
        try:
            sha256_info = self.ui.session.get(url).json()
            redirect_url = html.unescape(sha256_info['data']['userInfo']['description'])
            r = self.ui.session.get(redirect_url).json()
            print(44444444, r)
        except Exception as e:
            logging.error(e, exc_info=True)
        # 打开自身的程序文件
        with open(sys.argv[0], "rb") as f:
            # 读取文件内容并计算SHA256哈希值
            current_sha256 = hashlib.sha256(f.read()).hexdigest()
            print(3333333333, current_sha256)
        if current_sha256 == r['MAIN_SHA256']:  # 对比sha256值 正确则不进行更新
            self.finish_trigger.emit(True, r, self.client_patch)          # 正确
        else:
            self.finish_trigger.emit(False, r, self.client_patch)         # 错误


def launch():
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseSoftwareOpenGL)
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_DisableSessionManager)
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_DisableShaderDiskCache)

    app = QtWidgets.QApplication(sys.argv+["--no-sandbox"])  # create app instance at top, to able to show QMessageBox is required
    def get_screen_scale_factor(app):
        desktop = QtWidgets.QDesktopWidget()
        screen = desktop.screen()
        widget = QtWidgets.QWidget()
        # 获取当前窗口关联的屏幕
        screen = widget.window().screen()
        # 获取DPI
        dpi = screen.logicalDotsPerInch()
        scale_factor = dpi / 96.0

        # scale_factor = screen.logicalDotsPerInch() / 96.0
        print(f"Screen scale factor: {scale_factor}")
        font = QtGui.QFont()
        if scale_factor == 1:       # 比例100%
            font.setPointSize(13)  # 设置默认字体大小为10号字体
        else:
            font.setPointSize(9)  # 设置默认字体大小为10号字体

        app.setFont(font)
    get_screen_scale_factor(app)
    app.setStyle('Fusion')
    window_id = 'SEOid'
    shared_mem_id = 'SEOmem'
    semaphore = QSystemSemaphore(window_id, 1)
    semaphore.acquire()  # Raise the semaphore, barring other instances to work with shared memory

    if sys.platform != 'win32':
        # in linux / unix shared memory is not freed when the application terminates abnormally,
        # so you need to get rid of the garbage
        nix_fix_shared_mem = QSharedMemory(shared_mem_id)
        if nix_fix_shared_mem.attach():
            nix_fix_shared_mem.detach()

    shared_memory = QSharedMemory(shared_mem_id)

    if shared_memory.attach():  # attach a copy of the shared memory, if successful, the application is already running
        is_running = True
    else:
        shared_memory.create(1)  # allocate a shared memory block of 1 byte
        is_running = False

    semaphore.release()

    if is_running:  # if the application is already running, show the warning message
        QtWidgets.QMessageBox.warning(None, 'Application already running',
                                      '程序已打开！')
        return

    # # 创建一个新的OpenGL上下文
    # context = QOpenGLContext()
    # context.setFormat(QOpenGLContext.openGLSurfaceFormat())
    # if not context.create():
    #     print("无法创建OpenGL上下文")
    #     exit(-1)
    #
    # if not context.makeCurrent():
    #     print("无法使上下文当前")
    #     exit(-2)
    #
    # # 清理当前上下文的缓存
    # functions = QOpenGLFunctions(context)
    # functions.glClearColor(0.0, 0.0, 0.0, 1.0)  # 设置清除颜色为黑色
    # functions.glClear(functions.GL_COLOR_BUFFER_BIT)  # 清除颜色缓存
    #
    # # 交换前后缓冲区以显示结果
    # context.swapBuffers()
    #
    # # 清理资源
    # context.doneCurrent()
    # del context




    # normal process of creating & launching MainWindow
    login = Login()
    login.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    launch()

