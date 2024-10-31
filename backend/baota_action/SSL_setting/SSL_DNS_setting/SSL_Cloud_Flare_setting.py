from frontend.baota_action.SSL_setting.SSL_DNS_setting.SSL_Cloud_Flare_setting import Ui_Form
from PyQt5.QtWidgets import *





class SSL_Cloud_Flare_setting(QWidget, Ui_Form):
    def __init__(self, dns_setting):
        super().__init__()
        self.setupUi(self)
        self.dns_setting = dns_setting

    def set_default_value(self):
        self.lineEdit.setText(self.dns_setting['key'])
        self.lineEdit_2.setText(self.dns_setting['value'])