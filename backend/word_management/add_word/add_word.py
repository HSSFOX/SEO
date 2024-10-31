from frontend.words_management.add_word.add_word import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
import requests
from collections import OrderedDict
from model.utils import word_management_logger as my_logger
import datetime
import re
from PyQt5.QtWidgets import *


class AddWord(Ui_Form):
    def __init__(self, page, parent_ui):
        super().setupUi(page)
        self.page = page
        self.parent_ui = parent_ui
        self.cookies = parent_ui.cookies
        self.headers = parent_ui.headers
        self.child_refer_d = {}
        self.job_l = []
        self.word_type_l = []
        self.checked_list = []
        self.session = requests.session()

        self.main()
        self.set_default_value()

        self.connect_slot()

    def set_default_value(self):
        self.frame.hide()
        self.frame_2.hide()
        self.extend_labels = False

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
        self.comboBox_3.addItems([ele['name'] for ele in self.word_type_l])

    def save(self):
        keyword = self.lineEdit.text()
        alp = self.lineEdit_2.text()        # 拼音
        sector_id = self.job_l[self.comboBox.currentIndex()]['typeid']
        word_type_id = self.word_type_l[self.comboBox_3.currentIndex()]['typeid']
        try:
            url = f'{self.parent_ui.main_page.domain}/index.php?m=keywords&c=keywords&a=add&json=1'
            params = {}
            params['dosubmit'] = '提交'
            params['types'] = '0'
            params['keywords[sectorid]'] = sector_id
            params['keywords[typeid]'] = word_type_id
            params['keywords[keyword]'] = keyword
            params['keywords[pinyin]'] = alp
            params['keywords[parent]'] = ''
            params['pc_hash'] = self.parent_ui.main_page.pc_hash
            res = self.session.post(url, headers=self.headers, cookies=self.cookies, data=params).json()
            print("res", res)
            if res['msg'] == '操作成功！':
                self.parent_ui.main_page.return_msg_update(f"关键词 - {keyword} 添加成功")
                self.lineEdit.clear()
                self.lineEdit_2.clear()
            else:
                self.parent_ui.main_page.return_msg_update(f"关键词 - {keyword} 添加失败")
        except Exception as e:
            my_logger.error(e)

    def connect_slot(self):
        self.pushButton.clicked.connect(self.save)
        self.pushButton_2.clicked.connect(self.extend_word_labels)
        self.pushButton_3.clicked.connect(self.test_labels_infos)
        self.comboBox_3.currentIndexChanged.connect(self.word_type_change)

    def word_type_change(self):
        if self.comboBox_3.currentIndex():
            self.frame.show()
        else:
            self.frame.hide()

    def extend_word_labels(self):
        if not self.extend_labels:          # 未展开的状态下
            if self.lineEdit.text():
                self.pushButton_2.setText("收起标签库")
                self.extend_labels = True
                self.t_get_word_labels = SearchWordLabels(self)
                self.t_get_word_labels.start()
                self.t_get_word_labels.finish_trigger.connect(self.return_finish_extend_word_labels)
            else:
                self.parent_ui.main_page.return_msg_update("未检测到关键词")

        else:
            self.pushButton_2.setText("展开标签库")
            self.clear_grid_layout(self.gridLayout)
            self.frame_2.hide()
            self.extend_labels = False

    def return_finish_extend_word_labels(self, labels_l):
        if labels_l:
            print(labels_l)
            self.frame_2.show()
            row, column = 0, 0
            while labels_l:
                cb_widget = self.create_checkbox_widget(labels_l.pop())
                self.gridLayout.addWidget(cb_widget, row, column)
                column += 1
                if column == 2:          # grid_layout宽为3
                    row += 1
                    column = 0
        else:
            self.frame_2.hide()
            self.pushButton_2.setText("展开标签库")
            self.extend_labels = False


    def test_labels_infos(self):
        print(self.checked_list)


    def create_checkbox_widget(self, label_info):
        cb_widget = QWidget()
        cb_layout = QHBoxLayout()
        cb_item = QCheckBox(label_info['name'])
        cb_layout.addWidget(cb_item)
        cb_widget.setLayout(cb_layout)
        cb_item.toggled.connect(lambda: self.append_check_info_list(label_info))
        return cb_widget

    def append_check_info_list(self, label_info):
        self.checked_list.append(label_info)

    def clear_grid_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_grid_layout(item.layout())


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


class GetLanmu(QThread):
    msg_trigger = pyqtSignal(str)
    finish_trigger = pyqtSignal(list)

    def __init__(self, ui, parent_id):
        super().__init__()
        self.ui = ui
        self.parent_id = parent_id

    def run(self):
        url = f'{self.ui.parent_ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_submenu&keyid={self.parent_id}'

        try:
            cate_l = requests.get(url, headers=self.ui.headers, cookies=self.ui.cookies).json()
        except Exception as e:
            my_logger.error(e)
            self.msg_trigger.emit("无法连接至服务器")
            cate_l = []
        finally:
            self.finish_trigger.emit(cate_l)


class SearchWordLabels(QThread):
    msg_trigger = pyqtSignal(str)
    finish_trigger = pyqtSignal(list)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.main_page = self.ui.parent_ui.main_page

    def run(self):
        try:
            url = f'{self.main_page.domain}/index.php?m=keywords&c=keywords&a=obtain_keywords&pc_hash={self.main_page.pc_hash}'
            sector_id = self.ui.job_l[self.ui.comboBox.currentIndex()]['typeid']
            keyword = self.ui.lineEdit.text()
            data = {'sectorid': sector_id, 'keyword': keyword}
            response = requests.post(url, headers=self.ui.headers, cookies=self.ui.cookies, data=data).json()
            if response == {"msg":"0"}:
                self.finish_trigger.emit([])
                return
            pattern = re.compile(r'(?<=>).*?(?=<)')
            return_l = []
            for ele in response:
                l = re.findall(pattern, str(ele['name']))
                if l:
                    return_l.append({'name': l[0], 'id': ele['term_id']})
            self.finish_trigger.emit(return_l)
        except Exception as e:
            my_logger.error(e)

