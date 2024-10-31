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

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap, QImage, QMovie
from PyQt5.QtCore import QByteArray
from base64 import b64decode


class SEOUpdateProgram(QWidget, Ui_Form):
    def __init__(self, program_path, new_program_path):
        super().__init__()
        self.setupUi(self)
        self.base64_gif = 'data:image/png;base64,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'
        self.old_program_path = program_path
        self.new_program_path = new_program_path
        # img_data = base64.b64decode(self.base64_gif)
        # # 将图片数据转换为QImage对象
        # image = QPixmap()
        # image.loadFromData(img_data)
        # # # 创建一个QMovie对象
        # movie = QMovie(image)
        # #
        # # # 将QLabel与QMovie关联
        # self.label.setMovie(movie)
        # # # 播放动图
        # movie.start()

        # img = QPixmap()
        # img.loadFromData(img_data)
        # self.label.setPixmap(img)

        self.download()

    def download(self):
        # path = f"{os.getcwd()}//SEO.exe"                # 当前exe的path
        # link = f'http://192.168.110.12:5001/uploadfile'
        host_url = self.get_host_port()
        link = f'{host_url}/version'
        UUID = r'SEO.exe'
        url = os.path.join(link, UUID)
        print("原神！启动！", url)
        self.write_download(url, self.old_program_path)

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

    # 结束进程的函数
    def terminate_process(self, process_id):
        handle = ctypes.windll.kernel32.OpenProcess(1, False, process_id)
        if handle:
            ctypes.windll.kernel32.TerminateProcess(handle, 1)
            ctypes.windll.kernel32.CloseHandle(handle)

    # 替换.exe文件的函数
    def replace_exe(self, old_exe_path, new_exe_path):
        # 获取进程ID
        process_id = ctypes.windll.kernel32.GetCurrentProcessId()

        # 结束当前进程
        self.terminate_process(process_id)

        # 删除旧的.exe文件，并复制新的.exe文件
        os.remove(old_exe_path)
        os.startfile(new_exe_path)

    def write_download(self, url, path):
        self.t_donload_write = DownloadWriteInThread(url, os.path.join(os.getcwd(), path))
        self.t_donload_write.start()
        self.t_donload_write.progress_bar_trigger.connect(self.update_progress_bar)
        self.t_donload_write.finish_trigger.connect(self.finish_download)

    def update_progress_bar(self, progress_percent):
        self.progressBar.setValue(progress_percent)

    def finish_download(self):
        print("下载结束！")
        self.progressBar.setValue(100)
        self.update_version_patch()             # 更新版本号
        self.close()

    def closeEvent(self, event):
        # 退出表示弹出框标题，"你确定退出吗？"表示弹出框的内容
        reply = QMessageBox.question(self, '下载完毕确认', '更新完毕，点击确认退出',
                                     QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()  # 接受关闭事件

    def return_msg(self, msg):
        QMessageBox.warning(None, '错误', f'在程序下载过程中发生了错误, 错误信息: {str(msg)}')


class DownloadWriteInThread(QThread):
    progress_bar_trigger = pyqtSignal(int)
    finish_trigger = pyqtSignal()
    msg_trigger = pyqtSignal(str)

    def __init__(self, url, path):
        super().__init__()
        self.url = url
        self.path = path
        print("path: ", self.path)

    def run(self):
        self.downfile(self.url)
        self.finish_trigger.emit()

    def downfile(self, url):
        try:
            response = requests.get(url, stream=True, verify=False)
            print(url)
            total_size = int(response.headers['Content-Length'])  # 获取总长
            print("total_size", total_size)
            progress = 0
            with open(self.path, 'wb') as f:
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
            self.msg_trigger.emit(str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    seo_update_p = SEOUpdateProgram('SEO.exe')
    # execute_script = sys.argv[0]
    # print(execute_script)
    # arguments = sys.argv[1:]
    # seo_update_p = SEOUpdateProgram(arguments[0], arguments[1])
    SEOUpdateProgram(seo_update_p)
    seo_update_p.show()
    sys.exit(app.exec_())

