from frontend.SEO_setting.platform_setting.platform_setting import Ui_Form
import re
import requests
import json
from model.utils import seo_logger as my_logger


class PlatformSetting(Ui_Form):
    def __init__(self, page, ui, main_page):
        super().setupUi(page)
        self.page = page
        self.ui = ui
        self.main_page = main_page
        self.seo_info = {}
        self.from_outside = False
        self.connect_slot()

    def save(self):
        if self.from_outside:
            title = self.lineEdit.text()
            keyword = self.lineEdit_2.text()
            description = self.lineEdit_3.text()
            cate_num = self.lineEdit_4.text()  # 栏目数量
            need_sec_cate = self.checkBox_2.isChecked()  # 是否需要子栏目

            words_insert = self.lineEdit_5.text()
            adj_words_insert = self.lineEdit_6.text()
            business_insert = self.lineEdit_7.text()
            brand_insert = self.lineEdit_8.text()
            region_insert = self.lineEdit_9.text()
            setting_name = self.lineEdit_10.text()

            try:
                cate_num = int(cate_num)
                pattern = r'\{([^}]*)\}'
                key_type_l = re.findall(pattern, title)
                if not key_type_l:
                    self.main_page.return_msg_update("格式错误, 请检查格式")
                    return
            except Exception as e:
                self.main_page.return_msg_update("格式错误, 请检查格式")

            return_d = {}
            return_d['dosubmit'] = '提交'
            return_d['name'] = setting_name
            return_d['seoconfig[title]'] = title
            return_d['seoconfig[keywords]'] = keyword
            if self.checkBox.isChecked():         # 随机描述语料
                return_d['seoconfig[ran]'] = 'on'
            else:
                return_d['seoconfig[description]'] = description
            return_d['seoconfig[lanmu]'] = cate_num
            return_d['seoconfig[guanjianci]'] = words_insert
            return_d['seoconfig[xiushici]'] = adj_words_insert
            return_d['seoconfig[yewuci]'] = business_insert
            return_d['seoconfig[pingpaici]'] = brand_insert
            return_d['seoconfig[diquci]'] = region_insert
            return_d['seoconfig[typeid]'] = json.loads(self.seo_info['content'])['typeid']
            return_d['pc_hash'] = self.main_page.pc_hash

            try:
                url = f'{self.main_page.domain}/index.php?m=seoconfig&c=seoconfig&a=edit&json=1&id={self.seo_info["id"]}'
                response = requests.post(url, headers=self.main_page.headers, cookies=self.main_page.cookies, data=return_d).json()
            except Exception as e:
                my_logger.error(e)
            else:
                if response.get('msg') == '':
                    self.main_page.return_msg_update('SEO配置更新成功')
                    self.ui.main()
                    self.self_clear()
                else:
                    self.main_page.return_msg_update('SEO配置更新失败')

    def self_clear(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()  # 栏目数量
        self.checkBox.setChecked(False)     # 随机描述
        self.checkBox_2.setChecked(False)   # 是否需要子栏目

        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()
        self.lineEdit_10.clear()

        self.from_outside = False

    def connect_slot(self):
        self.pushButton.clicked.connect(self.save)