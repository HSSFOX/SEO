from frontend.baota_action.file_action.search.search import Ui_Form
from api_requests.BtAPI import Bt


class Search(Ui_Form):
    def __init__(self, page):
        super().setupUi(page)
        self.page = page
        self.connect_slot()

    def search(self):
        if self.radioButton.isChecked():
            self.search_by_word()
        elif self.radioButton_2.isChecked():
            self.search_by_ext()
        elif self.radioButton_3.isChecked():
            self.search_by_re()
        else:
            print("请选择其中至少一个选项！")

    def search_by_word(self):
        word = self.lineEdit_2.text()
        # Bt(bt_panel='', key='').search_file()

    def search_by_ext(self):
        ext = self.lineEdit_2.text()

    def search_by_re(self):
        re = self.lineEdit_2.text()

    def connect_slot(self):
        self.pushButton.clicked.connect(self.search)