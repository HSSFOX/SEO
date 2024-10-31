from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from frontend.words_management.word_management import Ui_Form
from backend.word_management.add_word.add_word import AddWord
from backend.word_management.batch_add.batch_add import BatchAdd
import requests
from backend.word_management.set_table import SetTable
from model.utils import word_management_logger as my_logger
import datetime
from backend.word_management.table_insertion import TableInsertion
import logging


class WordManagement(Ui_Form):
    def __init__(self, page, main_page):
        super().setupUi(page)
        self.page = page
        self.main_page = main_page
        self.cookies = main_page.cookies
        self.headers = main_page.headers
        self.add_word_page = AddWord(self.tab, self)
        self.batch_word_page = BatchAdd(self.tab_2, self)
        # self.tableWidget.action1 = QAction("修改")
        SetTable(self.tableWidget, main_page).main()
        self.tableWidget.action1 = QAction("删除")
        self.tableWidget.popup_menu.addAction(self.tableWidget.action1)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.page = 0
        self.max_page = 0
        self.row_limit = 100
        self.job_l = []
        self.word_type_l = []
        self.words_l = []
        self.sum_words_l = []
        self.session = requests.session()
        self.main()

        self.connect_slot()

    def main(self):
        self.t_job = JobThread(self)
        self.t_job.start()
        self.t_job.msg_trigger.connect(self.return_msg)
        self.t_job.trigger.connect(self.add_job)

    def return_msg(self, msg):
        self.main_page.return_msg_update(str(msg))

    def get_current_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_job(self, job_l, word_type_l):
        self.job_l = job_l
        self.word_type_l = word_type_l
        self.comboBox.addItems([ele['name'] for ele in self.job_l])
        self.comboBox_2.addItems(['全部'] + [ele['name'] for ele in self.word_type_l])

    def insert_table(self):
        self.update_labels()
        TableInsertion(self.tableWidget).table_main(self.words_l[self.page * self.row_limit:self.page * self.row_limit + self.row_limit])

    def next_page(self):
        self.page += 1
        self.insert_table()

    def prev_page(self):
        self.page -= 1
        self.insert_table()

    def update_labels(self):
        self.max_page = len(self.words_l) // self.row_limit             # 更新最大页数
        if self.page == 0:
            self.pushButton_2.setEnabled(False)
        else:
            self.pushButton_2.setEnabled(True)
        if self.page == self.max_page:
            self.pushButton_3.setEnabled(False)
        else:
            self.pushButton_3.setEnabled(True)
        self.label_5.setText(f"当前第{self.page + 1}页")

    def search(self):
        self.lineEdit.clear()       # 清空搜索内容
        url = f'{self.main_page.domain}/index.php?m=keywords&c=oauth&a=json_seoconfig_ke'
        type_id = self.word_type_l[self.comboBox_2.currentIndex() - 1]['typeid'] if self.comboBox_2.currentIndex() > 0 else ''
        params = {'typeid': type_id,
                  'sectorid': self.job_l[self.comboBox.currentIndex()]['typeid'],
                  'pc_hash': self.main_page.pc_hash,}
        try:
            self.sum_words_l = requests.get(url, headers=self.headers, cookies=self.cookies, params=params).json()
            self.words_l = self.sum_words_l
        except Exception as e:
            print(str(e))
            my_logger.error(e)
        else:
            self.insert_table()

    def word_search(self):
        search_word = self.lineEdit.text()
        self.page = 0               # 搜索时重置页面数
        self.max_page = 0
        self.words_l = [ele for ele in self.sum_words_l if search_word in ele['keyword'] or search_word in ele['pinyin']]
        self.insert_table()

    def connect_slot(self):
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.prev_page)
        self.pushButton_3.clicked.connect(self.next_page)
        self.pushButton_4.clicked.connect(self.delete_keyword)

        self.lineEdit.textChanged.connect(self.word_search)
        self.tableWidget.action1.triggered.connect(self.single_delete)

    def single_delete(self):
        row = self.tableWidget.row
        row_info = self.words_l[row + self.page * self.row_limit]  # 安全一点
        params = {'kid': row_info['kid'], 'pc_hash': self.main_page.pc_hash}
        url = f'{self.main_page.domain}/index.php?m=keywords&c=keywords&a=delete&json=1'
        try:
            res = self.session.get(url, headers=self.headers, cookies=self.cookies, params=params).json()
            if res.get('msg') == '操作成功！':
                self.main_page.return_msg_update(f"关键词 {row_info['keyword']} 删除成功")
            else:
                self.main_page.return_msg_update(f"关键词 {row_info['keyword']} 删除失败, 错误信息: {res['msg']}")
        except Exception as e:
            my_logger.error(e)
            logging.error(e, exc_info=True)
            self.main_page.return_msg_update(f"关键词删除失败, 错误信息: {str(e)}")
        else:
            self.tableWidget.hideRow(row)

    def delete_keyword(self):
        url = f'{self.main_page.domain}/index.php?m=keywords&c=keywords&a=delete&json=1'
        try:
            for row in range(self.tableWidget.rowCount()):
                if self.tableWidget.cellWidget(row, 0).checkbox.isChecked():
                    row_info = self.words_l[row + self.page * self.row_limit]  # 安全一点
                    params = {'kid': row_info['kid'], 'pc_hash': self.main_page.pc_hash}
                    res = self.session.get(url, headers=self.headers, cookies=self.cookies, params=params).json()
                    if res.get('msg') == '操作成功！':
                        self.main_page.return_msg_update(f"关键词 {row_info['keyword']} 删除成功")
                    else:
                        self.main_page.return_msg_update(f"关键词 {row_info['keyword']} 删除失败, 错误信息: {res['msg']}")
        except Exception as e:
            my_logger.error(e)
            print(str(e))
            self.main_page.return_msg_update(f"关键词删除失败, 错误信息: {str(e)}")
        else:
            self.search()


class JobThread(QThread):
    msg_trigger = pyqtSignal(str)
    trigger = pyqtSignal(list, list)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        try:
            url_word_type = f'{self.ui.main_page.domain}/index.php?m=keywords&c=oauth&a=json_typeid'
            word_type_l = requests.get(url_word_type, headers=self.ui.headers, cookies=self.ui.cookies).json()



            url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_type&mode=sector'       # 获取行业， 放入comboBox中
            upper_cate_url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_init'
            job_l = requests.get(url, headers=self.ui.headers, cookies=self.ui.cookies, timeout=5).json()
            upper_cate_l = requests.get(upper_cate_url, headers=self.ui.headers, cookies=self.ui.cookies, timeout=5).json()

            for ele in job_l:
                ele['upper_cate_info'] = []
                for item in upper_cate_l:
                    if ele['typeid'] == item['typeid']:
                        ele['upper_cate_info'].append(item)
        except Exception as e:
            my_logger.error(e)
            print("无法连接至服务器！")
            self.msg_trigger.emit("无法连接至服务器！")
            job_l = []
            word_type_l = []
        finally:
            self.trigger.emit(job_l, word_type_l)

