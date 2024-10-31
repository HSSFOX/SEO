from frontend.baota_action.ip_ban.ip_ban import Ui_Form


class IPBan(Ui_Form):
    def __init__(self, page):
        super().setupUi(page)
        self.page = page