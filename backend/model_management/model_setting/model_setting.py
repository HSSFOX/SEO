

from frontend.model_management.model_setting.model_setting import Ui_widget
from PyQt5 import QtCore, QtWidgets, QtGui
import requests
from model.utils import my_logger
from tkinter import filedialog, Tk
import os
import logging


class ModelSetting(QtWidgets.QWidget, Ui_widget):
    def __init__(self, ui, model_l, model_content, act=1):
        super().__init__()
        super().setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint|QtCore.Qt.WindowCloseButtonHint)

        self.ui = ui
        self.model_l = model_l
        self.model_content = model_content
        self.act = act          # 1=edit  0=add
        self.program_refer_d = {'68': 'PHPCMS', '69': 'WordPress', '70': 'Z-Blog'}
        self.set_init_value()
        self.connect_slot()

    def set_init_value(self):
        if self.act:
            self.lineEdit.setText(self.model_content['name'])
            self.comboBox.setCurrentText(self.program_refer_d[self.model_content['typeid']])
            if self.model_content['types'] == '1':
                self.radioButton.setChecked(True)
            elif self.model_content['types'] == '2':
                self.radioButton_2.setChecked(True)
            elif self.model_content['types'] == '3':
                self.radioButton_3.setChecked(True)
            elif self.model_content['types'] == '4':
                self.radioButton_4.setChecked(True)
            self.lineEdit_2.setText(self.model_content['category'])
            self.lineEdit_3.setText(self.model_content['style'])
            self.lineEdit_4.setText(self.model_content['image'])
            self.textEdit.setText(self.model_content['remarks'])
            self.textEdit_2.setText(str(self.model_content['rewrite']))
        else:
            self.comboBox.setCurrentText(self.program_refer_d[self.model_content['typeid']])


    def radio_box_exclusive(self, checked_radio_box, radio_boxes_l):
        if checked_radio_box in radio_boxes_l and checked_radio_box.isChecked():
            radio_boxes_l.remove(checked_radio_box)
            for radio_box in radio_boxes_l:
                radio_box.setChecked(False)

    def radio_auto_exclusive(self, radio_button):
        if radio_button.isChecked():
            if radio_button == self.radioButton or radio_button == self.radioButton_2 or radio_button == self.radioButton_3 or radio_button == self.radioButton_4:
                self.radio_box_exclusive(radio_button, [self.radioButton, self.radioButton_2, self.radioButton_3, self.radioButton_4])

        else:           # 确认在一个自定义范围内的radio button不可以被直接点掉导致无radio button被选择
            if radio_button == self.radioButton or radio_button == self.radioButton_2 or radio_button == self.radioButton_3 or radio_button == self.radioButton_4:
                self.check_rest_uncheck(radio_button, [self.radioButton, self.radioButton_2, self.radioButton_3, self.radioButton_4])

    def check_rest_uncheck(self, radio_button, radio_button_l):
        for r in radio_button_l:
            if r.isChecked():
                break
        else:
            radio_button.setChecked(True)

    def save(self):
        if self.act:
            url = f'{self.ui.main_page.domain}/index.php?m=templates&c=index&a=edit&id={self.model_content["id"]}&json=1'
        else:
            url = f'{self.ui.main_page.domain}/index.php?m=templates&c=index&a=add&json=1'

        return_data = {}
        return_data['dosubmit'] = ''
        return_data['pc_hash'] = self.ui.main_page.pc_hash
        return_data['data[name]'] = self.lineEdit.text()
        return_data['data[typeid]'] = self.model_l[self.comboBox.currentIndex()]['typeid']
        if self.radioButton.isChecked():
            return_data['data[types]'] = '1'
        elif self.radioButton_2.isChecked():
            return_data['data[types]'] = '2'
        elif self.radioButton_3.isChecked():
            return_data['data[types]'] = '3'
        elif self.radioButton_4.isChecked():
            return_data['data[types]'] = '4'
        return_data['data[category]'] = self.lineEdit_2.text()
        return_data['data[style]'] = self.lineEdit_3.text()
        return_data['data[image]'] = self.lineEdit_4.text()
        return_data['data[remarks]'] = self.textEdit.toPlainText()
        return_data['data[rewrite]'] = self.textEdit_2.toPlainText()

        try:
            res = requests.post(url, headers=self.ui.main_page.headers, cookies=self.ui.main_page.cookies, data=return_data).json()
        except Exception as e:
            my_logger.error(e)
            self.ui.main_page.return_msg_update("无法连接至网络")
        else:
            if not res.get('msg'):
                if self.act:
                    self.ui.main_page.return_msg_update(f"模型{self.model_content['name']} 修改成功")
                else:
                    self.ui.main_page.return_msg_update(f"模型{self.lineEdit.text()} 添加成功")
                self.ui.handle_double_click()
                self.close()
            else:
                if self.act:
                    self.ui.main_page.return_msg_update(f"模型{self.model_content['name']} 修改失败")
                else:
                    self.ui.main_page.return_msg_update(f"模型{self.lineEdit.text()} 添加成功")

    def open_static_file(self):
        root = Tk()
        root.withdraw()  # 隐藏主窗口，因为不需要显示整个窗口，只显示文件选择对话框
        file_path = filedialog.askopenfilename()  # 用户选择文件后，文件路径会被存储在file_path变量中
        if file_path:  # 如果用户选择了文件
            response = self.request_url(file_path)
            self.lineEdit_3.setText(response['url'])
            # self.lineEdit_3.setText(file_path)

    def open_image_file(self):
        root = Tk()
        root.withdraw()  # 隐藏主窗口，因为不需要显示整个窗口，只显示文件选择对话框
        file_path = filedialog.askopenfilename()  # 用户选择文件后，文件路径会被存储在file_path变量中
        if file_path:  # 如果用户选择了文件
            response = self.request_url(file_path)
            self.lineEdit_4.setText(response['url'])

    def request_url(self, local_url):
        data = {}
        url = f'{self.ui.main_page.domain}/index.php?m=attachment&c=attachments&a=upload'
        data['upload'] = (local_url, open(os.path.join(local_url), 'rb+'), 'application/octet-stream')
        for i in range(3):
            try:
                response = requests.post(url, cookies=self.ui.main_page.cookies, headers=self.ui.main_page.headers, data=data, files=data).json()
            except Exception as e:
                my_logger.error(e)
                logging.error(e, exc_info=True)
                self.ui.main_page.return_msg_update(f"模型{self.model_content['name']} 上传失败, 错误原因: 网络波动/ Cookies会话过期")
            else:
                print(1111111111, response)
                return response
        return {"url": ""}

    def connect_slot(self):
        self.radioButton.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton))
        self.radioButton_2.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_2))
        self.radioButton_3.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_3))
        self.radioButton_4.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_4))

        self.pushButton.clicked.connect(self.open_static_file)
        self.pushButton_2.clicked.connect(self.open_image_file)
        self.pushButton_3.clicked.connect(self.save)
        self.pushButton_4.clicked.connect(self.close)



