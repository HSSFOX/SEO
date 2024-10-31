from SEO_update_program_ui import Ui_Form
from PyQt5.QtWidgets import *
import os
import sys
import requests
import win32api
import ctypes
from PyQt5.QtCore import *
import logging
import configparser
from PyQt5.QtGui import *
import base64
import subprocess
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap, QImage, QMovie
from PyQt5.QtCore import QByteArray
from base64 import b64decode
import datetime
import html
import hashlib


class SEOUpdateProgram(QWidget, Ui_Form):
    def __init__(self, program_path='', old_program_basename='SEO.exe', new_program_basename='.SEO.exe', source='0'):
        super().__init__()
        self.setupUi(self)
        self.session = requests.session()
        # # 创建一个QMovie对象
        movie = QMovie('images/loading.gif')
        # # 将QLabel与QMovie关联
        movie.setCacheMode(QMovie.CacheAll)
        self.label.setMovie(movie)
        # # 播放动图
        movie.start()
        print(11111, program_path, old_program_basename, new_program_basename, source)
        self.program_path = program_path
        self.old_program_basename = old_program_basename
        self.new_program_basename = new_program_basename
        self.source = source
        # self.reinstall_program()
        self.main()
        self.connect_slot()

    def main(self):
        if self.source == '1':             # 直接重命名！
            self.frame_2.hide()
            self.progressBar.setValue(100)
            self.t = InstallProgress(self)
            self.t.start()
            self.t.finished.connect(self.return_program)
        else:
            self.frame.hide()

    def download_from_sha256(self, choice=0):
        if choice == 1:
            self.old_program_basename = 'AutoPublishTool.exe'
        self.frame.show()
        self.frame_2.hide()
        self.t_download = DownloadFromSHA256(self, choice)
        self.t_download.start()
        self.t_download.progress_bar_trigger.connect(self.update_progress_bar)
        self.t_download.finished.connect(self.finish_download)

    def update_progress_bar(self, progress_percent):
        self.progressBar.setValue(progress_percent)

    def finish_download(self):
        print("下载结束！")
        self.progressBar.setValue(100)
        self.update_version_patch()             # 更新版本号
        self.close()

    def reinstall_program(self):
        print("下载结束！")

        os.remove(os.path.join(self.program_path, self.old_program_basename))
        os.rename(os.path.join(self.program_path, self.new_program_basename), os.path.join(self.program_path, self.old_program_basename))          # 将旧程序删除 安装重命名新程序
        # os.remove(os.path.join(self.program_path, self.new_program_basename))         # 重命名不需要删除
        self.update_version_patch()             # 更新版本号
        self.update_config('SHA256_CHECK_DATE', 'sha256_update_date', str(datetime.datetime.now().date()))

    def return_program(self):
        self.close()
        subprocess.Popen(os.path.join(self.program_path, self.old_program_basename))

    def update_version_patch(self):
        status, version = self.get_version_patch()
        print("保存！", status, version)
        if status:
            config = configparser.ConfigParser()
            try:
                config.read('config/login_config.ini')                # 读取 config.ini 文件
                if not config.has_section('Version'):
                    config.add_section('Version')
            except Exception as e:
                print(str(e))
            finally:
                # 设置键值对
                config.set('Version', 'version', version)
                with open('config/login_config.ini', 'w', encoding='utf-8') as configfile:
                    config.write(configfile)

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
            logging.error(e, exc_info=True)

    def get_version_patch(self):
        url = self.get_login_config('Domain', 'host_port')
        try:
            res = requests.get(url, timeout=1).json()
        except Exception as e:
            logging.error(e)
            return False, ''
        else:
            if res.get('status'):
                return True, res['version']
            else:
                return False, ''

    def get_login_config(self, section, name, path='config/login_config.ini'):
        try:
            config = configparser.ConfigParser()
            config.read(path)
            name = config[section][name]
            return name
        except Exception as e:
            logging.error(e)
            return ''

    def closeEvent(self, event):
        # 退出表示弹出框标题，"你确定退出吗？"表示弹出框的内容
        reply = QMessageBox.question(None, '下载完毕确认', '更新完毕，点击确认退出',
                                     QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()  # 接受关闭事件

    def return_msg(self, msg):
        QMessageBox.warning(None, '错误', f'在程序下载过程中发生了错误, 错误信息: {str(msg)}')

    def connect_slot(self):
        self.pushButton.clicked.connect(lambda: self.download_from_sha256())
        self.pushButton_2.clicked.connect(lambda: self.download_from_sha256(1))

    def get_host_port(self):
        url = self.get_login_config('Domain', 'host_port')
        return url

    def get_login_config(self, section, name, path='config/login_config.ini'):
        try:
            config = configparser.ConfigParser()
            config.read(path)
            name = config[section][name]
            return name
        except Exception as e:
            logging.error(e)
            return 'http://192.168.110.110:501'


class InstallProgress(QThread):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        self.ui.reinstall_program()


class DownloadFromSHA256(QThread):
    progress_bar_trigger = pyqtSignal(int)
    finish_trigger = pyqtSignal(bool, dict, str)

    def __init__(self, ui, choice):
        super().__init__()
        self.ui = ui
        self.choice = choice

    def run(self):
        # url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=5396493280'
        # try:
        #     sha256_info = self.ui.session.get(url).json()
        #     redirect_url = html.unescape(sha256_info['data']['userInfo']['description'])
        #     r = self.ui.session.get(redirect_url).json()
        #     print(44444444, r)
        # except Exception as e:
        #     logging.error(e, exc_info=True)
        # else:
        #     if self.choice:
        #         url = r['MAIN_URL']  # 对比sha256值 正确则不进行更新
        #     else:
        #         url = r['UPDOUN_URL']
        host_port = self.ui.get_host_port()
        if self.choice:
            url = f'{host_port}/version/SEO.exe'
        else:
            url = f'{host_port}/version/SEO_auto_publish_tool.exe'
        self.downfile(url)

    def downfile(self, url):
        try:
            response = requests.get(url, stream=True, verify=False)
            print(url)
            total_size = int(response.headers['Content-Length'])  # 获取总长
            print("total_size", total_size)
            progress = 0
            with open(self.ui.old_program_basename, 'wb') as f:
                iterator = response.iter_content(chunk_size=1024)  # you can adjust the chunk size as needed
                # total_chunks = (total_size + 1023) // 1024  # calculate the number of chunks based on the chunk size
                for chunk in iterator:
                    if chunk:
                        f.write(chunk)
                        # f.flush()           # 直接写入磁盘
                        progress_percent = int(100 * progress / total_size)
                        progress += len(chunk)
                        sys.stdout.flush()
                        self.progress_bar_trigger.emit(progress_percent)
        except Exception as e:
            logging.error(e, exc_info=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    # seo_update_p = SEOUpdateProgram('SEO.exe')
    print(1111111111111111111111)
    print(sys.argv)
    execute_script = sys.argv
    # print(execute_script)
    arguments = sys.argv[1:]
    print("arguments: ", arguments)
    if arguments:
        seo_update_p = SEOUpdateProgram(arguments[0], arguments[1], arguments[2], arguments[3])
    else:
        seo_update_p = SEOUpdateProgram()
    # seo_update_p = SEOUpdateProgram()

    seo_update_p.show()
    sys.exit(app.exec_())

