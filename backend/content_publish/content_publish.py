import time

from frontend.content_publish.content_publish import Ui_Form
import requests
from backend.content_publish.set_table import SetTable
from tkinter import filedialog, Tk
from backend.content_publish.table_insertion import TableInsertion
import os
from model.utils import content_publish_logger as my_logger
import random
import re
import jieba as jb
import jieba.analyse as analyse
import datetime
from PyQt5.QtCore import *
from api_requests.TokenAPI import Token
from collections import OrderedDict
from api_requests.RedisAPI import RedisDb
import json
from backend.content_publish.article_count.article_count import ArticleCount
from backend.content_publish.article_storage.article_storage import ArticleStorage
import logging
from backend.content_publish.article_await.article_await import ArticleAwait
import base64
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox"


class ContentPublish(Ui_Form):
    def __init__(self, page, main_page):
        super().setupUi(page)
        self.page = page
        self.main_page = main_page
        self.cookies = main_page.cookies
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                        }
        self.session = requests.session()
        self.redis = RedisDb()
        self.token_api = Token()
        self.set_default_value()
        # self.page = WebEnginePage()
        # self.webEngineView.setPage(self.page)
        # self.page.load(QUrl("https://www.yahoo.com"))

        self.article_count_ui = None
        self.export_running = False
        # print("除了main全初始化了")
        self.main()

    def set_default_value(self):
        self.auto_publish_list = []
        self.sep_words_d = {}
        self.cate_l = []
        self.web_l = []
        self.image_path_d = {}
        self.lanum_d_under_web = []
        self.job_l = []

        self.label_4.hide()
        self.label_12.hide()

        self.comboBox_2.hide()
        self.comboBox_7.hide()

        self.label_3.show()
        self.comboBox.show()
        # print("正在清理缓存")
        #
        # # # 获取默认的web引擎配置文件
        # # profile = QWebEngineProfile.defaultProfile()
        # # # print(profile.cachePath())
        # # # 清除缓存
        # # profile.clearHttpCache()
        # # profile.clearAllVisitedLinks()
        # # profile.cookieStore().deleteAllCookies()
        #
        # print("清理完毕")

    def main(self):
        self.t_job_thread = JobThread(self)
        self.t_job_thread.start()
        self.t_job_thread.msg_trigger.connect(self.return_msg_trigger)
        self.t_job_thread.finish_trigger.connect(self.return_finish_trigger)

        self.t_get_redis_info = InitRedisThread(self)
        self.t_get_redis_info.start()
        self.t_get_redis_info.finish_trigger.connect(self.return_redis_finish_trigger)

    def return_msg_trigger(self, msg):
        self.main_page.return_msg_update(str(msg))

    def get_current_datetime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def return_finish_trigger(self, job_l, auto_publish_list):
        self.job_l = job_l
        self.comboBox_5.addItems([ele['name'] for ele in self.job_l])
        self.auto_publish_list = auto_publish_list
        self.connect_slot()

    def return_redis_finish_trigger(self, content_publish_config):
        if content_publish_config:
            self.lineEdit.setText(content_publish_config['article_path'])
            self.lineEdit_2.setText(content_publish_config['images_path'])
            self.lineEdit_3.setText(str(content_publish_config['images_num']))
            self.lineEdit_4.setText(str(content_publish_config['cut_sentence_num']))
            self.lineEdit_5.setText(str(content_publish_config['thumb_image_num']))
            self.checkBox_2.setChecked(True) if content_publish_config['cut_sentence'] else self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(True) if content_publish_config['thumb_image_sign'] else self.checkBox_3.setChecked(False)

    def gain_cate_and_cate_web(self):
        # 获取栏目以及
        try:
            self.comboBox.clear()               # 以下这部分是获取行业的栏目
            combo_index = self.comboBox_5.currentIndex()
            if combo_index >= 0:
                parent_id = self.job_l[combo_index]['linkageid']
                self.t_lanmu_thread = GainLanmu(self, parent_id)
                self.t_lanmu_thread.start()
                self.t_lanmu_thread.msg_trigger.connect(self.return_msg_trigger)
                self.t_lanmu_thread.finish_trigger.connect(self.lanmu_finished_trigger)
            # else:
            self.web_l = []
            self.comboBox_2.clear()
            combo_index = self.comboBox_5.currentIndex()
            if combo_index >= 0:
                type_id = self.job_l[combo_index]['typeid']
                # for i in self.auto_publish_list:
                #     if i['typeid'] == type_id:
                #         self.web_l.append(i)
                self.web_l = [ele for ele in self.auto_publish_list if ele['typeid'] == type_id]
                self.comboBox_2.addItems(['全部'] + [i['web'] for i in self.web_l])
            if not self.article_count_ui:
                self.article_count_ui = ArticleCount(self.tab, self)
                self.article_storage_ui = ArticleStorage(self.tab_2, self)
                self.article_await_ui = ArticleAwait(self.tab_3, self)
        except Exception as e:
            logging.error(e, exc_info=True)

    def lanmu_finished_trigger(self, l):
        self.cate_l = self.list_shorten(l)
        self.comboBox.addItems([i['linkageid'] + i['name'] for i in self.cate_l])
        # self.comboBox_3.addItems([i['name'] for i in self.cate_l])
        self.article_count_ui.get_cate_article_left()

    def list_shorten(self, l):     # 行业list瘦身
        for i in l[:]:
            if i['parentid'] == '0' and i['arrchildid'] != i['linkageid']:
                l.remove(i)
        return l

    def open_file(self):
        self.create_dir()
        root = Tk()
        root.withdraw()  # 隐藏主窗口，因为不需要显示整个窗口，只显示文件选择对话框
        folder_selected = filedialog.askdirectory(initialdir='articles')
        if folder_selected:
            self.lineEdit.setText(folder_selected)

    def open_image_file(self):
        self.create_dir('images')
        root = Tk()
        root.withdraw()  # 隐藏主窗口，因为不需要显示整个窗口，只显示文件选择对话框
        file_path = filedialog.askdirectory(initialdir='images')  # 用户选择文件后，文件路径会被存储在file_path变量中
        if file_path:  # 如果用户选择了文件
            self.lineEdit_2.setText(file_path)

    def create_dir(self, path='articles'):
        try:
            File_Path = os.getcwd() + "\\" + path
            # 判断是否已经存在该目录
            if not os.path.exists(File_Path):
                # 目录不存在，进行创建操作
                os.makedirs(File_Path)  # 使用os.makedirs()方法创建多层目录
        except BaseException as msg:
            print("新建目录失败：" + msg)

    def export(self):
        # self.export_running = False
        # print(self.lanum_d_under_web[self.comboBox_7.currentIndex()])
        # print(self.cate_l[self.comboBox.currentIndex()])
        # return

        if self.export_running:
            self.export_running = False
            self.pushButton_2.setEnabled(False)
            return
        else:
            if not self.checkBox.isChecked():       # 禁用图片库
                try:
                    image_num = int(self.lineEdit_3.text())
                except Exception as e:
                    self.main_page.return_msg_update("数字格式错误，请检查")
                    return
            else:
                image_num = 0
            try:
                image_folder_path = self.lineEdit_2.text()
                if int(image_num) != 0:
                    if image_folder_path:
                        if os.path.exists(image_folder_path):
                            files_in_folder = self.get_all_files(image_folder_path, ['jpg', 'jpeg', 'jpg', 'gif', 'png'])
                            if len(files_in_folder) < image_num:
                                self.main_page.return_msg_update("图片库中图片数量少于设置的图片数量，请确认")
                                return
                        else:
                            self.main_page.return_msg_update("图片路径错误")
                            return
                    else:
                        self.main_page.return_msg_update("无图片路径")
                        return
                else:
                    files_in_folder = []
            except Exception as e:
                self.main_page.return_msg_update("图片路径错误")
                return

            try:
                article_path = self.lineEdit.text()
                if article_path:
                    if os.path.exists(self.lineEdit.text()):
                        txt_files = self.get_all_files(article_path, ['txt'])
                else:
                    self.main_page.return_msg_update("无文章路径！")
                    return
            except Exception as e:
                self.main_page.return_msg_update("文章路径错误")
                return

            if self.checkBox_2.isChecked():     # 截取摘要
                cut_sentence = 1
                try:
                    cut_sentence_num = int(self.lineEdit_4.text())
                except Exception as e:
                    self.main_page.return_msg_update("数字格式错误，请检查")
                    return
            else:
                cut_sentence = 0
                cut_sentence_num = 0

            if self.checkBox_3.isChecked():
                auto_show_image = 1
                try:
                    show_image_num = int(self.lineEdit_5.text())
                    if not self.checkBox.isChecked():
                        if show_image_num > image_num:
                            self.main_page.return_msg_update("缩略图选择数不可超过总图片数量")
                            return
                    else:
                        show_image_num = 1
                except Exception as e:
                    self.main_page.return_msg_update("数字格式错误，请检查")
                    return
            else:
                auto_show_image = 0
                show_image_num = 0

            if self.cate_l:
                cate_choice = {'linkageid': -1}
                web_choice = -1
                web_cate_choice = -1
                if not self.comboBox_6.currentIndex():      # 如果是选择的是栏目导入
                    if self.comboBox.currentIndex() >= 0:
                        cate_choice = self.cate_l[self.comboBox.currentIndex()]
                        if self.comboBox.currentText() not in [ele['name'] for ele in self.cate_l]:
                            self.comboBox.setCurrentText(cate_choice['name'])
                    else:
                        self.main_page.return_msg_update("无可用栏目！")
                        return
                else:
                    if self.comboBox_2.currentIndex() >= 0:
                        web_choice = self.web_l[self.comboBox_2.currentIndex()]['id']
                        if self.comboBox_7.currentIndex() >= 0:
                            web_cate_choice = self.lanum_d_under_web[self.comboBox_7.currentIndex()]['catid']
                        else:
                            if self.comboBox_6.currentIndex() == 1:         # 如果是栏目发布, 无影响 如果是站点发布，必须选择
                                self.main_page.return_msg_update("域名栏目不可为空！")
                                return
                    else:
                        self.main_page.return_msg_update("无可用域名！")
                        return
            else:
                self.main_page.return_msg_update("请先获取 文章库内容发布 - 行业栏目与域名！")
                return

            redis_d = {'article_path': article_path, 'images_path': image_folder_path, 'images_num': image_num,
                       'thumb_image_num': show_image_num, 'thumb_image_sign': auto_show_image,
                       'cut_sentence': cut_sentence, 'cut_sentence_num': cut_sentence_num,}
            self.redis.handle_redis_token(f'{self.main_page.username}_ContentPublishConfig', json.dumps(redis_d))
            data = {'inputtime': int(time.time()),
                    'updatetime': int(time.time()),
                    'catid': self.comboBox_6.currentIndex() + 1,
                    'username': self.main_page.username,
                    'linkageid': cate_choice['linkageid'],
                    'web_or_cate': self.comboBox_6.currentIndex(),
                    'web': web_choice,
                    'web_cateid': web_cate_choice,
                    'add_introduce': cut_sentence,
                    'introduce_length': cut_sentence_num,
                    'auto_thumb': auto_show_image,
                    'auto_thumb_no': show_image_num,
                    'sector_name': self.comboBox_5.currentText(),
                    'cate_name': self.comboBox.currentText(),
                    'web_cate_name': self.comboBox_7.currentText(),
                    'article_folder_path': article_path,
                    }
            # 开始正式导出到文章库中 by QThread'
            self.pushButton_2.setText("终止导入")
            self.export_running = True
            self.main_page.return_msg_update("上传开始...")
            self.t_export = ExportToBase(self, data, txt_files, files_in_folder, image_num)
            self.t_export.start()
            self.t_export.msg_trigger.connect(self.return_msg_trigger)
            self.t_export.move_file_trigger.connect(self.return_move_file_trigger)
            self.t_export.finish_trigger.connect(self.return_finish_export)

    def return_finish_export(self):
        self.export_running = False
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setText("导入到文章库")
        self.main_page.return_msg_update("上传结束")

    def return_move_file_trigger(self, file_info):
        txt_path = file_info['article_path']
        article_folder_path = file_info['article_folder_path']
        self.move_file(txt_path, article_folder_path + "/已上传")

    def move_file(self, source_path, destination_path):
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        try:
            file_name = os.path.basename(source_path)
            destination_file_path = os.path.join(destination_path, file_name)
            os.rename(source_path, destination_file_path)
            self.main_page.return_msg_update("文件已成功移动到目标文件夹！")
        except FileExistsError:
            self.main_page.return_msg_update("文件夹中已存在同名文件，请重命名或选择新的目标文件夹。")
        except FileNotFoundError:
            self.main_page.return_msg_update("指定的源文件或目标文件夹不存在")

    def random_get_images(self, files_in_folder, image_num):
        if image_num > len(files_in_folder):  # 如果需要的图片超出文件夹中图片的数量, 打乱文件夹中的图片(用于后续插入)
            random.shuffle(files_in_folder)
            return files_in_folder
        else:
            random_images_l = []
            for i in range(image_num):
                image = random.choice(files_in_folder)
                random_images_l.append(image)
                files_in_folder.remove(image)
            return random_images_l

    def check_txt_files(self, txt_files, image_folder, image_num):
        return_content_l = []
        for txt_file in txt_files:
            if self.export_running:
                images_l = self.random_get_images(image_folder[:], image_num)         # 重新洗牌
                title = self.get_filename_without_extension(txt_file)                   # 获取pure title
                image_status, keywords, return_content = self.file_deal(txt_file, images_l, title)      # 文件处理
                print(111111, image_status)
                if image_status:
                    return_content_l.append({'content': return_content, 'title': title, 'keywords': keywords, 'path': txt_file})      # 不需要keywords作为第一行
        return return_content_l

    def get_filename_without_extension(self, file_path):
        return os.path.splitext(os.path.basename(file_path))[0]

    def insert_url_randomly(self, text, url_l, title):
        words = text.split('\n')  # 将字符串按空白字符分割成单词列表
        for url in url_l:
            status, web_url = self.request_image_web_url(url, title)
            if status:          # 如果返回成功
                random_index = random.randrange(len(words))  # 选择随机插入URL的位置
                word = words[random_index]
                if '# ' in word or '* ' in word or '. ' in word or "+ " in word or "- " in word or '< ' in word or ('|' in word and ':' in word):
                    words.insert(random_index + 1, f"\n{web_url}\n")  # 在随机位置插入URL
                else:
                    words.insert(random_index, f"\n{web_url}\n")  # 在随机位置插入URL

                # words.insert(random_index, web_url)  # 在随机位置插入URL
            else:
                self.main_page.return_msg_update(f"图片路径: {url} 错误信息: URL转换错误，此URL录入失败。,请检查该图片格式后稍后再试，本次上传将不会录入本篇文章。")
                return False, ''
        return True, '\n'.join(words)  # 将单词列表重新连接成字符串

    def file_deal(self, file, images_l, title):
        print("正在运行的file: ", file)
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        external_image_status, content = self.check_content_image_url(content)
        image_status, new_content = self.insert_url_randomly(content, images_l, title)
        print(external_image_status, image_status, content)
        if external_image_status and image_status:
            self.update_jieba_dict()
            keywords_l = self.jieba_get_keywords(content)
            keywords_line = ",".join(keywords_l)
            return image_status, keywords_line, new_content
        return image_status and external_image_status, '', ''

    def check_content_image_url(self, content):
        image_status, content_text = UploadScraperTxt(content, self.main_page).main()
        return image_status, content_text

    def request_image_web_url(self, local_url, title):
        # return True, local_url
        data = {}
        if local_url in self.image_path_d:
            return True, self.image_path_d.get(local_url)
        else:
            url = f'{self.main_page.domain}/index.php?m=attachment&c=attachments&a=upload'
            print("图片url: ", local_url)
            data['upload'] = (local_url, open(os.path.join(local_url), 'rb+'), 'application/octet-stream')
            for i in range(3):
                try:
                    response = self.session.post(url, cookies=self.cookies, headers=self.headers, data=data, files=data).json()
                    print("图片上传后台返回: ", response)
                except Exception as e:
                    my_logger.error(e)
                    time.sleep(1)
                else:
                    self.image_path_d[local_url] = "<img src=" + f'"{self.main_page.domain}{response["url"]}"' + f' alt="{title}" />'
                    return True, "<img src=" + f'"{self.main_page.domain}{response["url"]}"' + f' alt="{title}" />'        # 暂时先如此
            return False, ''

    def get_lanmu_under_web(self):
        self.comboBox_7.clear()
        if self.comboBox_2.currentIndex() > 0:          # 随着域名变换而变换
            try:
                current_web_info = self.web_l[self.comboBox_2.currentIndex() - 1]
                self.t_get_cate_under_web_thread = GetCateUnderWebThread(self, current_web_info, self.token_api)
                self.t_get_cate_under_web_thread.start()
                self.t_get_cate_under_web_thread.msg_trigger.connect(self.main_page.return_msg_update)
                self.t_get_cate_under_web_thread.finish_trigger.connect(self.refresh_cate_under_web)

            except Exception as e:
                logging.error(e, exc_info=True)
                my_logger.error(e)

    def refresh_cate_under_web(self):
        self.comboBox_7.addItems([ele['refer_id'] + ele['name'] for ele in self.lanum_d_under_web])
        if self.article_count_ui:
            # self.article_count_ui.get_articles_left_under_web_cate()
            self.article_count_ui.get_cate_article_left()

    def get_lanmu_web(self, response_content):
        l = []
        if response_content.get('url'):
            for k, v_d in response_content['url'].items():
                l.append(v_d)
        return l

    def update_jieba_dict(self):
        status, custom_dict = self.get_sep_words()
        if not status:
            for item in custom_dict:
                jb.add_word(item, freq=99999, tag=None)     # 加入词典

    def get_lanmu_and_web(self):
        if self.comboBox.currentIndex() == 0 and self.comboBox_2.currentIndex() == 0:
            cate_choice = random.choice(self.cate_l)        # 随机选择栏目
            web_choice = random.choice(self.web_l)          # 随机选择域名
        elif self.comboBox.currentIndex() == 0:
            cate_choice = random.choice(self.cate_l)        # 随机选择栏目
            web_choice = self.web_l[self.comboBox_2.currentIndex() - 1]     # 选择的域名
        elif self.comboBox_2.currentIndex() == 0:
            cate_choice = self.cate_l[self.comboBox.currentIndex() - 1]     # 选择的栏目
            web_choice = random.choice(self.web_l)          # 随机选择域名
        else:
            cate_choice = self.cate_l[self.comboBox.currentIndex() - 1]     # 选择的栏目
            web_choice = self.web_l[self.comboBox_2.currentIndex() - 1]     # 选择的域名
        return cate_choice, web_choice

    def get_all_files(self, folder_path, suffix_l):             # 获取文件夹下的所有文件
        files = []
        # folder_path
        for file_name in os.listdir(folder_path):
            for suffix in suffix_l:
                if file_name.endswith(suffix):
                    file_path = os.path.join(folder_path, file_name)
                    if os.path.isfile(file_path):
                        files.append(file_path)
        return files

    def connect_slot(self):
        self.pushButton_2.clicked.connect(self.export)
        self.pushButton_3.clicked.connect(self.open_file)
        self.pushButton_4.clicked.connect(self.open_image_file)
        self.pushButton_7.clicked.connect(self.gain_cate_and_cate_web)
        self.comboBox_6.currentIndexChanged.connect(self.lanmu_or_web)
        self.comboBox_2.currentIndexChanged.connect(self.get_lanmu_under_web)

    def get_sep_words(self):            # 获取关键词字典
        combo_index = self.comboBox_5.currentIndex()
        parent_id = self.job_l[combo_index]['linkageid']
        if parent_id in self.sep_words_d:
            return True, self.sep_words_d[parent_id]            # True表示已在jieba字典中插入自定义词典
        else:
            url = f'{self.main_page.domain}/index.php?m=keywords&c=oauth&a=json_seoconfig_ke&sectorid={parent_id}'
            words_l = self.session.get(url, cookies=self.cookies, headers=self.headers, timeout=5).json()
            self.sep_words_d[parent_id] = words_l
            return False, words_l

    def jieba_get_keywords(self, text, k=3):
        new_text = re.sub(r'[|\-、:/\\*#^<>]', '', text)

        keyword_1 = jb.analyse.extract_tags(new_text, topK=10, allowPOS=['n','nz', 'vd', 'vn', 'nr', 'nw', 'nt', 'ORG'],)      # 默认先取10个
        keyword_2 = jb.analyse.textrank(new_text, topK=10, allowPOS=['n','nz', 'vd', 'vn', 'nr', 'nw', 'nt', 'ORG'],)
        total_l = list(set(keyword_1 + keyword_2))
        total_l.sort(key=lambda x: len(x), reverse=True)
        return_l = self.self_filter(total_l)[:k]
        return return_l

    def self_filter(self, l):
        i, j = 0, 0
        while j < len(l) and i <= j:
            if i == j:
                j += 1
            else:
                if len(l[i]) == len(l[j]):  # 长度相等作比较
                    status = self.compare_word(l[i], l[j])
                    if not status:
                        j += 1
                    else:
                        l.remove(l[j])
                else:
                    i += 1
        return l

    def compare_word(self, w1, w2):
        w_l = list(w1)
        for w in w_l:
            if w not in w2:
                return False
        return True

    def lanmu_or_web(self):
        if self.comboBox_6.currentIndex() == 0:
            self.label_4.hide()
            self.label_12.hide()

            self.comboBox_2.hide()
            self.comboBox_7.hide()

            self.label_3.show()
            self.comboBox.show()

        else:
            self.label_4.show()
            self.label_12.show()

            self.comboBox_2.show()
            self.comboBox_7.show()

            self.label_3.hide()
            self.comboBox.hide()
        if self.article_count_ui:
            self.article_count_ui.get_cate_article_left()
            self.article_storage_ui.get_table_content_title()


class JobThread(QThread):
    msg_trigger = pyqtSignal(str)
    finish_trigger = pyqtSignal(list, list)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        job_l, auto_publish_list = [], []
        url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_init'            # 获取行业， 放入comboBox中
        url2 = f'{self.ui.main_page.domain}/index.php?m=automatic&c=apps&a=time&s=1'             # 获取所有的域名

        try:
            job_l = self.ui.session.get(url, headers=self.ui.headers, cookies=self.ui.cookies).json()
            auto_publish_list = self.ui.session.get(url2, headers=self.ui.headers, cookies=self.ui.cookies).json()
        except Exception as e:
            my_logger.error(e)
            logging.error(e, exc_info=True)
            self.msg_trigger.emit("无法连接至服务器")
        finally:
            self.finish_trigger.emit(job_l, auto_publish_list)


class InitRedisThread(QThread):
    finish_trigger = pyqtSignal(dict)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        content_publish_config = {}
        try:
            content_publish_config = self.ui.redis.handle_redis_token(f'{self.ui.main_page.username}_ContentPublishConfig')
            if not content_publish_config:
                content_publish_config = {}
            else:
                content_publish_config = json.loads(content_publish_config)
        except Exception as e:
            my_logger.error(e)
            logging.error(e, exc_info=True)
        finally:
            self.finish_trigger.emit(content_publish_config)


class GainLanmu(QThread):
    msg_trigger = pyqtSignal(str)
    finish_trigger = pyqtSignal(list)

    def __init__(self, ui, parent_id):
        super().__init__()
        self.ui = ui
        self.parent_id = parent_id

    def run(self):
        try:
            # ?m=seoconfig&c=oauth&a=json_submenu&keyid=1
            url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_submenu&keyid={self.parent_id}'
            l = self.ui.session.get(url, headers=self.ui.headers, cookies=self.ui.cookies).json()
        except Exception as e:
            my_logger.error(e)
            self.msg_trigger.emit("无法连接至服务器")
            l = []
        finally:
            self.finish_trigger.emit(l)


class ExportToBase(QThread):                # 导出到文章库
    msg_trigger = pyqtSignal(str)
    move_file_trigger = pyqtSignal(dict)
    finish_trigger = pyqtSignal()

    def __init__(self, ui, format_data, txt_files, files_in_folder, image_num):
        super().__init__()
        self.ui = ui
        self.format_data = format_data
        self.request_queue = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'}
        self.session = requests.session()
        self.txt_files = txt_files
        self.files_in_folder = files_in_folder
        self.image_num = image_num

    def run(self):
        success = 0
        fail = 0
        self.update_articles_d()
        for info in self.request_queue:
            if self.ui.export_running:
                status = self.single_request(info)
                time.sleep(0.5)
                if status:
                    success += 1
                else:
                    fail += 1
        self.msg_trigger.emit(f"本次共成功导出{success}条文章，{fail}条失败")
        self.finish_trigger.emit()

    def update_articles_d(self):
        self.msg_trigger.emit("正在初始化文章列表...")
        txt_contents = self.ui.check_txt_files(self.txt_files, self.files_in_folder, self.image_num)
        for articles_d in txt_contents:
            d = {}
            d.update(self.format_data)
            d['title'] = articles_d['title']
            d['keywords'] = articles_d['keywords']
            d['content'] = articles_d['content']
            d['article_path'] = articles_d['path']
            self.request_queue.append(d)

    def get_main_long_keywords(self, cate_l):           # 获取主词和长尾词
        try:
            url = f'{self.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_seoconfig_keywords&linkageid={",".join([ele["linkageid"] for ele in cate_l])}'
            res = requests.get(url, headers=self.main_page.headers, cookies=self.main_page.cookies).json()
        except Exception as e:
            logging.error(e, exc_info=True)
            my_logger.error(e)
            return {'keyword': [], 'keywords': []}
        else:
            return res

    def single_request(self, info):
        self.msg_trigger.emit(f"正在上传{info['title']}.txt文件...")
        data = {'info[thumb]': '',
                'info[relation]': '',
                'info[inputtime]': int(time.time()),  # 2024-07-26 18:26:38
                'info[islink]': 0,
                'info[template]': '',
                'info[readpoint]': '',
                'info[allow_comment]': 1,
                'info[paytype]': 0,
                'status': 99,                       # 暂时不知道啥用
                # 'info[pubsites]': '',               # 已上传的站点 (用逗号隔开)
                'info[catid]': info['catid'],       # 栏目或者域名上传  必填
                # 'info[web]': info['web_cate'],              # 上传至的域名|栏目   用|分开
                'info[title]': info['title'],      # 必填
                'info[keywords]': info['keywords'],           # 关键词 即分词出来的那些
                'info[copyfrom]': '',               # sour
                'info[description]': '',
                'copyfrom_data': 0,
                'info[content]': info['content'],
                'add_introduce': info['add_introduce'],
                'page_title_value': '',
                'introcude_length': info['introduce_length'],
                'auto_thumb': info['auto_thumb'],
                'auto_thumb_no': info['auto_thumb_no'],  # 缩略图数量
                'info[paginationtype]': 0,
                'info[maxcharperpage]': 10000,
                'info[posids][]': -1,
                'info[groupids_view]': 1,
                'info[voteid]': '',
                'dosubmit_continue': '保存并继续发表',
                'pc_hash': self.ui.main_page.pc_hash
                }
        if info['web_or_cate']:
            data['info[web]'] = int(info['web'])
            data['info[webcatid]'] = int(info['web_cateid'])
            data['info[linkageid]'] = 0
        else:
            data['info[web]'] = 0
            data['info[webcatid]'] = 0
            data['info[linkageid]'] = int(info['linkageid'])

        url = f'{self.ui.main_page.domain}/index.php?m=content&c=content&a=add&json=1'
        # url = 'http://192.168.110.12:5001/index.php?m=content&c=content&a=add'
        try:
            # print(url)
            # print(data)
            response = self.session.post(url, data=data, headers=self.headers, cookies=self.ui.cookies)
            print("请求内容数据库添加返回: ", response.text)
            response = response.json()
        except Exception as e:
            my_logger.error(e)
            self.msg_trigger.emit(f"文件{info['title']}.txt上传失败, 错误信息: {str(e)}")
            return False
        else:
            if response.get('msg') == '数据添加成功！':
                self.msg_trigger.emit(f"文件{info['title']}.txt上传成功")
                self.move_file_trigger.emit(info)
                return True
            else:
                self.msg_trigger.emit(f"文件{info['title']}.txt上传失败")
                return False


class GetCateUnderWebThread(QThread):
    msg_trigger = pyqtSignal(str)
    finish_trigger = pyqtSignal(list)

    def __init__(self, ui, current_web_info, token_api):
        super().__init__()
        self.ui = ui
        self.current_web_info = current_web_info
        self.token_api = token_api

    def run(self):
        try:
            client = self.token_api.generateToken(self.current_web_info['token'])
            client.update({'model': 'content', 'func': 'json'})
            response = self.token_api.sendPostRequestWithToken(self.current_web_info['api'], client)
            if response.get('status'):
                self.ui.lanum_d_under_web = self.ui.get_lanmu_web(response)
            else:
                if response.get('msg'):
                    if 'Max retries exceeded with url' in response['msg']:
                        self.msg_trigger.emit(f"{self.current_web_info['web']} 接口无法连接！请检查网络以及确认接口链接是否已解析！")
                    else:
                        self.msg_trigger.emit(response.get('msg'))
                # self.main_page.return_msg_update(response.get('msg'))
        except Exception as e:
            logging.error(e, exc_info=True)
            my_logger.error(e)
        self.finish_trigger.emit(self.ui.lanum_d_under_web)


class UploadScraperTxt:

    def __init__(self, content_html, main_page):
        # self.url = 'http://www.cqxdfrj.com/biao17/500.html'
        # self.url = url
        # self.cookies = {'DMuxX_admin_email': '2dcb2xAw-Vi7l1JsR0w742Yfm3zao4TRjVZOdggqg-3f1Fmdio0I', 'DMuxX_admin_username': '3d2chnEAFmn9FMlm3H2jXX_o_acDBVRTK5zSNpODS72sgns', 'DMuxX_siteid': '2ff4SeD4hjjSPwlpjKG0r9hM2hRSrbXVEZFiv6Em', 'DMuxX_sys_lang': '14aaYe6SgSetL_l-InYX60VkZR86MJ8Feg_vl_uy1u2n9w', 'DMuxX_userid': 'a781BqOJSEXH1HyY229fOVab4bH7iiYhN9pHHArn', 'PHPSESSID': 'kf9fj9414f25ifkmgj2r2pdu89'}
        # self.headers = {
        #                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        #                 }
        self.content_html = content_html
        self.main_page = main_page
        self.requests_url = f'{self.main_page.domain}/index.php?m=attachment&c=attachments&a=upload'
        self.cookies = self.main_page.cookies
        self.headers = self.main_page.headers

    def main(self):
        # 获取内容html -> 提取图片url -> 上传图片 -> 替换图片url -> 上传html
        # content_html = self.get_content()
        image_urls_l = self.get_content_image_urls()
        print(4444444444, image_urls_l)
        if image_urls_l:
            image_status, image_refer_d = self.get_image_refer_d(image_urls_l)
            if image_status:
                for k, v in image_refer_d.items():
                    self.content_html = self.content_html.replace(k, v)
            else:
                return False, self.content_html
                # content_publish -> upload_html
        return True, self.content_html.replace("\\n", "\n")

    def get_content(self):
        content_html = requests.get(self.url).text
        return content_html

    def get_content_image_urls(self):
        """提取html中的图片url"""
        pattern = re.compile(r'(?<=<img src=").*?(?=" )')
        urls = []
        # urls += re.findall(pattern, content_html)
        # print(urls)
        html_urls = re.findall(pattern, self.content_html)
        print(html_urls)

        # pre_fix = 'https:' if 'https' in self.url else 'http:'
        # print(pre_fix)
        pre_fix = 'https:'
        for url in html_urls:
            if 'http' in url:
                urls.append(url)
            else:
                urls.append(pre_fix + url)
        print(urls)
        return urls

    def get_image_refer_d(self, urls):
        refer_d = {}
        for url in urls:
            image_base64 = self.image_url_to_base64(url)
            if not image_base64:
                return False, refer_d
            print(image_base64)
            image_in_bytes = self.convert_base64_to_bytes(image_base64)
            data = {}
            data['upload'] = (url, image_in_bytes, 'application/octet-stream')
            for i in range(3):
                try:
                    res = requests.post(self.requests_url, headers=self.headers, cookies=self.cookies, files=data, data=data).json()
                    print(res)
                except Exception as e:
                    logging.error(e, exc_info=True)
                else:
                    refer_d[url] = res['url']
                    break

            else:
                return False, refer_d
        return True, refer_d

    def convert_base64_to_bytes(self, base64_str):
        # 去掉头部信息
        if 'data' in  base64_str:
            base64_data = base64_str.split(',')[1]
        else:
            base64_data = base64_str
        # 解码Base64字符串
        byte_data = base64.b64decode(base64_data)
        return byte_data

    def image_url_to_base64(self, image_url):
        # 发送请求获取图片
        try:
            response = requests.get(image_url)

            if response.status_code == 200:
                # 获取图片的字节流
                image_data = response.content
                # 转换为Base64编码
                base64_image = base64.b64encode(image_data).decode('utf-8')
                return base64_image
            else:
                # raise Exception(f"Failed to retrieve image, status code: {response.status_code}")
                return ''
        except Exception as e:
            logging.error(e, exc_info=True)
            return ''
