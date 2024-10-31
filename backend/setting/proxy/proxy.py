from PyQt5 import QtCore, QtGui, QtWidgets
from frontend.setting.proxy.proxy import Ui_Form
from backend.setting.proxy.HTTP.HTTP import UI_HTTP
from backend.setting.proxy.SOCKS.SOCKS import SOCKS as SOCKS_UI


class Proxy(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(Proxy, self).__init__()
        self.setupUi(self)

        self.http_page = UI_HTTP(self.tab, self)
        self.socks_page = SOCKS_UI(self.tab_2, self)



