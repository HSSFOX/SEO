from frontend.baota_action.file_action.file_action import Ui_Form
from backend.baota_action.file_action.create.create import Create
from backend.baota_action.file_action.upload.upload import Upload
from backend.baota_action.file_action.search.search import Search
from backend.baota_action.file_action.sub.sub import Sub
from backend.baota_action.file_action.rename.rename import Rename
from backend.baota_action.file_action.access.access import Access
from backend.baota_action.file_action.delete.delete import Delete


class FileAction(Ui_Form):
    def __init__(self, page, parent_ui, main_page):
        super().setupUi(page)
        self.page = page
        self.parent_ui = parent_ui
        self.main_page = main_page

        self.create_page = Create(self.tab, self.parent_ui, self.main_page)
        self.upload_page = Upload(self.tab_2, self.parent_ui, self.main_page)
        # self.search_page = Search(self.tab_3)
        self.sub_page = Sub(self.tab_4, self.parent_ui, self.main_page)
        self.rename_page = Rename(self.tab_5, self.parent_ui, self.main_page)
        self.access_page = Access(self.tab_6, self.parent_ui, self.main_page)
        self.delete_page = Delete(self.tab_7, self.parent_ui, self.main_page)


