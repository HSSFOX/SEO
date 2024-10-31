from frontend.auto_publish.auto_publish import Ui_Form
# from backend.auto_publish.auto_publishment.auto_publishment import AutoPublishment
from backend.auto_publish.platform_management.platform_management import PlatformManagement
from backend.auto_publish.FTP_management.FTP_management import FTP_management


class AutoPublish(Ui_Form):
    def __init__(self, page, main_page):
        super().setupUi(page)
        self.page = page
        self.main_page = main_page
        self.init_FTP_page = False
        self.platform_management_page = PlatformManagement(self.tab, self, self.main_page)



        self.connect_slot()

    def initializeTabContent(self, tab_index):
        if tab_index == 1:
            if not self.init_FTP_page:
                self.ftp_management_page = FTP_management(self.tab_2, self, self.main_page)
                self.init_FTP_page = True

    def connect_slot(self):
        self.tabWidget.currentChanged.connect(self.initializeTabContent)