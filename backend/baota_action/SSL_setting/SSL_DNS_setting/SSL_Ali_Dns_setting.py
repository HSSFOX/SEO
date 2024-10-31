from frontend.baota_action.SSL_setting.SSL_DNS_setting.SSL_Dns_Pod_setting import Ui_Form
from PyQt5.QtWidgets import *





class SSL_Ali_Dns_setting(QWidget, Ui_Form):
    def __init__(self, main_page, dns_setting):
        super().__init__()
        self.setupUi(self)
        self.main_page = main_page
        self.dns_setting = dns_setting

        self.set_default_value()
        self.connect_slot()

    def set_default_value(self):
        if self.dns_setting.get('key'):
            self.lineEdit.setText(self.dns_setting['key'])
        if self.dns_setting.get('value'):
            self.lineEdit_2.setText(self.dns_setting['value'])

    def save(self):
        self.close()

    def connect_slot(self):
        self.pushButton.clicked.connect(self.save)
        self.pushButton_2.clicked.connect(self.close)

    def closeEvent(self, event):
        self.main_page.hide_loading_label()
        event.accept()                      # 允许正常关闭

