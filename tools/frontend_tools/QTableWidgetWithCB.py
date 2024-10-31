
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class CHeaderTable(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.headerBox = QCheckBox(self.horizontalHeader())

    def resizeEvent(self, event=None):
        super().resizeEvent(event)
        self.headerBox.setGeometry(QRect(11, 10, 20, 20))

    def change_state(self, all_header_combobox):
        if self.headerBox.checkState() == 2:
            for cb in all_header_combobox[:]:
                try:
                    cb.setChecked(True)
                except:
                    all_header_combobox.remove(cb)
        else:
            for cb in all_header_combobox[:]:
                try:
                    cb.setChecked(False)
                except:
                    all_header_combobox.remove(cb)
