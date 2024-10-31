from PyQt5.QtCore import QThread, pyqtSignal

from frontend.AI_write.AI_write import Ui_Form
from tkinter import filedialog, Tk
from backend.AI_write.qw_model import QWModel, QWCheckKey
from backend.AI_write.chatgpt_model import ChatGptModel, GPTCheckKey
from model.utils import my_logger
import datetime
import time
import os
import re
import requests
from api_requests.RedisAPI import RedisDb
import json
import configparser
import logging


class AIWrite(Ui_Form):
    def __init__(self, page, main_page):
        super().setupUi(page)
        self.page = page
        self.main_page = main_page
        self.cookies = {'DMuxX_admin_email': 'b4f4ugirucYKdvcnd0qdeODMGWVQHlVTfclKrTH_EJRgMHDpz62Pzg', 'DMuxX_admin_username': '9d08TB8Z7IQ3_8n0A34aiWWhbbiQm8wUZBUIW_cH1KRhKQ', 'DMuxX_siteid': '9cedy0zfpq1skQlTFFBLyGpl9ICYB2WP_RBp8Hwa', 'DMuxX_sys_lang': 'e5c0LYDXQneCDCDKb22ektYXwBSHLvjvpZRCslPGP4Pwcg', 'DMuxX_userid': '372bXCdgE7-8p96DBNMoW2NPTDrON7CSrRIW2xvh', 'PHPSESSID': 'ksfpc0fvpq60fpg1jf9s6rr5ck'}
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                        }
        self.gpt_app_key_l = self.get_gpt_app_key_config()
        # self.gpt_app_key_l = [{"id":"1","name":"ChatGPT","agent":"1","key":"","time":"1721295555","items":[{"id":"2","aid":"1","mode":"gpt-3.5-turbo","url":"https:\/\/api.openai.com\/v1\/chat\/completions","frequency":"60","time":"1721287880"},{"id":"3","aid":"1","mode":"gpt-4","url":"https:\/\/api.openai.com\/v1\/chat\/completions","frequency":"5","time":"1721287956"},{"id":"4","aid":"1","mode":"gpt-4o","url":"https:\/\/api.openai.com\/v1\/chat\/completions","frequency":"5","time":"1721287982"},{"id":"5","aid":"1","mode":"gpt-4-turbo","url":"https:\/\/api.openai.com\/v1\/chat\/completions","frequency":"5","time":"1721287999"},{"id":"6","aid":"1","mode":"davinci-002","url":"https:\/\/api.openai.com\/v1\/chat\/completions","frequency":"30","time":"1721288057"}]},{"id":"2","name":"\u901a\u4e49\u5343\u95ee","agent":"0","key":"","time":"1721295560","items":[{"id":"7","aid":"2","mode":"qwen_turbo","url":"#","frequency":"30","time":"1721288147"},{"id":"8","aid":"2","mode":"qwen-turbo","url":"#","frequency":"30","time":"1721288182"},{"id":"9","aid":"2","mode":"qwen-plus","url":"#","frequency":"10","time":"1721288201"},{"id":"10","aid":"2","mode":"qwen-max","url":"#","frequency":"5","time":"1721288213"}]}]
        # self.get_combo_set()
        # self.combo_set = {'GPT-3.5': ['gpt-3.5-turbo', 'davinci-002'], 'GPT-4.0': ["gpt-4", 'gpt-4o', 'gpt-4-turbo'], '通义千问': ["qwen-turbo", "qwen-plus", "qwen-max"], '腾讯混元': []}
        self.job_l = []
        self.cate_l = []
        self.default_start = False
        self.redis = RedisDb()
        self.use_external_api()

        self.get_default_sector()
        # self.connect_slot()

    def get_redis_key_words(self):
        self.online_keywords = self.redis.handle_redis_token(f'{self.main_page.username}_AiKeywords')
        content_config = self.redis.handle_redis_token(f'{self.main_page.username}_AiContentConfig')
        print("redis check", self.online_keywords)
        if self.online_keywords:
            self.textEdit.setText(self.online_keywords)
        if content_config:
            content_config = json.loads(content_config)
            self.textEdit_2.setText(content_config['character_define'])
            self.textEdit_3.setText(content_config['content_sentence'])
            self.textEdit_4.setText(content_config['double_title_sentence'])
            self.lineEdit.setText(str(content_config['words_limit']))
            self.lineEdit_2.setText(content_config['front_sep'])
            self.lineEdit_3.setText(content_config['back_sep'])

    def get_default_sector(self):
        self.t_job = JobThread(self)
        self.t_job.start()
        self.t_job.trigger.connect(self.get_lanmu)

    def get_lanmu(self, job_l):
        self.job_l = job_l
        self.comboBox.addItems(i['name'] for i in job_l)
        combo_index = self.comboBox.currentIndex()
        if combo_index >= 0:
            parent_id_l = [ele['linkageid'] for ele in self.job_l[combo_index]['upper_cate_info']]
            self.t_lanmu = LanmuThread(self, parent_id_l)
            self.t_lanmu.start()
            self.t_lanmu.trigger.connect(self.add_lanmu)
        self.get_redis_key_words()

        self.connect_slot()

    def add_lanmu(self, cate_l):
        self.cate_l = cate_l
        self.comboBox_2.clear()
        self.comboBox_2.addItems([ele['linkageid'] + ele['name'] for ele in self.cate_l])

    def refresh_lanmu(self):
        combo_index = self.comboBox.currentIndex()
        if combo_index >= 0:
            parent_id_l = [ele['linkageid'] for ele in self.job_l[combo_index]['upper_cate_info']]
            self.t_lanmu = LanmuThread(self, parent_id_l)
            self.t_lanmu.start()
            self.t_lanmu.trigger.connect(self.add_lanmu)

    def get_combo_set(self):
        self.combo_set = {}
        self.api_refer_d = {}           # 频率, url等
        for GPT_l in self.gpt_app_key_l:
            self.combo_set[GPT_l['name']] = [i['mode'] for i in GPT_l['items']]
            self.api_refer_d[GPT_l['name']] = {}
            for model in GPT_l['items']:
                d = {}
                d[model['mode']] = {}
                d[model['mode']]['frequency'] = model['frequency']
                d[model['mode']]['url'] = model['url']
                d[model['mode']]['key'] = GPT_l['key']
                d[model['mode']]['agent'] = GPT_l['agent']
                self.api_refer_d[GPT_l['name']].update(d)

    def start_task(self):
        if not self.default_start:      # 如果还没开始, 就变为已开始状态
            run_sign, request_config, keywords, content_config, keys = self.get_config()
            if run_sign:
                keywords = sorted(keywords, key=len, reverse=True)
                self.online_keywords = "\n".join(keywords)
                self.redis.handle_redis_token(f'{self.main_page.username}_AiKeywords', self.online_keywords)     # 更新并存入redis
                self.redis.handle_redis_token(f'{self.main_page.username}_AiContentConfig', json.dumps(content_config))

                if self.comboBox_3.currentText() == '通义千问':
                    gpt = self.comboBox_3.currentText()
                    model = self.comboBox_4.currentText()       # 模型选择
                    self.main_page.return_msg_update(f"正在使用 {gpt} {model} AI模型...")
                elif self.comboBox_3.currentText() == 'ChatGPT':
                    gpt = self.comboBox_3.currentText()
                    model = self.comboBox_4.currentText()       # 模型选择
                    self.main_page.return_msg_update(f"正在使用 {gpt} {model} AI模型...")

                print(f"共有{len(keywords)}个关键词")
                self.ai_write_t = ModelThread(self, self.api_refer_d, request_config, keywords, content_config, keys, model, gpt)
                self.ai_write_t.start()
                self.ai_write_t.msg_trigger.connect(self.return_ai_write_msg)
                self.ai_write_t.output_trigger.connect(self.return_ai_write_output)
                self.ai_write_t.finished_trigger.connect(self.return_ai_write_finished)

                self.pushButton_6.setText("终止任务")
                self.pushButton_6.setEnabled(False)
                self.default_start = True
                self.t_button_reset = ButtonReset()
                self.t_button_reset.start()
                self.t_button_reset.trigger.connect(self.return_button_reset)
        else:
            # trying to stop model
            self.default_start = False
            self.ai_write_t.stop_threading()
            self.pushButton_6.setText("开始任务")

    def return_button_reset(self):
        # self.pushButton_6.setText("终止任务")
        # self.default_start = True
        self.pushButton_6.setEnabled(True)

    def check_key_valid(self):
        if self.comboBox_3.currentText() == '通义千问':
            gpt = '通义千问'
            model = self.comboBox_4.currentText()  # 模型选择
        elif self.comboBox_3.currentText() == 'ChatGPT':
            gpt = 'ChatGPT'
            model = self.comboBox_4.currentText()       # 模型选择

        self.t_check_key = CheckKeyThread(self.api_refer_d, gpt, model)
        self.t_check_key.start()
        self.t_check_key.msg_trigger.connect(self.return_check_key_valid)
        self.t_check_key.finished_trigger.connect(self.return_check_key_valid_finished)

    def return_check_key_valid(self, msg):
        self.main_page.return_msg_update(msg)

    def return_check_key_valid_finished(self):
        self.main_page.return_msg_update(f"全部Key已校验完毕")

    def return_ai_write_msg(self, msg, word, title):
        if '错误信息' in msg:
            my_logger.info(msg)
            self.main_page.return_msg_update(str(msg))
        else:
            self.main_page.return_msg_update(str(msg))           # 仅成功的词会被去掉

            self.online_keywords = self.online_keywords.replace(word, '')
            self.online_keywords = self.online_keywords.strip()
            if self.online_keywords:
                self.redis.handle_redis_token(f"{self.main_page.username}_AiKeywords", self.online_keywords, expire=60*60*24)          # 更新
            else:
                self.redis.delete_key(f"{self.main_page.username}_AiKeywords")                                                              # 更新
            current_text = self.textEdit.toPlainText().strip()
            if word.strip() in current_text:
                if word.strip() == current_text:
                    self.textEdit.clear()
                else:
                    new_text = current_text.split("\n")
                    if word in new_text:
                        new_text.remove(word)
                    self.textEdit.setText("\n".join(new_text))

    def return_ai_write_finished(self):
        self.pushButton_6.setText("开始任务")
        self.pushButton_6.setEnabled(True)
        self.default_start = False
        self.online_keywords = ''
        self.redis.handle_redis_token(f"{self.main_page.username}_AiKeywords", self.online_keywords,
                                      expire=60 * 60 * 24)  # 更新

    def return_ai_write_output(self, word, content):
        self.create_dir()
        if "新标题:" in word:
            title = word.split("新标题:")[-1].strip()
        elif "新标题:" in word:
            title = word.split("新标题:")[-1].strip()
        else:
            title = word
        title = re.sub(r'[|\-、:/\\?*^<>\n]', '', title)

        print("导出时的title: ", title.strip())
        sector = self.comboBox.currentText()
        cate = self.comboBox_2.currentText()

        if not os.path.exists(f'articles/{sector}'):
            try:
                os.mkdir(f'articles/{sector}')
            except Exception as e:
                pass
        if not os.path.exists(f'articles/{sector}/{cate}'):
            try:
                os.mkdir(f'articles/{sector}/{cate}')
            except Exception as e:
                pass
        try:
            with open(f"articles/{sector}/{cate}/{title.strip()}.txt", 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            self.main_page.return_msg_update(f"文章: {title.strip()} 录入失败！错误信息: {str(e)}")


    def create_dir(self):
        try:
            File_Path = "articles"
            # 判断是否已经存在该目录
            if not os.path.exists(File_Path):
                # 目录不存在，进行创建操作
                os.makedirs(File_Path)  # 使用os.makedirs()方法创建多层目录
        except BaseException as msg:
            print("新建目录失败：" + msg)

    def get_config(self, simple=False):
        run_sign = True
        try:
            timeout = int(self.lineEdit_8.text())       # 超时
            threads = int(self.lineEdit_9.text())       # 线程
            attempt = int(self.lineEdit_10.text())       # 重试
            remove_p_label = self.checkBox_10.isChecked()        # 去p标签
            ban_word = self.checkBox_11.isChecked()              # 违禁词处理
            fail_attempt = self.checkBox_12.isChecked()          # 失败自动重试
            running_choices = self.comboBox_5.currentIndex()    # 文章/ 双标题/ 三标题
            redirect_api = self.lineEdit_4.text()               # 跳板api请求
            use_external_api = self.checkBox_3.isChecked()      # 使用外部接口
        except Exception as e:
            self.main_page.return_msg_update("输入格式不规范，请检查")
            run_sign = False
            request_config = {}
        else:
            request_config = {'timeout': timeout, 'threads': threads, 'attempt': attempt, 'remove_p_label': remove_p_label, 'ban_word': ban_word,
                              'fail_attempt': fail_attempt, 'running_choices': running_choices, 'redirect_api': redirect_api, 'use_external_api': use_external_api}

        try:
            keyword_str = self.textEdit.toPlainText().strip()
            if keyword_str:
                keywords = list(set(keyword_str.split()))
            else:
                keywords = []
            external_keys = list(set(self.textEdit_10.toPlainText().strip().split("\n")))
        except Exception as e:
            logging.error(e, exc_info=True)
            self.main_page.return_msg_update("请确认关键词无误")
            keywords = []
            external_keys = []
            run_sign = False
        else:
            if not keywords:
                run_sign = False
                self.main_page.return_msg_update("关键词为空")
            if use_external_api and not external_keys:
                run_sign = False
                self.main_page.return_msg_update("在使用外部接口时, keys不可为空")
        content_config = {}         # 如语料、角色化等  暂不参与判断
        if not self.checkBox_5.isChecked():
            character_define = self.textEdit_2.toPlainText()
            content_sentence = self.textEdit_3.toPlainText()
            title_sentence = self.textEdit_4.toPlainText()

            title_custom = True
            content_custom = True

            words_limit = int(self.lineEdit.text())
            front_sep = self.lineEdit_2.text()
            back_sep = self.lineEdit_3.text()

            content_config['character_define'] = character_define
            content_config['double_title_sentence'] = title_sentence
            content_config['triple_title_sentence'] = title_sentence
            content_config['content_sentence'] = content_sentence
            content_config['title_custom'] = title_custom
            content_config['content_custom'] = content_custom
            content_config['words_limit'] = words_limit
            content_config['front_sep'] = front_sep
            content_config['back_sep'] = back_sep

            # if "{标题}" not in content_sentence or "{标题}" not in title_sentence:
            if "{标题}" not in content_sentence:
                run_sign = False
                self.main_page.return_msg_update("请确认语料中包含 {标题}")

        # if request_config and keywords:     # 还有keys
        #     # do something
        return run_sign, request_config, keywords, content_config, external_keys

    def get_gpt_app_key_config(self):
        self.t_app_key_config = GetAppKeyConfigThread(self)
        self.t_app_key_config.start()
        self.t_app_key_config.msg_trigger.connect(self.return_msg)
        self.t_app_key_config.finished_trigger.connect(self.finish_gpt_app_key_config)

    def finish_gpt_app_key_config(self, config_l):
        self.gpt_app_key_l = config_l
        print(3333, self.gpt_app_key_l)
        self.get_combo_set()
        self.default_chatai_box_setting()       # 设置默认的CHAT AI

    def return_msg(self, msg):
        self.main_page.return_msg_update(str(msg))

    def chatai_box_change(self):
        self.comboBox_4.clear()
        self.comboBox_4.addItems(self.combo_set[self.comboBox_3.currentText()])

        # if self.comboBox_3.currentText() == '通义千问':
        #     self.lineEdit_4.clear()
        #     self.lineEdit_8.setEnabled(False)
        #     self.lineEdit_9.setEnabled(False)
        #     self.lineEdit_4.setEnabled(False)
        # elif self.comboBox_3.currentText() == 'GPT-3.5' or self.comboBox_3.currentText() == 'GPT-4.0':
        #     self.lineEdit_4.setEnabled(True)
        #     self.lineEdit_8.setEnabled(True)
        #     self.lineEdit_9.setEnabled(True)
        # else:
        #     self.lineEdit_4.clear()
        #     self.lineEdit_4.setEnabled(False)
        #     self.lineEdit_8.setEnabled(True)
        #     self.lineEdit_9.setEnabled(True)

    def default_chatai_box_setting(self):
        self.comboBox_3.addItems([ele for ele in self.combo_set.keys()])
        self.comboBox_4.addItems(self.combo_set[self.comboBox_3.currentText()])

    def open_article_folder(self):
        self.create_dir()           # 如果没有这个路径就先创建

        path = os.path.abspath("articles")
        os.startfile(path)

    def connect_slot(self):
        # self.pushButton.clicked.connect(self.open_article_folder)
        self.comboBox.currentIndexChanged.connect(self.refresh_lanmu)
        self.comboBox_3.currentIndexChanged.connect(self.chatai_box_change)           # 接触通义千问无法多线程的限制
        self.pushButton_4.clicked.connect(self.check_key_valid)
        self.pushButton_5.clicked.connect(self.open_article_folder)
        self.pushButton_6.clicked.connect(self.start_task)
        self.pushButton_7.clicked.connect(self.keyword_import)
        self.checkBox_3.toggled.connect(self.use_external_api)
        self.textEdit.textChanged.connect(self.text_edit_changed)

    def text_edit_changed(self):
        lines = self.textEdit.toPlainText().strip().split("\n")
        for line in lines[:]:
            if not line.strip():
                lines.remove(line)
        self.label_6.setText(f"共有{len(lines)}个关键词")

    def get_current_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def keyword_import(self):
        root = Tk()
        root.withdraw()  # 隐藏主窗口，因为不需要显示整个窗口，只显示文件选择对话框
        folder_selected = filedialog.askopenfilename()
        if folder_selected:
            with open(folder_selected, 'r', encoding='utf-8') as f:
                content = f.read()
            self.textEdit.append(content)

    def use_external_api(self):
        if not self.checkBox_3.isChecked():
            self.label_16.hide()
            self.label_20.hide()
            self.label_21.hide()
            self.lineEdit_4.hide()
            self.textEdit_10.hide()
            self.pushButton_4.hide()

            self.label_15.show()
            self.comboBox_3.show()
            self.comboBox_4.show()
            self.pushButton_4.show()
        else:
            self.label_16.show()
            self.label_20.show()
            self.label_21.show()
            self.lineEdit_4.show()
            self.textEdit_10.show()
            self.pushButton_4.show()

            self.label_15.hide()
            self.comboBox_3.hide()
            self.comboBox_4.hide()
            self.pushButton_4.hide()


class ModelThread(QThread):
    msg_trigger = pyqtSignal(str, str, str)
    output_trigger = pyqtSignal(str, str)
    finished_trigger = pyqtSignal()

    def __init__(self, ui, api_refer_d, request_config, keywords, content_config, keys, model, gpt):
        super().__init__()
        self.ui = ui
        self.api_refer_d = api_refer_d
        self.request_config = request_config
        self.keywords = keywords
        self.content_config = content_config
        self.keys = keys
        self.model = model
        self.gpt = gpt

    def run(self):
        # print(33333, self.api_refer_d)
        model_l = self.api_refer_d[self.gpt]
        # print(666666666666666666, model_l)
        # l = model_l[self.model]['key'].split("\n")
        # print(l)
        # self.finished_trigger.emit()
        # return
        # if [model_l[ele]['agent'] for ele in model_l][0] == '1':
        #     status, proxy_type, proxy = self.read_proxy()
        # else:
        #     status, proxy_type, proxy = False, None, None
        if self.gpt == '通义千问':
            if [model_l[ele]['agent'] for ele in model_l][0] == '1':
                status, proxy_type, proxy = self.read_proxy()
                if status:
                    self.qw_model = QWModel(self.ui, model_l, self.msg_trigger, self.output_trigger, self.request_config, self.content_config, self.keywords, self.keys, self.model, proxy_type, proxy)
                    self.qw_model.main()
                else:
                    self.ui.default_start = False
                    self.msg_trigger.emit("未检测到VPN设置, 请先前往代理设置", "", "")
            else:
                self.qw_model = QWModel(self.ui, model_l, self.msg_trigger, self.output_trigger, self.request_config,
                                        self.content_config, self.keywords, self.keys, self.model)
                self.qw_model.main()
        elif self.gpt == 'ChatGPT':

            if [model_l[ele]['agent'] for ele in model_l][0]:
                status, proxy_type, proxy = self.read_proxy()
                if status:
                    self.chatgpt_model = ChatGptModel(self.ui, model_l, self.msg_trigger, self.output_trigger, self.request_config, self.content_config, self.keywords, self.keys, self.model, proxy_type, proxy)
                    self.chatgpt_model.main()
                else:
                    self.ui.default_start = False
                    self.msg_trigger.emit("未检测到VPN设置, 请先前往代理设置", "", "")
            else:
                self.chatgpt_model = ChatGptModel(self.ui, model_l, self.msg_trigger, self.output_trigger,
                                                  self.request_config, self.content_config, self.keywords, self.keys,
                                                  self.model)
                self.chatgpt_model.main()

        self.finished_trigger.emit()

    def stop_threading(self):
        if self.gpt == '通义千问':
            self.qw_model.running_sign = False
        elif self.gpt == 'ChatGPT':
            self.chatgpt_model.running_sign = False

    def read_proxy(self):
        config = configparser.ConfigParser()
        try:
            config.read('config/config.ini')  # 读取 config.ini 文件
            if config.has_section('Proxy'):
                proxy_type = config.get('Proxy', 'type')
                host = config.get('Proxy', 'host')
                port = config.get('Proxy', 'port')
                username = config.get('Proxy', 'username')
                password = config.get('Proxy', 'password')
                if proxy_type == 'http':
                    if username and password:
                        proxies = {
                            "http": f"http://{username}:{password}@{host}:{port}",
                            "https": f"http://{username}:{password}@{host}:{port}",
                        }
                    else:
                        proxies = {
                            "http": f"http://{host}:{port}",
                            "https": f"http://{host}:{port}",
                        }
                    return True, 'http', proxies
                elif proxy_type == 'socks':
                    if username and password:
                        proxies = {
                            "http": f"socks5://{username}:{password}@{host}:{port}",
                            "https": f"socks5://{username}:{password}@{host}:{port}",
                        }
                    else:
                        proxies = {
                            "http": f"socks5://{host}:{port}",
                            "https": f"socks5://{host}:{port}",
                        }
                    return True, 'socks', proxies
                else:
                    return False, '', None
            else:
                return False, '', None
        except Exception as e:
            logging.error(e, exc_info=True)
            return False, '', None


class CheckKeyThread(QThread):
    msg_trigger = pyqtSignal(str)
    finished_trigger = pyqtSignal()

    def __init__(self, api_refer_d, gpt, model):
        super().__init__()
        self.api_refer_d = api_refer_d
        self.gpt = gpt
        self.model = model

    def run(self):
        model_l = self.api_refer_d[self.gpt]
        if self.gpt == '通义千问':
            if [model_l[ele]['agent'] for ele in model_l][0]:
                status, proxy_type, proxy = self.read_proxy()
                if status:
                    QWCheckKey(model_l, self.gpt, self.model, self.msg_trigger, proxy_type, proxy).main()
                else:
                    self.msg_trigger.emit("未检测到VPN设置, 请先前往代理设置")
            else:
                QWCheckKey(model_l, self.gpt, self.model, self.msg_trigger).main()
        elif self.gpt == 'ChatGPT':
            if [model_l[ele]['agent'] for ele in model_l][0]:
                status, proxy_type, proxy = self.read_proxy()
                if status:
                    GPTCheckKey(model_l, self.gpt, self.model, self.msg_trigger, proxy_type, proxy).main()
                else:
                    self.msg_trigger.emit("未检测到VPN设置, 请先前往代理设置")
            else:
                QWCheckKey(model_l, self.gpt, self.model, self.msg_trigger).main()
        self.finished_trigger.emit()

    def read_proxy(self):
        config = configparser.ConfigParser()
        try:
            config.read('config/config.ini')  # 读取 config.ini 文件
            if config.has_section('Proxy'):
                proxy_type = config.get('Proxy', 'type')
                host = config.get('Proxy', 'host')
                port = config.get('Proxy', 'port')
                username = config.get('Proxy', 'username')
                password = config.get('Proxy', 'password')
                if proxy_type == 'http':
                    if username and password:
                        proxies = {
                            "http": f"http://{username}:{password}@{host}:{port}",
                            "https": f"http://{username}:{password}@{host}:{port}",
                        }
                    else:
                        proxies = {
                            "http": f"http://{host}:{port}",
                            "https": f"http://{host}:{port}",
                        }
                    return True, 'http', proxies
                elif proxy_type == 'socks':
                    if username and password:
                        proxies = {
                            "http": f"socks5://{username}:{password}@{host}:{port}",
                            "https": f"socks5://{username}:{password}@{host}:{port}",
                        }
                    else:
                        proxies = {
                            "http": f"socks5://{host}:{port}",
                            "https": f"socks5://{host}:{port}",
                        }
                    return True, 'socks', proxies
                else:
                    return False, '', None
            else:
                return False, '', None
        except Exception as e:
            print(str(e))
            return False, '', None


class GetAppKeyConfigThread(QThread):
    msg_trigger = pyqtSignal(str)
    finished_trigger = pyqtSignal(list)
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        try:
            url = f'{self.ui.main_page.domain}/index.php?m=ai&c=oauth&a=json_init'
            config_l = requests.get(url, headers=self.ui.headers, cookies=self.ui.cookies).json()
        except Exception as e:
            print(e)
            my_logger.error(e)
            self.msg_trigger.emit("无法连接至服务器")
            config_l = []
        finally:
            self.finished_trigger.emit(config_l)


class JobThread(QThread):
    msg_trigger = pyqtSignal(str)
    trigger = pyqtSignal(list)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        try:
            url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_type&mode=sector'       # 获取行业， 放入comboBox中
            upper_cate_url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_init'

            job_l = requests.get(url, headers=self.ui.headers, cookies=self.ui.cookies, timeout=5).json()
            upper_cate_l = requests.get(upper_cate_url, headers=self.ui.headers, cookies=self.ui.cookies, timeout=5).json()

            for ele in job_l:
                ele['upper_cate_info'] = []
                for item in upper_cate_l:
                    if ele['typeid'] == item['typeid']:
                        ele['upper_cate_info'].append(item)

        except Exception as e:
            my_logger.error(e)
            print("无法连接至服务器！")
            self.msg_trigger.emit("无法连接至服务器！")
            job_l = []
        finally:
            self.trigger.emit(job_l)


class LanmuThread(QThread):
    trigger = pyqtSignal(list)

    def __init__(self, ui, parent_id_l):
        super().__init__()
        self.ui = ui
        self.parent_id_l = parent_id_l

    def run(self):
        cate_l = []
        try:
            for parent_id in self.parent_id_l:
                url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_submenu&keyid={parent_id}'
                s_cate_l = requests.get(url, headers=self.ui.headers, cookies=self.ui.cookies, timeout=5).json()
                print(1111111111, s_cate_l)

                cate_l += [ele for ele in s_cate_l if ele['linkageid'] == ele['arrchildid']]
            self.trigger.emit(cate_l)
        except Exception as e:
            my_logger.error(e)
            print("无法连接至服务器！")


class ButtonReset(QThread):
    trigger = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        time.sleep(2)
        self.trigger.emit()

