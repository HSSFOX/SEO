from frontend.SEO_setting.program_setting.program_setting import Ui_Form


class ProgramSetting(Ui_Form):
    def __init__(self, page):
        super().setupUi(page)
        self.page = page