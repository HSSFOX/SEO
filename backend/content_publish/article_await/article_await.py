import time
import logging
from frontend.content_publish.artticle_await.article_await import Ui_Form
import requests
from backend.content_publish.article_count.set_table import SetTable
from backend.auto_publish.auto_publishment.auto_publishment import GetAvailableLinkageId            # 用于获取文章内容数量
import os
from model.utils import content_publish_logger as my_logger
import random
import re
import datetime
from PyQt5.QtCore import *
from backend.content_publish.article_await.set_table import SetTable
from backend.content_publish.article_await.table_insertion import TableInsertion


class ArticleAwait(Ui_Form):
    def __init__(self, page, parent_ui):
        super().__init__()
        self.setupUi(page)
        self.parent_ui = parent_ui
        SetTable(self.tableWidget, self.parent_ui.main_page).main()
        self.connect_slot()

    def get_path_check(self):
        path = self.parent_ui.lineEdit.text()
        if not path:
            self.parent_ui.main_page.return_msg_update("请先选择路径！")
            return
        if os.path.exists(path):
            self.find_txt_under_path(path)
        else:
            self.parent_ui.main_page.return_msg_update("请选择有效路径！")

    def find_txt_under_path(self, path):
        files_d = self.get_all_folders(path, ['.txt'])
        files_l = [{"name": k, "count": len(v)} for k, v in files_d.items()]

        TableInsertion(self.tableWidget).table_main(files_l)
        print(files_d)

    def get_all_folders(self, folder_path, suffix_l):             # 获取文件夹下的所有文件
        folders = {}
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isdir(file_path) and file_name != '已上传' and file_name != '已发布':
                folders[file_name] = self.get_all_files(file_path, suffix_l)
        return folders

    def get_all_files(self, folder_path, suffix_l):             # 获取文件夹下的所有文件
        files = []
        for file_name in os.listdir(folder_path):
            for suffix in suffix_l:
                if file_name.endswith(suffix):
                    file_path = os.path.join(folder_path, file_name)
                    if os.path.isfile(file_path):
                        files.append(file_path)
        return files

    def connect_slot(self):
        self.pushButton.clicked.connect(self.get_path_check)

