from frontend.words_management.batch_add.batch_add import Ui_Form
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from model.utils import word_management_logger as my_logger
from collections import OrderedDict
import datetime
from PyQt5.QtWidgets import *


class BatchAdd(Ui_Form):
    def __init__(self, page, parent_ui):
        super().setupUi(page)
        self.page = page
        self.parent_ui = parent_ui
        self.cookies = parent_ui.cookies
        self.headers = parent_ui.headers
        self.job_l = []
        self.word_type_l = []
        self.session = requests.session()
        self.main()
        self.connect_slot()

    def main(self):
        self.t_job_thread = JobThread(self)
        self.t_job_thread.start()
        self.t_job_thread.msg_trigger.connect(self.return_msg_trigger)
        self.t_job_thread.finish_trigger.connect(self.finish_trigger)

    def return_msg_trigger(self, msg):
        self.parent_ui.main_page.return_msg_update(str(msg))

    def get_current_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def finish_trigger(self, job_l, word_type_l):
        self.job_l = job_l
        self.word_type_l = word_type_l
        self.comboBox.addItems([ele['name'] for ele in self.job_l])
        self.comboBox_2.addItems([ele['name'] for ele in self.word_type_l])

    def save(self):
        sector_id = self.job_l[self.comboBox.currentIndex()]['typeid']
        word_type_id = self.word_type_l[self.comboBox_2.currentIndex()]['typeid']
        batch_keyword_str = self.check_format()
        if batch_keyword_str:
            try:
                url = f'{self.parent_ui.main_page.domain}/index.php?m=keywords&c=keywords&a=add&json=1'
                params = {}
                params['dosubmit'] = '提交'
                params['types'] = '1'
                params['keywords[sectorid]'] = sector_id
                params['keywords[typeid]'] = word_type_id
                params['keywords[setting]'] = batch_keyword_str.strip()
                params['pc_hash'] = self.parent_ui.main_page.pc_hash
                print(params)
                res = self.session.post(url, headers=self.headers, cookies=self.cookies, data=params).json()
                print("res", res)
                if res['msg'] == '操作成功！':
                    self.parent_ui.main_page.return_msg_update(f"关键词添加成功")
                    self.textEdit.clear()
                else:
                    self.parent_ui.main_page.return_msg_update(f"关键词添加失败, 错误信息: {res['msg']}")
            except Exception as e:
                my_logger.error(e)
        else:
            self.parent_ui.main_page.return_msg_update(f"关键词添加失败, 未检测到关键词")


    def check_format(self):
        return_l = ""
        keywords_l = self.textEdit.toPlainText().split("\n")
        for line in keywords_l:
            line_l = line.split("|")
            if len(line_l) == 3:
                # keyword, alp, belong = line_l[0], line_l[1], line_l[2]
                return_l += line + "\n"
        return return_l


    def connect_slot(self):
        self.pushButton.clicked.connect(self.save)


class JobThread(QThread):
    msg_trigger = pyqtSignal(str)
    finish_trigger = pyqtSignal(list, list)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        try:
            url_word_type = f'{self.ui.parent_ui.main_page.domain}/index.php?m=keywords&c=oauth&a=json_typeid'
            word_type_l = requests.get(url_word_type, headers=self.ui.headers, cookies=self.ui.cookies).json()

            url = f'{self.ui.parent_ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_type&mode=sector'       # 获取行业， 放入comboBox中
            upper_cate_url = f'{self.ui.parent_ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_init'

            job_l = requests.get(url, headers=self.ui.headers, cookies=self.ui.cookies, timeout=5).json()
            upper_cate_l = requests.get(upper_cate_url, headers=self.ui.headers, cookies=self.ui.cookies, timeout=5).json()

            for ele in job_l:
                ele['upper_cate_info'] = []
                for item in upper_cate_l:
                    if ele['typeid'] == item['typeid']:
                        ele['upper_cate_info'].append(item)
        except Exception as e:
            my_logger.error(e)
            self.msg_trigger.emit("无法连接至服务器")
            job_l = []
            word_type_l = []
        finally:
            self.finish_trigger.emit(job_l, word_type_l)

