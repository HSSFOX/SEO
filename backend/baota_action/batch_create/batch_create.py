import collections

from frontend.baota_action.batch_create.batch_create import Ui_Form
from model.utils import bt_action_logger
import datetime
import requests
from tkinter import filedialog, Tk
import os
from PyQt5.QtWidgets import *
import re
import time
import json
import random
import string
from urllib import parse
import logging
from PyQt5.QtCore import *
from api_requests.TokenAPI import Token
from backend.baota_action.batch_create.attempt_ui.attempt_ui import AttemptUI
from collections import OrderedDict
from urllib.parse import urlparse
import tldextract
import copy
from ping3 import ping
from api_requests.RedisAPI import RedisDb
import configparser


class BatchCreate(Ui_Form):
    def __init__(self, page, ui, main_page):
        super().setupUi(page)
        self.page = page
        self.ui = ui
        self.main_page = main_page
        self.model_type_refer_d = {'1': 'PC站', '2': '有对应PC站的移动站', '3': '独立移动站', '4': '自适应'}

        self.frame.hide()
        self.seo_setting_l = []
        self.seo_words_typeid_l = []
        self.model_l = []
        self.model_program_l = []            # 当前模板下的程序
        self.record_no_refer_d = {}
        self.refresh_seo()
        self.connect_slot()
        self.get_models()
        self.lineEdit_2.setText("2")
        self.task_running = False

    def request_seo_setting(self):
        url = f'{self.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_seoconfig'
        words_url = f'{self.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_type&mode=seoconfig'       # 获取词性的type id e.g. 品牌词、业务词、修饰词的type_id
        try:
            self.seo_setting_l = requests.get(url, headers=self.main_page.headers, cookies=self.main_page.cookies).json()
            self.seo_words_typeid_l = requests.get(words_url, headers=self.main_page.headers, cookies=self.main_page.cookies).json()
        except Exception as e:
            bt_action_logger.error(e)
            self.main_page.return_msg_update(str(e))
        else:
            self.comboBox_2.clear()
            self.comboBox_2.addItems([ele['name'] for ele in self.seo_setting_l])

    def refresh_seo(self):
        self.request_seo_setting()

    def get_current_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def connect_slot(self):
        self.pushButton.clicked.connect(self.select_install_program)
        self.pushButton_2.clicked.connect(self.start_go)
        self.pushButton_3.clicked.connect(self.refresh_seo)
        self.pushButton_4.clicked.connect(self.get_models)
        self.comboBox.currentIndexChanged.connect(self.current_model_changed)
        # self.radioButton.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton))
        # self.radioButton_2.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_2))
        self.radioButton_3.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_3))
        self.radioButton_4.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_4))
        self.radioButton_5.toggled.connect(lambda: self.radio_auto_exclusive(self.radioButton_5))

    def radio_box_exclusive(self, checked_radio_box, radio_boxes_l):
        if checked_radio_box in radio_boxes_l and checked_radio_box.isChecked():
            radio_boxes_l.remove(checked_radio_box)
            for radio_box in radio_boxes_l:
                radio_box.setChecked(False)

    def radio_auto_exclusive(self, radio_button):
        if radio_button.isChecked():
            # if radio_button == self.radioButton or radio_button == self.radioButton_2:
            #     self.radio_box_exclusive(radio_button, [self.radioButton, self.radioButton_2, self.radioButton_3])
            if radio_button == self.radioButton_3 or radio_button == self.radioButton_4 or radio_button == self.radioButton_5:
                self.radio_box_exclusive(radio_button, [self.radioButton_3, self.radioButton_4, self.radioButton_5])
                if radio_button == self.radioButton_5:
                    self.frame.show()
                else:
                    self.frame.hide()
        else:           # 确认在一个自定义范围内的radio button不可以被直接点掉导致无radio button被选择
            # if radio_button == self.radioButton or radio_button == self.radioButton_2:
            #     self.check_rest_uncheck(radio_button, [self.radioButton, self.radioButton_2])
            if radio_button == self.radioButton_3 or radio_button == self.radioButton_4 or radio_button == self.radioButton_5:
                self.check_rest_uncheck(radio_button, [self.radioButton_3, self.radioButton_4, self.radioButton_5])


    def check_rest_uncheck(self, radio_button, radio_button_l):
        for r in radio_button_l:
            if r.isChecked():
                break
        else:
            radio_button.setChecked(True)

    def get_models(self):
        self.comboBox.clear()
        try:
            url = f'{self.main_page.domain}/?m=templates&c=oauth&a=json_type'
            response = requests.get(url, headers=self.main_page.headers, cookies=self.main_page.cookies).json()
            self.model_l = response
        except Exception as e:
            bt_action_logger.error(e)
        else:
            self.comboBox.addItems([ele['name'] for ele in self.model_l])
            # self.current_model_changed()

    def current_model_changed(self):
        if self.comboBox.currentIndex() != -1:
            current_model = self.model_l[self.comboBox.currentIndex()]
            try:
                response = requests.get(
                    f'{self.main_page.domain}/index.php?m=templates&c=oauth&a=json_init&typeid={current_model["typeid"]}').json()
                self.model_program_l = response
            except Exception as e:
                bt_action_logger.error(e)
            else:
                # self.comboBox_3.clear()
                # self.comboBox_3.addItems(list(set([self.model_type_refer_d[ele['types']] for ele in self.model_program_l])))
                temp_types_l = list(set([self.model_type_refer_d[ele['types']] for ele in self.model_program_l]))
                if 'PC站' in temp_types_l:
                    self.checkBox_2.show()
                else:
                    self.checkBox_2.hide()
                    self.checkBox_2.setChecked(False)
                if '有对应PC站的移动站' in temp_types_l:
                    self.checkBox_3.show()
                else:
                    self.checkBox_3.hide()
                    self.checkBox_3.setChecked(False)
                if '独立移动站' in temp_types_l:
                    self.checkBox_4.show()
                else:
                    self.checkBox_4.hide()
                    self.checkBox_4.setChecked(False)
                if '自适应' in temp_types_l:
                    self.checkBox_5.show()
                else:
                    self.checkBox_5.hide()
                    self.checkBox_5.setChecked(False)

    def start_go(self):
        if self.check_info_before_start():
            self.enable_disable_ui(False)
            self.clear_log()        # 清理log文件
            if self.radioButton_5.isChecked():
                try:
                    fan_domain_num = int(self.lineEdit_4.text())
                    fan_domain_prefix_len = int(self.lineEdit_3.text())
                except Exception as e:
                    bt_action_logger.error(e)
                    reply = QMessageBox.warning(self, '错误', '请检查泛域名输入格式是否正确')
                    return
            else:
                fan_domain_num = 0
                fan_domain_prefix_len = 0
            # if self.ui.checkBox.isChecked():
            #     status, proxy_type, proxy = self.read_proxy()
            #     if not status:
            #         self.main_page.return_msg_update("请先配置代理！")
            #         QMessageBox(None, "错误提示", "请先配置代理！")
            #         return
            # else:
            #     proxy = None
            self.t_create_sites = BatchCreateSites(self, fan_domain_num, fan_domain_prefix_len)
            self.t_create_sites.start()
            self.t_create_sites.finish_trigger.connect(self.return_finish_create_sites)
            self.t_create_sites.msg_trigger.connect(self.main_page.return_msg_update)

            self.t_refresh_log = ReadLogRefresh()
            self.t_refresh_log.start()
            self.t_refresh_log.msg_trigger.connect(self.return_msg)

    def enable_disable_ui(self, status):
        self.pushButton.setEnabled(status)
        self.pushButton_2.setEnabled(status)
        self.pushButton_3.setEnabled(status)
        self.pushButton_4.setEnabled(status)
        self.lineEdit.setEnabled(status)
        self.lineEdit_2.setEnabled(status)
        self.comboBox.setEnabled(status)
        self.comboBox_2.setEnabled(status)
        # self.comboBox_3.setEnabled(status)
        self.checkBox.setEnabled(status)
        self.checkBox_2.setEnabled(status)
        self.checkBox_3.setEnabled(status)
        self.checkBox_4.setEnabled(status)
        self.checkBox_5.setEnabled(status)
        # self.checkBox_6.setEnabled(status)
        # self.radioButton.setEnabled(status)
        # self.radioButton_2.setEnabled(status)
        self.radioButton_3.setEnabled(status)
        self.radioButton_4.setEnabled(status)
        self.radioButton_5.setEnabled(status)

        self.ui.listWidget.setEnabled(status)
        self.ui.comboBox.setEnabled(status)
        self.ui.pushButton.setEnabled(status)
        self.ui.radioButton.setEnabled(status)
        self.ui.radioButton_2.setEnabled(status)
        self.ui.checkBox.setEnabled(status)
        # self.ui.pushButton_3.setEnabled(status)

        self.textEdit.setEnabled(status)
        self.task_running = not status
        self.main_page.tabWidget.setTabEnabled(1, status)  # 内容发布不允许选取


    def check_info_before_start(self):
        if not self.main_page.bt_sign:
            self.return_qmsg_trigger()
            self.main_page.return_msg_update("请先登陆宝塔！")
            return False
        install_package_path = self.lineEdit.text()
        if not os.path.exists(install_package_path):
            self.main_page.return_msg_update("该安装包不存在！")
            return False
        # if self.comboBox.currentIndex() == -1 or self.comboBox_2.currentIndex() == -1 or self.comboBox_3.currentIndex() == -1:
        if (self.comboBox.currentIndex() == -1 or self.comboBox_2.currentIndex() == -1 or
                (not self.checkBox_2.isChecked() and not self.checkBox_3.isChecked() and not self.checkBox_4.isChecked() and not self.checkBox_5.isChecked())):
            self.main_page.return_msg_update("请确认有可用的模板以及SEO配置！")
            return False
        return True

    def clear_log(self):
        try:
            with open(f'logs/bt_action_logger/bt_action_logger_{str(datetime.datetime.now().date())}.log', 'w') as f:
                f.write('')
        except Exception as e:
            logging.error(e, exc_info=True)

    def return_msg(self, msg):
        self.main_page.textEdit.setText(msg)

    def return_qmsg_trigger(self):
        QMessageBox.information(None, '宝塔配置', f'请先登录宝塔！')

    def return_finish_create_sites(self, attempt_list):
        if attempt_list:
            self.attempt_ui_w = AttemptUI(self, attempt_list)
            self.attempt_ui_w.show()
        else:
            self.enable_disable_ui(True)
            self.t_refresh_log.running_sign = False
            self.main_page.return_msg_update("所有任务已执行完毕！")
            print("备案号: ", self.record_no_refer_d)

    def start_attempt(self, attempt_d):
        self.t_attempt = ReAttempt(self, attempt_d)
        self.t_attempt.start()
        self.t_attempt.finish_trigger.connect(self.return_finish_create_sites)


    def update_web_data_list(self, web_data_list, web_content):
        for web_line in web_content:
            web_line_l = web_line.split("|")
            for ele in web_data_list:
                if ele['name'] == web_line_l[0]:
                    ele['sql'] = int(web_line_l[3])
        return web_data_list

    def remove_sites_type(self, site_type_name, sites_type_id):
        status = self.main_page.bt.remove_sites_type({'id': sites_type_id})
        msg = f"已成功删除临时分类 {site_type_name}"
        bt_action_logger.info(msg)
        # self.main_page.return_msg_update(f"已成功删除临时分类 {site_type_name}")

    def lookup_mysql_file(self, file_name):
        res = self.main_page.bt.get_dir_files({'path': file_name})
        if res.get("FILES"):
            for ele in res['FILES']:
                if '.sql' in ele:
                    return ele.split(";")[0]
        else:
            return None

    def copy_mysql_to_backup(self, mysql_file_path, mysql_file_basename):
        params = {'sfile': mysql_file_path, 'dfile': f'/www/backup/database/{mysql_file_basename}'}
        res = self.main_page.bt.copy_file(params)
        if res.get('status'):
            msg = "备份MySql移动至备份目录"
            bt_action_logger.info(msg)
            # self.main_page.return_msg_update()
            return True
        else:
            # self.main_page.return_msg_update("MySql备份失败")
            msg = "MySql备份失败"
            bt_action_logger.info(msg)
            return False

    def check_db_username_password_update(self, domain, db_data):
        db_name = domain.replace(".", "_")[:16]
        db_username = domain.replace(".", "_")[:16]
        db_password = ''
        for ele in db_data:
            if db_name == ele['name']:
                db_password = ele['password']
                break

        path = f"/www/wwwroot/{domain}/caches/configs/database.php"
        if self.ui.bt_patch:             # 英文版
            params = {'path': path}
        else:                                   # 中文版
            params = {'path': parse.quote_plus(path)}
        print(path, params)
        res = self.main_page.bt.get_file_body(params)
        print("获取数据库文件", res)
        if res.get('status'):
            st_mtime = res['st_mtime']
            content = res['data']
            content = content.replace("I_am_database", db_name)
            content = content.replace("I_am_username", db_username)
            content = content.replace("I_am_password", db_password)
            if self.main_page.bt_patch:
                params = {'data': content, 'path': path}
            else:
                params = {'data': content, 'path': path, 'st_mtime': st_mtime}
            print("修改数据库登录信息: ", params)
            res = self.main_page.bt.save_file_body(params)
            print(res)
            if res.get('status'):
                msg = f"{domain} 数据库配置文件成功！"
                bt_action_logger.info(msg)
                # self.main_page.return_msg_update(f"{domain} 数据库配置文件成功！")
            else:
                msg = f"{domain} 数据库配置文件失败！请手动配置！"
                bt_action_logger.info(msg)
                # self.main_page.return_msg_update(f"{domain} 数据库配置文件失败！请手动配置！")
        else:
            # path = f"/www/wwwroot/{domain}/caches/configs/database.php"
            # params = {'path': path}
            # print(path, params)
            # res = self.main_page.bt.get_file_body(params)

            msg = f"{domain} 数据库获取失败！"
            bt_action_logger.info(msg)
            # self.main_page.return_msg_update(f"{domain} 数据库获取失败！")

    def select_install_program(self):
        root = Tk()
        root.withdraw()  # 隐藏主窗口，因为不需要显示整个窗口，只显示文件选择对话框
        file_path = filedialog.askopenfilename()  # 用户选择文件后，文件路径会被存储在file_path变量中
        if file_path:  # 如果用户选择了文件
            self.lineEdit.setText(file_path)

    def upload_single_file(self, file_path, root_path):
        try:
            basename = os.path.basename(file_path)
            params = {'f_path': file_path, 'f_name': root_path + basename,
                      'f_size': os.path.getsize(file_path), 'f_start': 0, 'blob': file_path}
        except Exception as e:
            bt_action_logger.log(e)
            self.main_page.return_msg_update(str(e))
        else:
            res = self.main_page.bt.upload_file(params, True)
            if res.get('status'):
                msg = f"{basename} 文件上传成功！"
                bt_action_logger.info(msg)
                # self.main_page.return_msg_update(res.get('msg'))
                return True
            else:
                msg = f"{basename} 文件上传失败！"
                bt_action_logger.info(msg)
                # self.main_page.return_msg_update(f"{basename} 文件上传失败！")
                return False

    def zip(self, sfile, dfile):
        params = {'sfile': sfile, 'dfile': dfile, 'type': 'zip', 'coding': 'UTF-8', 'password': ''}
        res = self.main_page.bt.unZip(params)
        # msg = res.get('msg')
        print("压缩结果: ", res)
        if res.get('status'):
            msg = f"{sfile} 解压成功"
        else:
            msg = f"{sfile} 解压失败"
        bt_action_logger.info(msg)
        # self.main_page.return_msg_update(res.get('msg'))
        return res

    def delete_zip_file(self, sfile):
        params = {"path": sfile}
        res = self.main_page.bt.delete_file(params)
        print("删除数据库文件res: ", res)
        if self.main_page.bt_patch:
            msg = f"{sfile} {res.get('result')}"
        else:
            msg = f"{sfile} {res.get('msg')}"
        bt_action_logger.info(msg)
        # self.main_page.return_msg_update(f"{sfile} {res.get('msg')}")

    def get_dir_files(self):
        res = self.main_page.bt.select_cat()            # 从网站列表中选取 而不是从文件中拿的
        return res['data']

    def get_sites_ids(self, web_list):          # web_list为放入批量建站的每一行组成的list
        refer_d = {}
        files_l = self.get_dir_files()
        for web_name in web_list:
            if web_name in [ele['name'] for ele in files_l]:            # 如果在里边儿
                for web_info in files_l:
                    if web_name == web_info['name']:
                        refer_d[web_name] = web_info['id']
                        break
        return refer_d

    def search_web_inside_cate(self, site_type_id):
        params = {'type': site_type_id}
        try:
            res = self.main_page.bt.select_cat(params)
        except Exception as e:
            self.main_page.return_msg_update("获取宝塔分类站群失败！")
        else:
            if res.get('data'):
                return True, res['data']
            else:
                return False, []

    def check_rule(self, sites_l):
        return_add_sites_l = []
        for site_info in sites_l:
            if site_info:           # 去空行
                status, record_no, site_line_info = self.check_line(site_info)
                if status:
                    return_add_sites_l.append(site_line_info)
                    self.record_no_refer_d[site_line_info.split("|")[0].split(",")[0]] = record_no        # 域名与备案号对应
                else:
                    msg = f"该域名字段 {site_line_info} 不符合上传规则！"
                    bt_action_logger.info(msg)
                    # self.main_page.return_msg_update(f"该域名字段 {site_line_info} 不符合上传规则！")
        return_add_sites_l = list(OrderedDict.fromkeys(return_add_sites_l))        # 去重 但不打乱顺序
        return return_add_sites_l

    def check_line(self, site_line):
        site_line = site_line.strip()       # 去除不必要的空格或/r /n
        record_no = self.get_record_no(site_line)           # 获取备案号
        site_info_str = site_line.split("#")[0]
        site_info_l = site_info_str.split("|")
        if len(site_info_l) == 5:
            for site_info_part in site_info_l[2:-1]:                # 检查FTP|数据库是否是个符合要求的数据 即0或1
                if not bool(re.match(r'^[0-1]$', site_info_part)):
                    return False, '', ''
            if not (site_info_l[-1].isdigit() and 1 <= len(site_info_l[-1]) <= 2):      # 检查PHP版本号是否是个单位数或双位数
                return False, '', ''
            return True, record_no, "|".join(site_info_l)             # 通过

        else:
            return False, '', ''

    def get_record_no(self, site_line):
        if '#' in site_line:
            record_no = site_line.split('#')[-1]
            return record_no
        else:
            return ''

    def create_site_cate(self):     # 创建站点分类
        current_timestamp = int(time.time())
        try:
            res = self.main_page.bt.add_site_type({'name': str(current_timestamp)})
        except Exception as e:
            bt_action_logger.error(e)
            return False, current_timestamp
        else:
            if res.get('status'):
                msg = f"创建宝塔分类成功！分类名: {current_timestamp}"
                bt_action_logger.info(msg)
                # self.main_page.return_msg_update(f"创建宝塔分类成功！分类名: {current_timestamp}")
                return True, current_timestamp
            else:
                msg = f"创建宝塔分类失败！"
                bt_action_logger.info(msg)
                # self.main_page.return_msg_update(msg)
                return False, current_timestamp

    def get_site_type(self):
        try:
            res = self.main_page.bt.get_site_cat()
            if self.main_page.bt_patch and res.get('status'):         # 宝塔英文版
                res = res['message']
        except Exception as e:
            bt_action_logger.error(e)
        else:
            return res

    def set_site_cate(self, site_type_name, web_list):         # aka timestamp
        site_cate_l = self.get_site_type()
        site_id = [ele for ele in site_cate_l[::-1] if str(site_type_name) in str(ele['name'])]
        try:
            if site_id:
                res = self.main_page.bt.set_site_type({'site_ids': json.dumps(web_list), 'id': str(int(site_id[0]['id']))})
            else:
                return False, ''
        except Exception as e:
            bt_action_logger.error(e)
            logging.error(e, exc_info=True)
            return False, ''
        else:
            if res.get('status'):
                msg = f'批量添加站点入分类成功！'
                bt_action_logger.info(msg)
                # self.main_page.return_msg_update(f'批量添加站点入分类成功！')
                return True, site_id[0]['id']
            else:
                msg = f'批量添加站点入分类失败！'
                bt_action_logger.info(msg)
                # self.main_page.return_msg_update(f'批量添加站点入分类失败！')
                return False, ''

    def get_chosen_models(self):            # 进行模型程序筛选, 返回成功或失败 以及list [..., ]
        if self.comboBox.currentIndex() >= 0 and self.comboBox_2.currentIndex() >= 0 and (self.checkBox_2.isChecked() or self.checkBox_3.isChecked() or self.checkBox_4.isChecked() or self.checkBox_5.isChecked()):
            # program = self.comboBox_3.currentText()
            program_id_l = self.get_checked_program()
            cate_level_str = self.lineEdit_2.text()
            try:
                if not cate_level_str:
                    cate_level_str = 0
                cate_level = int(cate_level_str)
            except Exception as e:
                self.main_page.return_msg_update(f'栏目格式错误！')
                return False, [], 0
            else:
                # program_type_id = str([k for k, v in self.model_type_refer_d.items() if v == program][0])
                print(444444444444, self.model_program_l)
                program_l = [ele for ele in self.model_program_l if ele['types'] in program_id_l and int(ele['category']) <= int(cate_level)]
                # print("板子: ", program_l)
                if program_l:
                    return True, program_l, cate_level
                else:
                    return False, program_l, 0
        else:
            msg = f'未找到对应模板程序或SEO配置！'
            bt_action_logger.info(msg)
            # self.main_page.return_msg_update(f'未找到对应模板程序或SEO配置！')
            return False, [], 0

    def get_checked_program(self):
        l = []
        if self.checkBox_2.isChecked():
            l.append('1')
        if self.checkBox_3.isChecked():
            l.append('2')
        if self.checkBox_4.isChecked():
            l.append('3')
        if self.checkBox_5.isChecked():
            l.append('4')
        return l

    def bt_remote_download(self, url, path_file):
        base_name = url.split("/")[-1]
        params = {'url': url, 'path': path_file, 'filename': base_name}
        res = self.main_page.bt.download_file(params)           # 加入到下载队列中
        if res.get('status'):
            return True
        else:
            return False

    def loop_check_download_status(self, download_l):
        while download_l:
            try:
                res = self.main_page.bt.get_task_list()
                for item in download_l[:]:
                    if item['url']:
                        base_name = item['url'].split("/")[-1]
                        path = item['path'] + "/" + base_name
                        for ele in res:                 # 如果无res 直接进入zip
                            if path == ele['other']:
                                break           # 它还在下载队列中
                        else:
                            web_ = item['path'].split("/")[-1]
                            msg = f"{web_} 模板下载完毕"
                            bt_action_logger.info(msg)
                            # self.main_page.return_msg_update(f"{web_} 模板下载完毕")
                            download_l.remove(item)
                            zip_res = self.zip(path, item['path'])            # 解压在当前文件夹下
                            if zip_res.get('status'):
                                msg = f"{web_} 模板解压完毕"
                                # self.main_page.return_msg_update(f"{web_} 模板解压完毕")
                            else:
                                msg = f"{web_} 模板解压失败"
                                # self.main_page.return_msg_update(f"{web_} 模板解压失败")
                            bt_action_logger.info(msg)
                time.sleep(1)           # 检查
            except Exception as e:
                lg = logging.getLogger("Error")
                lg.error(e, exc_info=True)


class BatchCreateSites(QThread):
    finish_trigger = pyqtSignal(dict)
    msg_trigger = pyqtSignal(str)

    def __init__(self, ui, fan_domain_num, fan_domain_prefix_len):
        super().__init__()
        self.ui = ui
        self.fan_domain_num = fan_domain_num
        self.fan_domain_prefix_len = fan_domain_prefix_len
        self.main_page = self.ui.main_page
        self.session = requests.session()
        self.redis = RedisDb()
        self.cate_compare_updated_sign = False
        self.slice_range = 10               # 防止英文站一下太多导致的超时
        self.batch_website_content_l = []
        self.download_model_l = []          # 已下载的或者上传的模板
        self.attempt_l = {}                 # 需要重新尝试的列表
        self.random_model_refer_d = {}
        self.extra_url_refer_d = {}

    def run(self):
        try:
            bt_action_logger.info("正在初始化已有站点栏目信息！")

            batch_sites_str = self.ui.textEdit.toPlainText().strip()
            if batch_sites_str:
                batch_sites_l = batch_sites_str.split("\n")
                self.batch_website_content_l = self.ui.check_rule(batch_sites_l)
                status, filter_program_l, cate_level = self.ui.get_chosen_models()  # 获取符合条件的model
                self.ping_detect()
                print(status, filter_program_l, cate_level)
                self.batch_website_content_l = self.check_dynamic_site()
                if status and self.batch_website_content_l:
                    self.allocate_random_model(filter_program_l)
                    seo_d = self.get_seo_info()
                    self.l1, self.l2, self.l3 = GetRandomCateByComparison(self.main_page).main()  # 三级list l1: 所有栏目  l2: 站点未用栏目   l3: 站点未用栏目且有文章

                    # random_cate_l = self.get_cate_level_cates(seo_d['cate_l'], cate_level, seo_d['cate_num'])
                    # print(random_cate_l)
                    # # print(seo_d)
                    # self.finish_trigger.emit(self.attempt_l)
                    # return
                    print(11111, self.l1, self.l2, self.l3)
                    while self.batch_website_content_l:
                        web_content = self.batch_website_content_l[:self.slice_range]  # 分区
                        self.task_go(web_content, seo_d, cate_level)
                        self.batch_website_content_l = self.batch_website_content_l[self.slice_range:]  # 更新区
                    else:
                        root_path = '/www/wwwroot/'
                        program_basename_l = [program['style'].split("/")[-1] for program in self.download_model_l]
                        for basename in program_basename_l:
                            self.ui.delete_zip_file(root_path + basename)       # 将下载下来的模板删除掉
                            print("删除下来下载的模板")
                        bt_action_logger.info("所有任务执行完毕！")
            else:
                self.msg_trigger.emit("未检测到站点！")
        except Exception as e:
            logging.error(e, exc_info=True)
        self.finish_trigger.emit(self.attempt_l)

    def check_dynamic_site(self):           # 泛域名
        # site = ['nc3fitness.com|1|1|1|74#0', 'nc3fitne1231ss.com|1|1|1|74#0']
        if self.ui.radioButton_5.isChecked():
            # num = self.ui.
            # num = 4
            # prefix_len = 5
            # self.fan_domain_num = fan_domain_num
            # self.fan_domain_prefix_len = fan_domain_prefix_len
            l = []
            letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
            while len(l) < self.fan_domain_num * len(self.batch_website_content_l):
                s = ''.join(random.sample(letters, self.fan_domain_prefix_len))
                if s not in l:
                    l.append(s)             # 先随机出不重复的string list
            print(l)
            new_site = []
            while self.batch_website_content_l:                 # 然后一个个pop出来然后重新组成web list
                url = self.batch_website_content_l.pop()
                for _ in range(self.fan_domain_num):
                    prefix = l.pop()
                    new_site.append(f'{prefix}.{url}')
            print(new_site)
            return new_site
        else:
            return self.batch_website_content_l

    def ping_detect(self):          # ping测试
        for website_content_line in self.batch_website_content_l[:]:
            full_domain = website_content_line.split("|")[0].split(',')[0]
            domain = tldextract.extract(full_domain).registered_domain
            if domain:
                for i in range(3):          # ping重试三次
                    status = ping(domain, timeout=10)
                    if status:
                        break
                else:
                    bt_action_logger.info(f"{full_domain} 域名无法ping通，已删除！请手动确认该域名已过白！")
                    self.batch_website_content_l.remove(website_content_line)

    def task_go(self, web_content, seo_d, cate_level):
        try:
            status, cate_name = self.ui.create_site_cate()  # 创建分类
            if status:
                # print("before_web_content", web_content)
                web_content = self.check_and_append_www(web_content)
                # print("after_web_content", web_content)

                status, web_content = self.batch_add_sites(web_content)  # 批量添加
                web_content = self.replace_ori_site_back(web_content)

            if status:
                web_list = web_content
                web_name_list = [ele.split("|")[0] for ele in web_list]  # 从string获取web的域名
                web_name_id_refer_d = self.ui.get_sites_ids(web_name_list)  # 获取域名对应的域名id
                # print(web_name_id_refer_d)
                if web_name_id_refer_d:
                    status, site_id = self.ui.set_site_cate(cate_name,
                                                            list(web_name_id_refer_d.values()))  # 批量添加站点入分类

            if status:
                status, data = self.ui.search_web_inside_cate(site_id)  # 获取分类下的站群信息
                self.ui.remove_sites_type(cate_name, site_id)  # 删除临时创建的分类
                current_site_cate_info = self.ui.ui.site_cate_l[self.ui.comboBox.currentIndex()]

                # 将其添加入 当前选择的网站下属的分类
                res = self.main_page.bt.set_site_type(
                    {'site_ids': json.dumps(list(web_name_id_refer_d.values())),
                     'id': current_site_cate_info['id']})
                if res:
                    msg = f'已添加{str(list(web_name_id_refer_d.keys()))}入当前网站分类 {current_site_cate_info["name"]}'
                else:
                    msg = f'添加{str(list(web_name_id_refer_d.keys()))}入当前网站分类 {current_site_cate_info["name"]} 失败！'
                bt_action_logger.info(msg)
            # print("上传安装包")
            if status:
                # 接下来应该上传安装包
                install_path = self.ui.lineEdit.text()
                if os.path.exists(install_path):
                    root_path = '/www/wwwroot/'
                    basename = os.path.basename(install_path)
                    status = self.ui.upload_single_file(install_path, root_path)  # 上传

            if status:
                web_data_list = [{'name': ele['name'], 'path': ele['path']} for ele in data]
                web_data_list = self.ui.update_web_data_list(web_data_list, web_content)
                # print("进入准备解压", web_data_list)
                basename = os.path.basename(install_path)
                if self.ui.checkBox.isChecked():  # 如果有需要解压文件
                    if basename.endswith('.zip'):
                        for web_data in web_data_list:  # 分批将zip文件打包入目标文件
                            res = self.ui.zip(root_path + basename, web_data['path'])
                            # print("????", res)
                        self.ui.delete_zip_file(root_path + basename)               # 如果有解压 则删除程序zip文件
                        self.backup_export_mysql(web_data_list)
                    else:
                        self.msg_trigger.emit("上传文件的文件类型不支持解压！")
            # print("准备配置模板！", status)
            if status:  # 从这里开始配置模板
                root_path = '/www/wwwroot/'
                for web_data in web_data_list:
                    try:
                        if self.ui.comboBox.currentIndex() == 0:                                        # PHP
                            # print(web_data)
                            # print(root_path)
                            status, program = self.set_web_program(web_data, root_path)         # 随机选择模型程序 并加入到下载队列中
                            # print("program: ", status, program)
                            if status:
                                program_basename = program['style'].split("/")[-1]
                                zip_res = self.ui.zip(root_path + "/" + program_basename, web_data['path'])  # 解压在域名文件夹下
                                # print(zip_res)
                                if zip_res.get('status'):
                                    msg = f"{program_basename} 模板解压完毕"
                                else:
                                    msg = f"{program_basename} 模板解压失败"
                                bt_action_logger.info(msg)
                                status = self.write_static_rule(web_data, str(program['rewrite']))
                                if not status:
                                    self.update_attempt_l(web_data, seo_d, program, '4')
                            self.set_seo_info(web_data, program, seo_d, cate_level)
                    except Exception as e:
                        logging.error(e, exc_info=True)
                        bt_action_logger.info(f"遭遇预期之外的错误, 错误信息: {str(e)}")
            print("attempt_list: ", self.attempt_l)
        except Exception as e:
            bt_action_logger.error(e)
            logging.error(e, exc_info=True)
            self.msg_trigger.emit(f"遭遇预期之外的错误, 错误信息: {str(e)}")

    def allocate_random_model(self, filter_program_l):
        program = None
        for i, web_content_line in enumerate(self.batch_website_content_l[:]):
            all_url = []        # 用于查找这个site对应所有的可用域名
            site = web_content_line.split('|')[0].split(",")[0]       # 域名  第0个
            program = random.choice([ele for ele in filter_program_l if ele != program])
            self.random_model_refer_d[site] = program
            all_url += web_content_line.split("|")[0].split(",")
            if program['types'] == '2':
                line_l = web_content_line.split("|")
                site_l_str = line_l[0] + ",m." + site
                # self.random_model_refer_d[self.extra_web_refer_d[site]['name']] = program
                self.batch_website_content_l[i] = "|".join([site_l_str] + line_l[1:])
                all_url.append('m.' + site)
            self.extra_url_refer_d[site] = all_url

    def batch_add_sites(self, website_content):
        if website_content:
            # print("传进去得: ", website_content)
            res = self.ui.main_page.bt.add_sites({'websites_content': json.dumps(website_content)})
            # print("批量添加返回: ", res)
            if res.get('status'):
                status, website_content = self.check_success_create(res, website_content)
                if status:
                    msg = res.get('msg')
                    bt_action_logger.info(msg)
                    # self.main_page.return_msg_update(f"{res.get('msg')}")
                    return True, website_content
                else:
                    for k, v in res['error'].items():
                        msg = f"站点{k}创建错误 错误信息: {v}"
                        bt_action_logger.info(msg)
                        # self.main_page.return_msg_update(f"站点{k}创建错误 错误信息: {v}")  # 输出第0个error
                        return False, website_content
                    # if website_content:
                    #     self.main_page.return_msg_update(f"{res['error'].values()[0]}")     # 输出第0个error
                    #     return False, website_content
                    # else:
                    #     self.main_page.return_msg_update(f"目标网站已被创建！")
                    #     return False, website_content
            else:
                msg = f"{str(res.get('error'))}"
                bt_action_logger.info(msg)
                # self.main_page.return_msg_update(f"{str(res.get('error'))}")
                return False, ""
        return False, ""

    def check_and_append_www(self, line_l):
        if self.ui.radioButton_4.isChecked():
            for i, line in enumerate(line_l[:]):
                domain = line.split("|")[0]
                if ',' in domain:
                    if 'www.' in domain:
                        return line
                    domain = domain.split(",")[0]
                pure_domain = "www." + tldextract.extract(domain).registered_domain
                line_l[i] = line.replace(domain, domain + "," + pure_domain)
            return line_l
        else:
            return line_l

    def replace_ori_site_back(self, web_content_list):
        for i, web_content in enumerate(web_content_list[:]):
            if ',' in web_content:
                l = web_content.split("|")
                s = l[0].split(",")[0]
                new_l = [s] + l[1:]
                web_content_list[i] = "|".join(new_l)

        return web_content_list

    def check_success_create(self, return_content, ori_web_l):
        if return_content.get('error'):
            if '您添加的域名已存在' in str(return_content['error']):
                pattern = r'\[([^\}]+)\]'
                matches = re.findall(pattern, return_content['msg'])            # 这里是根据已成功的进行筛选
                if matches:
                    sites_l = matches[0].strip().split(",")
                    if sites_l == ['']:
                        return False, []
                    if len(sites_l) == len(ori_web_l):              # 全部为未建过的站
                        return True, ori_web_l
                    else:
                        for ori_web_line in ori_web_l[:]:
                            site = ori_web_line.split("|")[0]
                            if site not in sites_l:
                                ori_web_l.remove(ori_web_line)

                        return True, ori_web_l
            else:           # e.g. PHP版本问题
                return False, []
        return True, ori_web_l

    def write_static_rule(self, web_data, static_rule_text):
        try:
            path = '/www/server/panel/vhost/rewrite/' + web_data['name'] + '.conf'
            params = {'data': static_rule_text, 'encoding': 'utf-8', 'path': path, 'force': 1}
            res = self.ui.main_page.bt.save_file_body(params)
            if res.get('status'):
                msg = f"{web_data['name']} 上传静态规则成功"
            else:
                msg = f"{web_data['name']} 上传静态规则失败, 失败原因: {str(res['msg'])}"
            bt_action_logger.info(msg)
            return res.get('status')
        except Exception as e:
            logging.error(e, exc_info=True)
        return False

    def requests_upload(self, local_url, path):
        base_name = local_url.split("/")[-1]
        res = requests.get(local_url, verify=False)
        content_length = res.headers['content-length']
        blob = (base_name, res.content, 'application/octet-stream')
        params = {'f_path': path, 'f_name': base_name, 'f_size': content_length, 'f_start': 0, 'blob': blob}
        for i in range(3):
            try:
                res = self.main_page.bt.upload_file_dir(params)
                # print("模板的参数: ", params)
                if not res.get('status'):
                    msg = f"{path.split('/')[-1]} 模板文件上传失败"
                    bt_action_logger.info(msg)
                    return res['status']
                else:
                    msg = f"{path.split('/')[-1]} 模板文件上传成功"
                    bt_action_logger.info(msg)
                    return res['status']
            except Exception as e:
                logging.error(e, exc_info=True)
                bt_action_logger.error(e)
                print("模板的参数: ", params)

        return False

    def get_seo_info(self):
        d = {}
        if self.ui.comboBox_2.currentIndex() != -1:
            current_seo_info = json.loads(self.ui.seo_setting_l[self.ui.comboBox_2.currentIndex()]['content'])
            for item in self.ui.seo_words_typeid_l:
                if item['name'] == '修饰词':
                    adj_words_l = self.get_words(item['typeid'], current_seo_info['typeid'])
                    d['adj_words_l'] = adj_words_l
                if item['name'] == '业务词':
                    business_words_l = self.get_words(item['typeid'], current_seo_info['typeid'])
                    d['business_words_l'] = business_words_l
                if item['name'] == '品牌词':
                    brand_words_l = self.get_words(item['typeid'], current_seo_info['typeid'])
                    d['brand_words_l'] = brand_words_l
                if item['name'] == '地区':
                    region_l = self.get_words(item['typeid'], current_seo_info['typeid'])
                    d['region_l'] = region_l
                if item['name'] == '描述':
                    if not current_seo_info.get('description'):
                        description_l = self.get_words(item['typeid'], current_seo_info['typeid'])
                    else:
                        description_l = [current_seo_info['description']]
                    d['description_l'] = description_l

            # keywords_l = [ele['keyword'] for ele in self.get_keywords(current_seo_info['typeid'])]
            cate_l = self.get_cate(current_seo_info['typeid'])
            btree_cate_l = self.build_tree(cate_l)
            cate_num = int(current_seo_info['lanmu'])
            need_cate_son = current_seo_info.get('need_cate_son')       # 需要子栏目  暂时不知道参数 不放入运算
            # random_cate_l = self.get_cate_level_cates(cate_l, cate_level, cate_num)

            d['need_cate_son'] = need_cate_son
            d['cate_num'] = cate_num
            # d['keywords_l'] = self.get_main_long_keywords(random_cate_l)
            d['btree_cate_l'] = btree_cate_l
            d['cate_l'] = cate_l
            # d['random_cate_l'] = random_cate_l
            return d
        else:
            return {}

    def get_main_long_keywords(self, random_cate_l):           # 获取主词和长尾词
        try:
            s = ",".join([ele["linkageid"] for ele in random_cate_l])
            print(55555, s)
            url = f'{self.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_seoconfig_keywords&linkageid={",".join([ele["linkageid"] for ele in random_cate_l])}'
            print(66666666666666666, url)
            res = requests.get(url, headers=self.main_page.headers, cookies=self.main_page.cookies)
            print("主词 长尾词 txt", res.text)
            if not res.text:
                url = f'{self.main_page.domain}/index.php?m=keywords&c=oauth&a=json_seoconfig_ke&sectorid={random_cate_l[0]["typeid"]}'
                try:
                    print("url: ", url)
                    sector_api_res = requests.get(url, headers=self.main_page.headers, cookies=self.main_page.cookies).json()
                    print(sector_api_res)
                except Exception as e:
                    logging.error(e, exc_info=True)
                    bt_action_logger.error(e)
                    return {'keyword': [], 'keywords': []}
                else:
                    l = len(sector_api_res) // 2
                    return {'keyword': [ele["keyword"] for ele in sector_api_res[:l]], 'keywords': [ele['keyword'] for ele in sector_api_res[l:]]}
            else:
                res = res.json()
                if res['keyword'] and res['keywords']:
                    return res
                else:
                    url = f'{self.main_page.domain}/index.php?m=keywords&c=oauth&a=json_seoconfig_ke&sectorid={random_cate_l[0]["typeid"]}'
                    try:
                        print("url: ", url)
                        sector_api_res = requests.get(url, headers=self.main_page.headers,
                                                      cookies=self.main_page.cookies).json()
                        print(sector_api_res)
                    except Exception as e:
                        logging.error(e, exc_info=True)
                        bt_action_logger.error(e)
                        return {'keyword': [], 'keywords': []}
                    else:
                        l = len(sector_api_res) // 2
                        print("从这里出", l)
                        print(444444, {'keyword': [ele["keyword"] for ele in sector_api_res[:l]], 'keywords': [ele['keyword'] for ele in sector_api_res[l:]]})
                        return {'keyword': [ele["keyword"] for ele in sector_api_res[:l]], 'keywords': [ele['keyword'] for ele in sector_api_res[l:]]}
        except Exception as e:
            logging.error(e, exc_info=True)
            bt_action_logger.error(e)
            return {'keyword': [], 'keywords': []}
        else:
            return res

    def set_seo_info(self, web_data, program, seo_info_d, cate_level):
        if seo_info_d:
            current_seo_info = json.loads(self.ui.seo_setting_l[self.ui.comboBox_2.currentIndex()]['content'])

            random_cate_l = self.get_cate_level_cates(seo_info_d['cate_l'][:], cate_level, seo_info_d['cate_num'])
            # print(random_cate_l)
            keywords_l = self.get_main_long_keywords(random_cate_l)
            print(888888888888888888, keywords_l)
            # print("init keywords_l", keywords_l)
            # random_cate_l = seo_info_d['random_cate_l']
            if seo_info_d['description_l']:
                random_description = random.choice(seo_info_d['description_l'])
            else:
                random_description = ""
            if seo_info_d['brand_words_l']:
                random_brand = self.insert_string(current_seo_info['pingpaici'], random.choice(seo_info_d['brand_words_l']))        # 仅随机一个
            else:
                random_brand = ''
            if seo_info_d['region_l']:
                random_region = self.insert_string(current_seo_info['diquci'], random.choice(seo_info_d['region_l']))
            else:
                random_region = ''
            # 从词库中获取最大数量的随机词
            random_inserted_business_l, random_inserted_keywords_l, random_inserted_keyword_l, random_inserted_adj_l = self.get_random_words_l(web_data, current_seo_info, random_description, seo_info_d, keywords_l)
            # print("random list: ", random_inserted_keywords_l, random_inserted_keyword_l)
            title = self.get_attributes_count(current_seo_info['title'], random_inserted_business_l, random_inserted_keyword_l, random_inserted_adj_l, [random_brand], [random_region])
            description = self.get_attributes_count(random_description, random_inserted_business_l, random_inserted_keyword_l, random_inserted_adj_l, [random_brand], [random_region])
            # print("title/ description: ", title, description)
            web_data['title'] = title
            web_data['description'] = description
            web_data['keywords'] = random_inserted_keywords_l
            web_data['keywords_inserted'] = random_inserted_keywords_l
            web_data['cate_l'] = random_cate_l
            web_data['sector_id'] = current_seo_info['typeid']
            web_data['brand'] = random_brand
            web_data['updated_domain'] = "http://" + web_data['name'] + "/"
            # web_data['is_https'] = '1' if self.ui.radioButton.isChecked() else '2'
            web_data['is_https'] = '1'
            web_data['is_www'] = '1' if self.ui.radioButton_4.isChecked() else '0'
            status = True

            if status:
                # 设置 网站TDK设置
                status = self.export_seo_setting(web_data)
                if not status:
                    self.update_attempt_l(web_data, seo_info_d, program, '1')
            else:
                self.update_attempt_l(web_data, seo_info_d, program, '1')  # 0: 重试上传TDK
            if status:      # 加入栏目
                status = self.get_local_cate_from_random_cate_list(web_data, seo_info_d['btree_cate_l'])
                if not status:
                    self.update_attempt_l(web_data, seo_info_d, program, '0')  # 0: 重试上传栏目
                else:
                    # 更新l2, l3
                    if self.cate_compare_updated_sign:          # l2 或 l3有变动的时候才更新
                        self.redis.handle_redis_token('batch_crate_random_cate_comparison_d', json.dumps({'l1': self.l1, 'l2': self.l2, 'l3': self.l3}))
            else:
                self.update_attempt_l(web_data, seo_info_d, program, '0')  # 0: 重试上传栏目

            if status:
                # 更新备案
                status = self.update_record_num(web_data)
                if not status:
                    self.update_attempt_l(web_data, seo_info_d, program, '2')  # 2: 重试上传备案号
            else:
                self.update_attempt_l(web_data, seo_info_d, program, '2')                          # 2: 重试上传备案号

            if status:
                # 更新CMS PHP后台
                status = self.update_local_setting(web_data, program)                          # 最后再更新设置
                if not status:
                    self.update_attempt_l(web_data, seo_info_d, program, '3')
            else:
                self.update_attempt_l(web_data, seo_info_d, program, '3')

    # def get_attributes_count(self, format_string, business_word_l, keyword_l, adj_word, brand_word_l, region_l):
    #     pattern = r'\{([^\}]+)\}'
    #     matches = re.findall(pattern, format_string)
    #     for ele in matches:
    #         count = 1
    #         if "," in ele:
    #             l = ele.split(",")
    #             try:
    #                 count = int(l[-1])
    #             except Exception as e:
    #                 logging.error(e, exc_info=True)
    #                 count = 1
    #         if '修饰词' in ele:
    #             adj = "、".join(adj_word[:count])
    #             format_string = format_string.replace("{" + ele + "}", adj)
    #         if '关键词' in ele:
    #             keyword_l = "、".join(keyword_l[:count])
    #             format_string = format_string.replace("{" + ele + "}", keyword_l)
    #         if '业务' in ele or '业务词' in ele:
    #             business_word = "、".join(business_word_l[:count])
    #             format_string = format_string.replace("{" + ele + "}", business_word)
    #         if '品牌' in ele or '品牌词' in ele:
    #             brand_word = "、".join(brand_word_l[:count])
    #             format_string = format_string.replace("{" + ele + "}", brand_word)
    #         if '地区' in ele or '地区词' in ele:
    #             region_word = "、".join(region_l[:count])
    #             format_string = format_string.replace("{" + ele + "}", region_word)
    #     return format_string

    def get_attributes_count(self, format_string, business_word_l, keyword_l, adj_word, brand_word_l, region_l):
        pattern = r'\{([^\}]+)\}'
        matches = re.findall(pattern, format_string)
        for ele in matches:
            # sub_ele = copy.deepcopy(ele)
            sum_d = collections.OrderedDict()
            s_l = []
            count = 1
            for item in ele.split("|"):
                # 获取一个{...}中的count
                if "," in item:
                    l = item.split(",")
                    try:
                        count = int(l[-1])
                    except Exception as e:
                        logging.error(e, exc_info=True)
                        count = 1
                if '修饰词' in item:
                    sum_d['修饰词'] = count
                    if count > len(adj_word):
                        sum_d['修饰词'] = len(adj_word)
                if '关键词' in item:
                    sum_d['关键词'] = count
                    if count > len(keyword_l):
                        sum_d['关键词'] = len(keyword_l)
                if '业务' in item or '业务词' in item:
                    sum_d['业务词'] = count
                    if count > len(business_word_l):
                        sum_d['业务词'] = len(business_word_l)
                if '品牌' in item or '品牌词' in item:
                    sum_d['品牌词'] = count
                    if count > len(brand_word_l):
                        sum_d['品牌词'] = len(brand_word_l)
                if '地区' in item or '地区词' in item:
                    sum_d['地区词'] = count
                    if count > len(region_l):
                        sum_d['地区词'] = len(region_l)
            print("d: ", sum_d)
            print("keywords_l: ", keyword_l)
            # 组合String replace ele
            if sum_d.get("关键词"):
                while sum_d.get('关键词') != 0:
                    s = ''
                    for k in sum_d:
                        if k == '修饰词':
                            s += random.choice(adj_word)
                        if k == '关键词':
                            s += keyword_l[sum_d[k] - 1]
                            sum_d[k] -= 1
                        if k == '业务词':
                            s += random.choice(business_word_l)
                        if k == '品牌词':
                            s += random.choice(brand_word_l)
                        if k == '地区词':
                            s += random.choice(region_l)
                        # print(k, s)
                    s_l.append(s)
            else:
                s = ''
                for k in sum_d:
                    if k == '修饰词':
                        s += random.choice(adj_word)
                    if k == '关键词':
                        s += keyword_l[sum_d[k] - 1]
                        sum_d[k] -= 1
                    if k == '业务词':
                        s += random.choice(business_word_l)
                    if k == '品牌词':
                        s += random.choice(brand_word_l)
                    if k == '地区词':
                        s += random.choice(region_l)
                s_l.append(s)
            # print(sum_d)
            # print("s_l: ", s_l)
            format_string = format_string.replace("{" + ele + "}", "、".join(s_l))
        return format_string

    def get_random_words_l(self, web_data, current_seo_info, desc, seo_info_d, keywords_l):
        business_word_l, adj_l = seo_info_d['business_words_l'], seo_info_d['adj_words_l']
        title_d = self.return_matches_count(current_seo_info['title'])
        desc_d = self.return_matches_count(desc)
        keyword_d = self.return_matches_count(current_seo_info['keywords'])
        # print(title_d, desc_d, keyword_d)
        sum_d = {'业务词': 0, '关键词': 0, '修饰词': 0, '业务': 0}
        for k in sum_d:                 # 获取在这种情况下需要获取的 词上限 e.g. {'业务': 1, '关键词': 5, '品牌': 1} {'品牌': 1, '关键词': 7} {'关键词': 6}
            v = sum_d[k]
            if title_d.get(k):
                v1 = title_d[k]
            else:
                v1 = 0
            if desc_d.get(k):
                v2 = desc_d[k]
            else:
                v2 = 0
            if keyword_d.get(k):
                v3 = keyword_d[k]
            else:
                v3 = 0
            sum_d[k] = max(v, v1, v2, v3)
        # print(sum_d)
        random_inserted_business_l = []
        random_inserted_keywords_l = []
        random_inserted_adj_l = []
        for k, v in sum_d.items():
            try:
                if k == '业务词' or k == '业务':         # 防止一下无法兼容问题
                    max_v = max(sum_d['业务词'], sum_d['业务'])
                    if len(business_word_l) < max_v:
                        max_v = len(business_word_l)         # 不让它爆出上限
                        bt_action_logger.info(
                            f"{web_data['name']} - {k} 随机词数量已超出词数据大小, 已自动调整，请手动再次确认！")

                    random_business_l = random.sample(business_word_l, max_v)
                    random_inserted_business_l = self.random_l_append_insertion(random_business_l, current_seo_info['yewuci'])
                if k == '关键词':
                    if len(keywords_l['keyword']) < v or len(keywords_l['keywords']) < v:
                        v = min(len(keywords_l['keyword']), len(keywords_l['keywords']))         # 不让它爆出上限
                        bt_action_logger.info(
                            f"{web_data['name']} - {k} 随机词数量已超出词数据大小, 已自动调整，请手动再次确认！")
                        print(f"{web_data['name']} - {k} 随机词数量已超出词数据大小, 已自动调整，请手动再次确认！")
                    random_keyword_l = random.sample(keywords_l['keyword'], v)
                    random_keywords_l = random.sample(keywords_l['keywords'], v)
                    random_inserted_keyword_l = self.random_l_append_insertion(random_keyword_l, current_seo_info['guanjianci'])
                    random_inserted_keywords_l = self.random_l_append_insertion(random_keywords_l, current_seo_info['guanjianci'])
                if k == '修饰词':
                    if len(adj_l) < v:
                        v = len(adj_l)         # 不让它爆出上限
                        bt_action_logger.info(
                            f"{web_data['name']} - {k} 随机词数量已超出词数据大小, 已自动调整，请手动再次确认！")

                    random_adj_l = random.sample(adj_l, v)
                    random_inserted_adj_l = self.random_l_append_insertion(random_adj_l, current_seo_info['xiushici'])
            except Exception as e:
                bt_action_logger.error(e, exc_info=True)
                bt_action_logger.info(f"{web_data['name']} - {k} 随机词数量已超出词数据大小, 已自动调整，请手动再次确认！")
        return random_inserted_business_l, random_inserted_keywords_l, random_inserted_keyword_l, random_inserted_adj_l


    def random_l_append_insertion(self, l, insert_word):
        return_l = []
        for w in l:
            return_l.append(self.insert_string(insert_word, w))
        return return_l

    def return_matches_count(self, format_string):
        pattern = r'\{([^\}]+)\}'
        matches = re.findall(pattern, format_string)
        d = {}
        for ele in matches:
            for item in ele.split("|"):
                try:    # try catch防止没有匹配到
                    count = 1
                    if "," in item:
                        l = item.split(",")
                        try:
                            count = int(l[-1])
                            d[l[0]] = count
                        except Exception as e:
                            logging.error(e, exc_info=True)
                            count = 1
                            d[l[0]] = count
                    else:
                        count = 1
                        d[item] = count
                except Exception as e:
                    logging.error(e, exc_info=True)
        return d

    def update_attempt_l(self, web_data, seo_info_d, program, stage_code):
        if self.attempt_l.get(web_data['name']):
            self.attempt_l[web_data['name']]['stage_code'] += [stage_code]
        else:
            self.attempt_l[web_data['name']] = {'web_data': web_data, 'seo_info_d': seo_info_d, 'program': program, 'stage_code': [stage_code]}  # 0: 上传栏目

    def update_record_num(self, web_data):
        if self.ui.record_no_refer_d.get(web_data['name']):
            token = Token()
            client = token.generateToken('')  # 初始值为空

            client['model'] = 'ICP'
            client['func'] = 'UpdateICP'
            client['icp'] = self.ui.record_no_refer_d[web_data['name']]


            try:
                response = token.sendPostRequestWithToken("http://" + web_data['name'] + "/jiekou.php", client)
            except Exception as e:
                logging.error(e)
                msg = f"{web_data['name']} 网站备案失败 失败原因: {str(e)}"
                bt_action_logger.info(msg)
                return False
            else:
                if response.get('status'):
                    msg = f"{web_data['name']} 网站备案设置更新成功"
                    bt_action_logger.info(msg)
                    # self.msg_trigger.emit(f"{web_data['name']} 网站TDK设置成功")
                    return True
                else:
                    msg = f"{web_data['name']} 网站备案设置更新失败"
                    bt_action_logger.info(msg)
                    # self.msg_trigger.emit(f"{web_data['name']} 网站TDK设置失败")
                    return False
        else:
            msg = f"{web_data['name']} 未检测到该网站备案"
            bt_action_logger.info(msg)
            return True


    def build_tree(self, elements, parent_id=0):
            branch = []

            for element in elements:
                if str(element['parentid']) == str(parent_id):
                    children = self.build_tree(elements, element['linkageid'])
                    if children:
                        element['children'] = children
                    else:
                        element['children'] = []
                    branch.append(element)
            return branch

    def export_seo_setting(self, web_data):
        token = Token()
        client = token.generateToken('')    # 初始值为空

        client['model'] = 'site'
        client['name'] = web_data['brand']
        client['domain'] = "http://" + web_data['name'] + "/"
        client['site_title'] = web_data['title']         # 网站名称
        client['keywords'] = ','.join(web_data['keywords'])
        client['description'] = web_data['description']
        client['is_https'] = web_data['is_https']
        client['is_www'] = web_data['is_www']

        try:
            # print(333333333, client)
            response = token.sendPostRequestWithToken("http://" + web_data['name'] + "/jiekou.php", client)
            # print(response)
        except Exception as e:
            logging.error(e)
            msg = f"{web_data['name']} 网站TDK设置失败 失败原因: {str(e)}"
            bt_action_logger.info(msg)
            return False
        else:
            if response.get('status'):
                msg = f"{web_data['name']} 网站TDK设置成功"
                web_data['updated_domain'] = response['msg']['url']
                bt_action_logger.info(msg)
                # self.msg_trigger.emit(f"{web_data['name']} 网站TDK设置成功")
                return True
            else:
                msg = f"{web_data['name']} 网站TDK设置失败"
                bt_action_logger.info(msg)
                # self.msg_trigger.emit(f"{web_data['name']} 网站TDK设置失败")
                return False

    def get_local_cate_from_random_cate_list(self, web_data, btree_cate_l):
        return_l = []

        def dfs(node, enter_node=True):
            d = {}
            d['name'] = node['name']
            d['refer_id'] = node['linkageid']
            d['parent'] = [{"name": ele['name'], "refer_id": ele['linkageid']} for ele in node['children']]

            for new_node in node['children']:
                dfs(new_node, enter_node=False)
            if not enter_node and node['children']:
                return_l.append(d)
            elif enter_node:
                return_l.append(d)

        for e in web_data['cate_l']:
            for r in btree_cate_l:
                if e['linkageid'] == r['linkageid']:
                    dfs(r)
        # print("------------------------------------------------------------------------------------------------------------------")
        # print(return_l)
        # print("这是传上去的cate_l: ",return_l)
        # for i in range(10):
        token = Token()
        client = token.generateToken('')    # 初始值为空

        client['model'] = 'category'
        client['batch_add'] = return_l
        try:
            url = "http://" + web_data['name'] + "/jiekou.php"
            # print(client)
            response = token.sendPostRequestWithToken(url, client)
            # print("response = = :", response)
            # print("----------------------------------------------------------------------------------------------------------------")
        except Exception as e:
            logging.error(e)
            msg = f"{web_data['name']} 栏目添加失败, 失败原因: {str(e)}"
            bt_action_logger.info(msg)
            return False
        else:
            if response.get('status'):
                msg = f"{web_data['name']} 栏目添加成功"
                bt_action_logger.info(msg)
                # self.msg_trigger.emit(f"{web_data['name']} 栏目添加成功")
                return True
            else:
                msg = f"{web_data['name']} 栏目添加失败"
                bt_action_logger.info(msg)
                # self.msg_trigger.emit(f"{web_data['name']} 栏目添加失败")
                return False

    def update_local_setting(self, web_data, program):
        url = f'{self.main_page.domain}/index.php?m=automatic&c=automatic_admin&a=add&json=1'
        data = {}
        data['dis_type'] = '2'
        data['dosubmit'] = ''
        data['pc_hash'] = self.main_page.pc_hash
        if self.ui.radioButton_5.isChecked():
            data['data[sort]'] = '2'
        else:
            data['data[sort]'] = '1'
        data['data[typeid]'] = web_data['sector_id']
        domain = self.get_domain(web_data['updated_domain'])

        data['data[domain]'] = web_data['updated_domain']
        data['data[token]'] = ''
        if program['types'] == '2':
            if "://www." in web_data['updated_domain']:
                data['data[mobile][]'] = [web_data['updated_domain'].replace("://www.", "://m."), '']
            else:
                data['data[mobile][]'] = [web_data['updated_domain'].replace(domain, 'm.' + domain ), '']
        else:
            data['data[mobile][]'] = []
        data['data[backstage][]'] = [web_data['updated_domain'] + 'myadmin/index.php', 'admin', 'xiaoyu']
        data['data[api]'] = web_data['updated_domain'] + "jiekou.php"

        data['data[baidu_token]'] = ''
        data['data[baidu_rule]'] = '1'
        data['data[order]'] = '3'
        data['data[release]'] = '2'
        data['data[num]'] = '20'
        data['data[start_time]'] = '08:00:00'
        data['data[start_times]'] = '18:00:00'
        data['data[remarks]'] = ''
        try:
            res = self.session.post(url, headers=self.main_page.headers, cookies=self.main_page.cookies, data=data).json()
            print("配置后台返回: ", web_data['updated_domain'], res)
        except Exception as e:
            logging.error(e, exc_info=True)
            self.msg_trigger.emit(f"{web_data['name']} 添加域名配置入后台 连接错误！错误信息: {str(e)}")
        else:
            if res.get('msg') == '成功！':
                msg = f"{web_data['name']} 添加域名配置入后台成功"
                bt_action_logger.info(msg)
                msg = f"{web_data['name']} 任务执行完毕！"
                bt_action_logger.info(msg)
                # self.msg_trigger.emit(f"域名{web_data['name']} 添加域名配置入后台成功")
                return True
            else:
                msg = f"{web_data['name']} 添加域名配置入后台失败"
                bt_action_logger.info(msg)
                # self.msg_trigger.emit(f"域名{web_data['name']} 添加域名配置入后台失败")
                return False

    def get_domain(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    def insert_string(self, direction_string, ori_string):
        if 'R+' in direction_string:
            return ori_string + direction_string.replace("R+", '')
        elif 'L+' in direction_string:
            return direction_string.replace("L+", '') + ori_string
        else:
            return ori_string

    def get_cate_level_cates(self, cate_l, cate_level, random_cate_num_init):
        print(cate_l)
        print(cate_level)
        print(random_cate_num_init)

        print(self.l1)
        print(self.l2)
        print(self.l3)
        l2_ori_len, l3_ori_len = len(self.l2), len(self.l3)
        random_refer_id_l, cate_num = self.get_random_cate_by_comparison([], self.l3, copy.deepcopy(random_cate_num_init))
        random_refer_id_l, cate_num = self.get_random_cate_by_comparison(random_refer_id_l, self.l2, cate_num)
        self.l3 = [item for item in self.l3 if item not in random_refer_id_l]           # 将已用过的栏目更新一遍， random_refer_id_l中为即将被使用的栏目
        self.l2 = [item for item in self.l2 if item not in random_refer_id_l]
        if l2_ori_len != len(self.l2) or l3_ori_len != len(self.l3):
            self.cate_compare_updated_sign = True
        return_l, cate_l = self.get_level_full_cate_info_l(random_refer_id_l, cate_l)
        if cate_num:            # 不为0时
            if cate_num < 2:
                min_random_cate_num = 1
            else:
                min_random_cate_num = 2         # 最低有2个等同于这个level的栏目，如果没有！！ 就算了..
            random_cate_num = random.randint(min_random_cate_num, cate_num)
            temp_l = [ele for ele in cate_l if ele.get('depth') == cate_level]          # 优先获取一定数量等于这个cate level的栏目
            if cate_num > len(temp_l):
                random_cate_num = len(temp_l)           # 防止随机溢出
            return_l += random.sample(temp_l, random_cate_num)
            temp_l_ = [ele for ele in cate_l if ele.get("depth") and int(ele['depth']) <= int(cate_level) and ele not in return_l]
            # temp_l = [ele for ele in cate_l if ele.get('depth') == cate_level]          # 不要动它！！！！！！！！！
            if cate_num > len(temp_l_):
                cate_num = len(temp_l_)
            return_l += random.sample(temp_l_, cate_num - random_cate_num)          # sample防止重复

        return return_l

    def get_level_full_cate_info_l(self, l, cate_l):
        return_l = []
        for cate_info in cate_l[:]:
            if cate_info['linkageid'] in l:
                return_l.append(cate_info)
                cate_l.remove(cate_info)
        return return_l, cate_l

    def get_random_cate_by_comparison(self, random_l, l, random_num):
        if l and random_num:
            if len(l) < random_num:
                random.shuffle(l)
                random_l += l
                random_num -= len(l)
            else:
                random_l += random.sample(l, random_num)
                random_num = 0
        return random_l, random_num

    def get_words(self, type_id, sector_id):
        url = f'{self.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_seoconfig_ke&sectorid={sector_id}&typeid={type_id}'
        words_l = self.session.get(url, headers=self.main_page.headers, cookies=self.main_page.cookies).json()
        return words_l

    def get_keywords(self, sector_id):
        url = f'{self.main_page.domain}/index.php?m=keywords&c=oauth&a=json_seoconfig_ke&sectorid={sector_id}&typeid=&pc_hash={self.main_page.pc_hash}'
        words_l = self.session.get(url, headers=self.main_page.headers, cookies=self.main_page.cookies).json()
        return words_l

    def get_cate(self, sector_id):      # 获取栏目
        job_url = f'{self.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_init'
        job_l = self.session.get(job_url, headers=self.main_page.headers, cookies=self.main_page.cookies).json()
        for item in job_l:
            if item['typeid'] == sector_id:
                url = f'{self.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_submenu&keyid={item["linkageid"]}'
                words_l = self.session.get(url, headers=self.main_page.headers, cookies=self.main_page.cookies).json()
                return words_l

    def set_web_program(self, web_data, root_path):         # path_file为宝塔中 e.g. www/wwwroot/test01.com/ 的目录
        program = self.random_model_refer_d[web_data['name']]
        if program not in self.download_model_l:
            if 'http' in program['style']:
                # status = self.ui.bt_remote_download(program['style'], root_path)            # 加入到下载队列中
                status = self.requests_upload(program['style'], root_path)                   # 直接请求并上传
            else:
                status = self.requests_upload(self.ui.main_page.domain + "/" + program['style'], root_path)                   # 直接上传
            if status:
                self.download_model_l.append(program)
            return status, program
        return True, program

    def backup_export_mysql(self, web_data_list):
        myqsl_file = None
        db_data = self.ui.main_page.bt.get_db_data()
        if self.main_page.bt_patch and db_data.get('status'):
            db_data['data'] = db_data['message']['data']
        found_mysql_sign = False
        for web_data in web_data_list:
            if web_data['sql']:  # 只有开启了SQL的才会进入到这里
                path_name = web_data['path']
                file_name = basename = web_data['name']
                # 找到MYSQL文件 移动到备份文件 -> 数据库 导入备份MYSQL
                if not found_mysql_sign:
                    myqsl_file = self.ui.lookup_mysql_file(path_name)
                    if myqsl_file:  # 如果文件夹下存在mysql文件，导入到备份文件夹中
                        found_mysql_sign = True
                        myqsl_file = myqsl_file
                        file_path = path_name + "/" + myqsl_file  # 组合宝塔中的文件夹位置
                        status = self.ui.copy_mysql_to_backup(file_path, myqsl_file)
                        if not status:
                            found_mysql_sign = False  # 复制失败咯
                # status = self.add_database(file_name)     # 不需要手动再次创建
                if found_mysql_sign:
                    params = {'file': '/www/backup/database/' + myqsl_file,
                              'name': file_name.replace(".", "_")[:16]}  # 只允许16位命名
                    res = self.main_page.bt.import_database(params)
                    print(222222222222, res)
                    if res.get('status'):
                        msg = f"{basename} 恢复数据库成功！"
                        bt_action_logger.info(msg)
                        # self.main_page.return_msg_update(f"{basename} 恢复数据库成功！")
                    else:
                        msg = f"{basename} 恢复数据库失败！！"
                        bt_action_logger.info(msg)
                        # self.main_page.return_msg_update(f"{basename} 恢复数据库失败！")
                    # if extra_web_d.get(web_data['name']):
                self.ui.check_db_username_password_update(file_name, db_data['data'])
                if found_mysql_sign:
                    self.ui.delete_zip_file(path_name + "/" + myqsl_file)  # 如果有解压 则删除该程序内的.sql文件
        if myqsl_file:
            self.ui.delete_zip_file('/www/backup/database/' + myqsl_file)  # 全部完成后删除数据库


class ReadLogRefresh(QThread):
    msg_trigger = pyqtSignal(str)
    def __init__(self):
        super(ReadLogRefresh, self).__init__()
        self.running_sign = True

    def run(self):
        try:
            while self.running_sign:
                with open(f'logs/bt_action_logger/bt_action_logger_{str(datetime.datetime.now().date())}.log', 'r', encoding='utf-8') as f:
                    log_text = f.read()
                    self.msg_trigger.emit(log_text)
                time.sleep(5)
            with open(f'logs/bt_action_logger/bt_action_logger_{str(datetime.datetime.now().date())}.log', 'r', encoding='utf-8') as f:          # 多发一遍 防止没有完全输出出来
                log_text = f.read()
                self.msg_trigger.emit(log_text)
        except Exception as e:
            logging.error(e, exc_info=True)


class ReAttempt(QThread):
    finish_trigger = pyqtSignal(dict)

    def __init__(self, ui, attempt_d):
        super().__init__()
        self.ui = ui
        self.attempt_d = attempt_d
        self.new_attempt_d = {}

    def run(self):
        for k, item in self.attempt_d.items():
            try:
                web_data = item['web_data']
                seo_info_d = item['seo_info_d']
                program = item['program']
                status = True

                if '4' in item['stage_code']:
                    if status:
                        status = self.write_static_rule(web_data, str(program['rewrite']))
                        if not status:
                            self.update_attempt_l(web_data, seo_info_d, program, '4')
                    else:
                        self.update_attempt_l(web_data, seo_info_d, program, '4')

                if '1' in item['stage_code']:
                    if status:
                        status = self.export_seo_setting(web_data)
                        if not status:
                            self.update_attempt_l(web_data, seo_info_d, program, '1')  # 0: 重试上传栏目
                    else:
                        self.update_attempt_l(web_data, seo_info_d, program, '1')

                if '0' in item['stage_code']:
                    if status:
                        status = self.get_local_cate_from_random_cate_list(web_data, seo_info_d['btree_cate_l'])
                        if not status:
                            self.update_attempt_l(web_data, seo_info_d, program, '0')
                    else:
                        self.update_attempt_l(web_data, seo_info_d, program, '0')

                if '2' in item['stage_code']:
                    if status:
                        status = self.update_record_num(web_data)
                        if not status:
                            self.update_attempt_l(web_data, seo_info_d, program, '2')  # 1: 重试上传网站后台设置
                    else:
                        self.update_attempt_l(web_data, seo_info_d, program, '2')

                if '3' in item['stage_code']:
                    if status:
                        status = self.update_local_setting(web_data, program)  # 最后再更新设置
                        if not status:
                            self.update_attempt_l(web_data, seo_info_d, program, '3')  # 2: 重试上传备案号
                    else:
                        self.update_attempt_l(web_data, seo_info_d, program, '3')

            except Exception as e:
                logging.error(e, exc_info=True)
        self.finish_trigger.emit(self.new_attempt_d)

    def update_attempt_l(self, web_data, seo_info_d, program, stage_code):
        if self.new_attempt_d.get(web_data['name']):
            self.new_attempt_d[web_data['name']]['stage_code'] += [stage_code]
        else:
            self.new_attempt_d[web_data['name']] = {'web_data': web_data, 'seo_info_d': seo_info_d,
                                                'program': program, 'stage_code': [stage_code]}  # 0: 上传栏目

    def update_record_num(self, web_data):
        if self.ui.record_no_refer_d.get(web_data['name']):
            token = Token()
            client = token.generateToken('')  # 初始值为空

            client['model'] = 'ICP'
            client['func'] = 'UpdateICP'
            client['icp'] = self.ui.record_no_refer_d[web_data['name']]

            try:
                response = token.sendPostRequestWithToken("http://" + web_data['name'] + "/jiekou.php", client)
            except Exception as e:
                logging.error(e)
                msg = f"重试 - {web_data['name']} 网站备案失败 失败原因: {str(e)}"
                bt_action_logger.info(msg)
                return False
            else:
                if response.get('status'):
                    msg = f"重试 - {web_data['name']} 网站备案设置更新成功"
                    bt_action_logger.info(msg)
                    # self.msg_trigger.emit(f"{web_data['name']} 网站TDK设置成功")
                    return True
                else:
                    msg = f"重试 - {web_data['name']} 网站备案设置更新失败"
                    bt_action_logger.info(msg)
                    # self.msg_trigger.emit(f"{web_data['name']} 网站TDK设置失败")
                    return False
        else:
            msg = f"{web_data['name']} 未检测到该网站备案"
            bt_action_logger.info(msg)
            return True

    def write_static_rule(self, web_data, static_rule_text):
        try:
            path = '/www/server/panel/vhost/rewrite/' + web_data['name'] + '.conf'
            params = {'data': static_rule_text, 'encoding': 'utf-8', 'path': path, 'force': 1}
            res = self.ui.main_page.bt.save_file_body(params)
            if res.get('status'):
                msg = f"{web_data['name']} 上传静态规则成功"
            else:
                msg = f"{web_data['name']} 上传静态规则失败, 失败原因: {str(res['msg'])}"
            bt_action_logger.info(msg)
            return res.get('status')
        except Exception as e:
            logging.error(e, exc_info=True)
        return False

    def export_seo_setting(self, web_data):
        token = Token()
        client = token.generateToken('')    # 初始值为空

        client['model'] = 'site'
        client['name'] = web_data['brand']
        client['domain'] = "http://" + web_data['name'] + "/"
        client['site_title'] = web_data['title']         # 网站名称
        client['keywords'] = ','.join(web_data['keywords'])
        client['description'] = web_data['description']
        client['is_https'] = web_data['is_https']
        client['is_www'] = web_data['is_www']
        try:
            response = token.sendPostRequestWithToken("http://" + web_data['name'] + "/jiekou.php", client)
            if response.get('status'):
                msg = f"重试 - {web_data['name']} 网站TDK设置成功"
                web_data['updated_domain'] = response['msg']['url']
                bt_action_logger.info(msg)
                # self.msg_trigger.emit(f"{web_data['name']} 网站TDK设置成功")
                return True
            else:
                msg = f"重试 - {web_data['name']} 网站TDK设置失败"
                bt_action_logger.info(msg)
                # self.msg_trigger.emit(f"{web_data['name']} 网站TDK设置失败")
                return False
        except Exception as e:
            msg = f"重试 - {web_data['name']} 网站TDK设置失败"
            bt_action_logger.info(msg)
            # self.msg_trigger.emit(f"{web_data['name']} 网站TDK设置失败")
            return False

    def get_local_cate_from_random_cate_list(self, web_data, btree_cate_l):
        return_l = []

        def dfs(node, enter_node=True):
            d = {}
            d['name'] = node['name']
            d['refer_id'] = node['linkageid']
            d['parent'] = [{"name": ele['name'], "refer_id": ele['linkageid']} for ele in node['children']]

            for new_node in node['children']:
                dfs(new_node, enter_node=False)
            if not enter_node and node['children']:
                return_l.append(d)
            elif enter_node:
                return_l.append(d)

        for e in web_data['cate_l']:
            for r in btree_cate_l:
                if e['linkageid'] == r['linkageid']:
                    dfs(r)
        # print("------------------------------------------------------------------------------------------------------------------")
        # print(return_l)
        # print("这是传上去的cate_l: ",return_l)
        # for i in range(10):
        token = Token()
        client = token.generateToken('')    # 初始值为空

        client['model'] = 'category'
        client['batch_add'] = return_l
        try:
            url = "http://" + web_data['name'] + "/jiekou.php"
            # print(client)
            response = token.sendPostRequestWithToken(url, client)
            # print("response = = :", response)
            # print("----------------------------------------------------------------------------------------------------------------")
        except Exception as e:
            logging.error(e)
            msg = f"{web_data['name']} 栏目添加失败, 失败原因: {str(e)}"
            bt_action_logger.info(msg)
            return False
        else:
            if response.get('status'):
                msg = f"{web_data['name']} 栏目添加成功"
                bt_action_logger.info(msg)
                # self.msg_trigger.emit(f"{web_data['name']} 栏目添加成功")
                return True
            else:
                msg = f"{web_data['name']} 栏目添加失败"
                bt_action_logger.info(msg)
                # self.msg_trigger.emit(f"{web_data['name']} 栏目添加失败")
                return False

    def get_local_cate_from_random_cate_list(self, web_data, btree_cate_l):
        return_l = []

        def dfs(node, enter_node=True):
            d = {}
            d['name'] = node['name']
            d['refer_id'] = node['linkageid']
            d['parent'] = [{"name": ele['name'], "refer_id": ele['linkageid']} for ele in node['children']]

            for new_node in node['children']:
                dfs(new_node, enter_node=False)
            if not enter_node and node['children']:
                return_l.append(d)
            elif enter_node:
                return_l.append(d)

        for e in web_data['cate_l']:
            for r in btree_cate_l:
                if e['linkageid'] == r['linkageid']:
                    dfs(r)

        token = Token()
        client = token.generateToken('')    # 初始值为空

        client['model'] = 'category'
        client['batch_add'] = return_l
        response = token.sendPostRequestWithToken("http://" + web_data['name'] + "/jiekou.php", client)
        if response.get('status'):
            msg = f"重试 - {web_data['name']} 栏目添加成功"
            bt_action_logger.info(msg)
            # self.msg_trigger.emit(f"{web_data['name']} 栏目添加成功")
            return True
        else:
            msg = f"重试 - {web_data['name']} 栏目添加失败"
            bt_action_logger.info(msg)
            # self.msg_trigger.emit(f"{web_data['name']} 栏目添加失败")
            return False

    def update_local_setting(self, web_data, program):
        url = f'{self.ui.main_page.domain}/index.php?m=automatic&c=automatic_admin&a=add&json=1'
        data = {}
        data['dis_type'] = '2'
        data['dosubmit'] = ''
        data['pc_hash'] = self.ui.main_page.pc_hash
        data['data[typeid]'] = web_data['sector_id']
        data['data[domain]'] = web_data['updated_domain']
        domain = self.get_domain(web_data['updated_domain'])
        data['data[domain]'] = web_data['updated_domain']
        data['data[token]'] = ''
        if program['types'] == '2':
            if "://www." in web_data['updated_domain']:
                data['data[mobile][]'] = [web_data['updated_domain'].replace("://www.", "://m."), '']
            else:
                data['data[mobile][]'] = [web_data['updated_domain'].replace(domain, 'm.' + domain ), '']
        else:
            data['data[mobile][]'] = []
        data['data[backstage][]'] = [web_data['updated_domain'] + '/myadmin/index.php', 'admin', 'xiaoyu']
        data['data[api]'] = web_data['updated_domain'] + "/jiekou.php"
        data['data[baidu_token]'] = ''
        data['data[baidu_rule]'] = '1'
        data['data[order]'] = '3'
        data['data[release]'] = '2'
        data['data[num]'] = '20'
        data['data[start_time]'] = '08:00:00'
        data['data[start_times]'] = '18:00:00'
        data['data[remarks]'] = ''
        try:
            res = requests.post(url, headers=self.ui.main_page.headers, cookies=self.ui.main_page.cookies, data=data).json()
            print("配置后台返回: ", res)
        except Exception as e:
            logging.error(e, exc_info=True)
            msg = f"{web_data['name']} 添加域名配置入后台 连接错误！错误信息: {str(e)}"
            bt_action_logger.info(msg)
        else:
            if res.get('msg') == '成功！':
                msg = f"{web_data['name']} 添加域名配置入后台成功"
                bt_action_logger.info(msg)
                # self.msg_trigger.emit(f"域名{web_data['name']} 添加域名配置入后台成功")
                return True
            else:
                msg = f"{web_data['name']} 添加域名配置入后台失败"
                bt_action_logger.info(msg)
                # self.msg_trigger.emit(f"域名{web_data['name']} 添加域名配置入后台失败")
                return False

    def get_domain(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc



class GetRandomCateByComparison:
    def __init__(self, main_page):
        self.main_page = main_page
        self.token_api = Token()
        self.redis = RedisDb()
        self.session = requests.session()

    def main(self):
        d = self.redis.handle_redis_token("batch_crate_random_cate_comparison_d")
        if d:
            d = json.loads(d)
            return d['l1'], d['l2'], d['l3']
        else:
            all_cate_articles_count_d = self.get_all_cate_from_sector()         # l1
            refer_id_not_in_linkageid_l, refer_id_not_in_linkageid_with_content_l = self.get_all_cate_from_web(all_cate_articles_count_d)       # l2, l3
            # print("l1: ", list(all_cate_articles_count_d.keys()))
            # print("l2: ", refer_id_not_in_linkageid_l)
            # print("l3: ", refer_id_not_in_linkageid_with_content_l)
            self.redis.handle_redis_token("batch_crate_random_cate_comparison_d", json.dumps({'l1': list(all_cate_articles_count_d.keys()), 'l2': refer_id_not_in_linkageid_l, 'l3': refer_id_not_in_linkageid_with_content_l}))
            return list(all_cate_articles_count_d.keys()), refer_id_not_in_linkageid_l, refer_id_not_in_linkageid_with_content_l

    # def get_random_cate_by_comparison(self, l):
    #     random_l = []
    #     if l and self.random_num:
    #         if len(l) < self.random_num:
    #             random_l += random.shuffle(l)
    #             self.random_num -= len(l)
    #         else:
    #             random_l += random.sample(l, self.random_num)
    #             self.random_num = 0
    #     return random_l

    def get_all_cate_from_sector(self):
        all_cate_articles_count_d = {}
        for i in range(3):
            try:
                url1 = f'{self.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_init'  # 获取行业， 放入comboBox中
                res1 = self.session.get(url1).json()
                for sector_info in res1:
                    # 获取行业下的栏目
                    url4 = f'{self.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_submenu&keyid={sector_info["linkageid"]}'
                    res4 = self.session.get(url4).json()
                    url3 = f'{self.main_page.domain}/index.php?m=automatic&c=oauth&a=json_linkage_web_all'
                    params = {'linkageid': ",".join([ele['linkageid'] for ele in res4])}
                    res3 = self.session.get(url3, params=params).json()
                    all_cate_articles_count_d.update(res3['number'])
            except Exception as e:
                logging.error(e, exc_info=True)
        return all_cate_articles_count_d

    def get_all_cate_from_web(self, all_cate_articles_count_d):
        all_web_cate_l = []
        refer_id_not_in_linkageid_l = []  # l2
        refer_id_not_in_linkageid_with_content_l = []  # l3
        for i in range(3):
            all_web_cate_l = []                 # 需要重试的时候重置一遍
            refer_id_not_in_linkageid_l = []  # l2
            refer_id_not_in_linkageid_with_content_l = []  # l3
            try:
                url2 = f'{self.main_page.domain}/index.php?m=automatic&c=apps&a=time&s=1'        # 获取网站后台
                res2 = self.session.get(url2).json()
                for web_info in res2:           # 测试 3个
                    web_cate_id_refer_l = self.get_single_web_cate(web_info)
                    for ele in web_cate_id_refer_l:
                        if ele['refer_id'] not in all_web_cate_l:
                            all_web_cate_l.append(ele['refer_id'])
                for refer_id, count in all_cate_articles_count_d.items():
                    if refer_id not in all_web_cate_l:
                        if all_cate_articles_count_d.get(refer_id) != '0':
                            refer_id_not_in_linkageid_with_content_l.append(refer_id)
                        else:
                            refer_id_not_in_linkageid_l.append(refer_id)
            except Exception as e:
                logging.error(e, exc_info=True)
        return refer_id_not_in_linkageid_l, refer_id_not_in_linkageid_with_content_l

    def get_single_web_cate(self, current_web_info):
        for i in range(3):
            try:
                client = self.token_api.generateToken(current_web_info['token'])
                client.update({'model': 'content', 'func': 'json'})
                response = self.token_api.sendPostRequestWithToken(current_web_info['api'], client)
                # print(response)
                return [v for k, v in response['url'].items()]
            except Exception as e:
                logging.error(e, exc_info=True)         # 错误了就是接口访问不了
                time.sleep(3)
        return []

