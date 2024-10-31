from frontend.baota_action.static_rules.static_rules import Ui_Form
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import logging


class StaticRules(Ui_Form):
    def __init__(self, page, ui, main_page):
        super().setupUi(page)
        self.page = page
        self.main_page = main_page
        self.ui = ui
        self.connect_slot()

    def set_sites_cate(self):
        if self.ui.main_page.bt_sign:
            static_rule_text = self.textEdit.toPlainText()
            self.t = SetStaticRuleThread(self, static_rule_text)
            self.t.start()
            self.t.msg_trigger.connect(self.return_msg)
        else:
            QMessageBox.information(None, '宝塔配置', f'请先登录宝塔！')
            self.ui.main_page.return_msg_update("请先登录宝塔！")

    def return_msg(self, msg):
        self.ui.main_page.return_msg_update(msg)

    def connect_slot(self):
        self.pushButton.clicked.connect(self.set_sites_cate)


class SetStaticRuleThread(QThread):
    msg_trigger = pyqtSignal(str)

    def __init__(self, ui, static_rule_text):
        super().__init__()
        self.ui = ui
        self.static_rule_text = static_rule_text

    def run(self):
        try:
            site_cate_name_index = self.ui.ui.comboBox.currentIndex()
            web_cate_l = self.ui.main_page.bt.get_site_cat()           # 获取宝塔网站分类
            # [{'id': 0, 'name': '默认分类'}, {'id': -2, 'name': '已停止网站'}, {'id': 1, 'name': '测试分类'}, {'id': 2, 'name': '程序分类'}]
            params = {'type': web_cate_l[site_cate_name_index]['id']}
            res = self.ui.main_page.bt.select_cat(params)
            if res.get('data'):
                for web_data in res['data']:
                    try:
                        params = {'data': self.static_rule_text, 'encoding': 'utf-8', 'path': '/www/server/panel/vhost/rewrite/' + web_data['name'] + '.conf'}
                        res = self.ui.main_page.bt.save_file_body(params)
                        if res.get('status'):
                            self.msg_trigger.emit(f"{web_data['name']}伪静态返回: " + res['msg'])
                        else:
                            self.msg_trigger.emit(f"{web_data['name']}伪静态上传失败 失败返回: " + res['msg'])
                    except Exception as e:
                        logging.error(e, exc_info=True)
                        self.msg_trigger.emit(f"{web_data['name']}伪静态上传失败 失败返回: " + str(e))
        except Exception as e:
            logging.error(e, exc_info=True)
            self.msg_trigger.emit(f"伪静态上传失败 失败返回: " + str(e))
