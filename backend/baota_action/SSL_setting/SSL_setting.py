from frontend.baota_action.SSL_setting.SSL_setting import Ui_Form
from backend.baota_action.SSL_setting.set_table import SetTable
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import logging
import configparser
import collections
from urllib.parse import urlparse, urlsplit
# from backend.baota_action.SSL_setting.SSL_DNS_setting.SSL_Dns_Pod_setting import SSL_Dns_Pod_setting
# from backend.baota_action.SSL_setting.SSL_DNS_setting.SSL_Ali_Dns_setting import SSL_Ali_Dns_setting
# from backend.baota_action.SSL_setting.SSL_DNS_setting.SSL_Cloud_Flare_setting import SSL_Cloud_Flare_setting



class SSLSetting(Ui_Form):
    def __init__(self, page, ui, main_page):
        super().setupUi(page)
        self.page = page
        self.main_page = main_page
        self.ui = ui

        self.set_default_value()
        self.refresh()
        self.connect_slot()

    def refresh(self):
        if self.main_page.bt_sign:
            # self.read_dns_setting()
            self.t_refresh = RefreshSites(self.main_page)
            self.t_refresh.start()
            self.t_refresh.finish_trigger.connect(self.table_insert)
        else:
            self.main_page.return_msg_update("请先登录宝塔！")

    # def read_dns_setting(self):
    #     self.comboBox.clear()
    #     self.comboBox_d = collections.OrderedDict()
    #     self.comboBox_d['手动解析'] = {}
    #     self.comboBox.addItem('手动解析')
    #     config = configparser.ConfigParser()
    #     try:
    #         config.read('config/config.ini')  # 读取 config.ini 文件
    #         if config.has_section('AliDns') and config['AliDns'].get('Key') and config['AliDns'].get('Value'):
    #             self.comboBox_d['AliDns'] = {'key': config['AliDns'].get('Key'), 'value': config['AliDns'].get('Value')}
    #             self.comboBox.addItem("阿里云DNS")
    #         else:
    #             self.comboBox_d['AliDns'] = {}
    #             self.comboBox.addItem("阿里云DNS (未配置)")
    #
    #         if config.has_section('DnsPod') and config['DnsPod'].get('Key') and config['DnsPod'].get('Value'):
    #             self.comboBox_d['DnsPod'] = {'key': config['DnsPod'].get('Key'), 'value': config['DnsPod'].get('Value')}
    #             self.comboBox.addItem("DnsPod")
    #         else:
    #             self.comboBox_d['DnsPod'] = {}
    #             self.comboBox.addItem("DnsPod (未配置)")
    #
    #         if config.has_section('CloudFlare') and config['CloudFlare'].get('Key') and config['CloudFlare'].get('Value'):
    #             self.comboBox_d['CloudFlare'] = {'key': config['CloudFlare'].get('Key'), 'value': config['CloudFlare'].get('Value')}
    #             self.comboBox.addItem("CloudFlare")
    #         else:
    #             self.comboBox_d['CloudFlare'] = {}
    #             self.comboBox.addItem("CloudFlare (未配置)")
    #         self.pushButton.hide()      # 手动DNS配置隐藏button （仅第一次）
    #     except Exception as e:
    #         logging.error(e, exc_info=True)

    def table_insert(self, web_l):
        self.current_sites_l = web_l
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()

        all_header_combobox = []
        self.tableWidget.setRowCount(len(web_l))
        for row, account_info in enumerate(web_l):
            self.tableWidget.setRowHeight(row, 60)
            checkBox = QCheckBox()
            checkBox.setCheckState(Qt.Unchecked)
            cb_layout = QHBoxLayout()
            cb_layout.addWidget(checkBox)
            cb_widget = QWidget()
            cb_widget.checkbox = checkBox

            cb_widget.checkState = checkBox.checkState
            cb_widget.setLayout(cb_layout)
            all_header_combobox.append(checkBox)

            account_name_w = QTableWidgetItem(str(account_info['name']))

            self.tableWidget.setCellWidget(row, 0, cb_widget)
            self.tableWidget.setItem(row, 1, account_name_w)

            self.center(account_name_w)
        self.tableWidget.headerBox.clicked.connect(lambda: self.tableWidget.change_state(all_header_combobox))  # 行表头复选框单击信号与槽

    def set_default_value(self):
        self.frame.hide()
        SetTable(self.tableWidget, self.main_page).main()
        # self.read_dns_setting()

    def file_verify(self):
        self.frame.hide()

    def dns_verify(self):
        self.frame.show()

    def connect_slot(self):
        self.radioButton.toggled.connect(self.file_verify)
        self.pushButton_2.clicked.connect(self.apply_cert)
        self.pushButton_3.clicked.connect(self.refresh)

    def apply_cert(self):
        check_l = self.get_check_l()
        self.t_apply_cert = ApplyCert(self.main_page, check_l)
        self.t_apply_cert.start()
        self.t_apply_cert.update_table_trigger.connect(self.update_table_status)
        self.t_apply_cert.finish_trigger.connect(self.update_table_status)

    def update_table_status(self, row, row_result):
        if row_result.get('status'):
            status_w = QTableWidgetItem(f"申请证书失败，失败原因: {row_result['msg']}")
        else:
            status_w = QTableWidgetItem(f"申请证书成功")
        self.tableWidget.setItem(row, 2, status_w)

    def get_check_l(self):
        sum_l = []
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.cellWidget(row, 0).checkbox.isChecked():
                row_info = self.current_sites_l[row]           # 安全一点
                row_info['row'] = row
                sum_l.append(row_info)
        return sum_l

    def center(self, value):
        # font = QFont()
        # font.setFamily("微软雅黑")
        value.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)  # 对齐
        # value.setFont(font)


class RefreshSites(QThread):
    msg_trigger = pyqtSignal(str)
    finish_trigger = pyqtSignal(list)

    def __init__(self, main_page):
        super().__init__()
        self.main_page = main_page

    def run(self):
        try:
            web_l = self.main_page.bt.select_cat({'type': 0})
            print(web_l)
            cert_l = self.main_page.bt.get_cert_list()
            print(cert_l)

            return_l = self.cert_filter(web_l['data'], [self.get_url_without_domain(ele['subject']) for ele in cert_l])
            self.finish_trigger.emit(return_l)
        except Exception as e:
            logging.error(e, exc_info=True)

    def cert_filter(self, total_site_l, cert_site_l):
        return_l = []
        for site_data in total_site_l:
            if self.get_url_without_domain(site_data['name']) not in cert_site_l:
                return_l.append(site_data)
        return return_l

    def get_url_without_domain(self, url):
        url_info = urlsplit(url.strip())
        full_domain = url_info.hostname
        if not full_domain:
            full_domain = url
        domain = ".".join(full_domain.split(".")[-2:])
        return domain


class ApplyCert(QThread):
    msg_trigger = pyqtSignal(str)
    update_table_trigger = pyqtSignal(int, dict)
    finish_trigger = pyqtSignal()

    def __init__(self, main_page, check_list):
        super().__init__()
        self.main_page = main_page
        self.check_list = check_list

    def run(self):
        for site_data in self.check_list:
            print(site_data)
            domains_l = self.get_domains(site_data)
            site_data['domains'] = domains_l
            res = self.apply_cert(site_data)
            self.update_table_trigger.emit(site_data['row'], res)

    def get_domains(self, site_data):          # 获取该域名下的子域名
        domains_l = self.main_page.bt.get_sites_domain({'id': site_data['id']})
        return domains_l

    def apply_cert(self, site_data):
        params = {'domains': [ele['name'] for ele in site_data['domains']['domains']],
                  'id': site_data['id'],
                  'auth_to': site_data['id'],
                  'auto_wildcard': '1'
                  }

        res = self.main_page.bt.apply_cert_api(params)
        return res
