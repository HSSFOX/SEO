
from frontend.model_management.model_management import Ui_Form
from backend.model_management.set_table import SetTable
import requests
from model.utils import my_logger
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datetime
from backend.model_management.model_setting.model_setting import ModelSetting
import os, base64
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
import logging
from PyQt5.QtGui import *


class ModelManagement(Ui_Form):
    def __init__(self, ui, main_page):
        super().setupUi(ui)
        self.ui = ui
        self.main_page = main_page
        self.tableWidget.action1 = QAction("修改")
        self.tableWidget.popup_menu.addAction(self.tableWidget.action1)
        SetTable(self.tableWidget, self.main_page).main()
        self.model_l = []
        self.model_program_l = []
        self.get_models()
        self.connect_slot()

    def get_models(self):
        try:
            url = f'{self.main_page.domain}/?m=templates&c=oauth&a=json_type'
            response = requests.get(url, headers=self.main_page.headers, cookies=self.main_page.cookies).json()
            print(response)
            self.model_l = response
        except Exception as e:
            my_logger.error(e)
        else:
            for i, item in enumerate(response):
                self.listWidget.addItem(QListWidgetItem(str(item['name'])))

    def handle_double_click(self):
        row = self.listWidget.currentRow()
        if row != -1:
            current_model = self.model_l[row]
            try:
                response = requests.get(f'{self.main_page.domain}/index.php?m=templates&c=oauth&a=json_init&typeid={current_model["typeid"]}').json()
                self.model_program_l = response
            except Exception as e:
                my_logger.error(e)
            else:
                self.tableWidget.clearContents()
                self.tableWidget.setRowCount(0)
                self.tableWidget.setRowCount(len(response))
                image_download_l = []
                for row, item in enumerate(response):
                    self.tableWidget.setRowHeight(row, 200)
                    serial_no_w = QTableWidgetItem(str(row + 1))
                    category_level_w = QTableWidgetItem(str(item['category']))
                    opt_w = QTableWidgetItem(str(item['name']))
                    static_path_w = QTableWidgetItem(str(item['style']))
                    # image_path_w = QTableWidgetItem(str(item['image']))           # 图片伪懒加载
                    add_time_w = QTableWidgetItem(str(datetime.datetime.fromtimestamp(int(item['time']))))
                    image_download_l.append({'row': row, 'url': f'{self.main_page.domain}{item["image"]}'})


                    self.tableWidget.setItem(row, 0, serial_no_w)
                    self.tableWidget.setItem(row, 1, category_level_w)
                    self.tableWidget.setItem(row, 2, opt_w)
                    self.tableWidget.setItem(row, 3, static_path_w)
                    # self.tableWidget.setItem(row, 4, image_path_w)
                    self.tableWidget.setItem(row, 5, add_time_w)

                    self.center(serial_no_w)
                    self.center(category_level_w)
                    self.center(opt_w)
                    self.center(static_path_w)
                    # self.center(image_path_w)
                    self.center(add_time_w)


                self.t_image_download = ImageDownload(image_download_l)
                self.t_image_download.start()
                self.t_image_download.trigger.connect(self.display_image)

    def display_image(self, row, image_in_base64):
        w = QWidget()
        parent_box = QVBoxLayout(w)
        parent_box.setContentsMargins(0, 0, 0, 0)
        parent_box.setSpacing(0)
        temp_w = QWidget()
        temp_box = QVBoxLayout(temp_w)
        temp_box.setSpacing(9)

        image_data = image_in_base64.replace('data:image/jpeg;base64,', '')
        lbl = QLabel()
        lbl.setMinimumSize(200, 200)
        lbl.setMaximumSize(200, 200)
        if image_data:
            image = QImage()
            image_base64_data = QByteArray.fromBase64(image_data.encode())
            image.loadFromData(image_base64_data)
            lbl.setPixmap(QPixmap(image).scaled(200, 200))
            lbl.setToolTip('<img src="{}" width="{}" height="{}">'.format(self.base64image(image_data), 1200, 1200))
        temp_box.addWidget(lbl)
        temp_w.setLayout(temp_box)
        parent_box.addWidget(temp_w)
        w.setLayout(parent_box)
        w.setStyleSheet('''QWidget{border-width:0px}''')
        self.tableWidget.setCellWidget(row, 4, w)

    def base64image(self, img_base64):
        data = 'data:image/jpeg;base64,%s' % img_base64
        return data

    def center(self, value):
        # font = QFont()
        # font.setFamily("微软雅黑")
        value.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)  # 对齐
        # value.setFont(font)

    def edit_model(self):
        # 修改模板
        row = self.tableWidget.row

        model_setting_content = self.model_program_l[row]
        self.model_setting_ui = ModelSetting(self, self.model_l, model_setting_content)
        self.model_setting_ui.show()

    def connect_slot(self):
        self.listWidget.doubleClicked.connect(self.handle_double_click)
        self.listWidget.action1.triggered.connect(self.add_model)
        self.tableWidget.action1.triggered.connect(self.edit_model)

    # def check_box_update_table(self, check_box):
    #     if check_box.isChecked():
    #         row_count = self.tableWidget.rowCount()

    def add_model(self):
        row = self.listWidget.row
        model = self.model_l[row]
        print(model)

        self.model_setting_ui = ModelSetting(self, self.model_l, model, act=0)
        self.model_setting_ui.show()



class ImageDownload(QThread):
    trigger = pyqtSignal(int, str)

    def __init__(self, download_l):
        super().__init__()
        self.download_l = download_l

    def run(self):
        pool = ThreadPoolExecutor(10)  # 开的线程数
        for rest_image in self.download_l:
            pool.submit(self.task, rest_image)
        pool.shutdown(wait=True)

    def task(self, rest_image):
        row = rest_image['row']
        image = rest_image['url']
        try:
            image_data = self.get_image_base64(image)  # base64 already
            base64display = self.base64image(image_data)
        except Exception as e:
            logging.error(e, exc_info=True)
        else:
            self.trigger.emit(row, base64display)


    def get_image_base64(self, product_main_image):  # product_main_image is the url
        attempt = 0
        s = ''
        while attempt < 3:
            try:
                response = requests.get(product_main_image, timeout=10, proxies=None)
                base64_data = base64.b64encode(BytesIO(response.content).read())
                s = base64_data.decode()
                return s
            except Exception as e:
                attempt += 1
        return s

    def base64image(self, img_base64):
        data = 'data:image/jpeg;base64,%s' % img_base64
        return data



