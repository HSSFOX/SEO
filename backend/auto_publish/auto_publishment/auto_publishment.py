from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import requests
from frontend.auto_publish.auto_publishment.auto_publishment import Ui_Form
from backend.auto_publish.auto_publishment.set_table import SetTable
from model.utils import auto_publish_logger as my_logger
import datetime
import time
import threading
import schedule
from backend.auto_publish.auto_publishment.table_insertion import TableInsertion
from backend.auto_publish.auto_publishment.auto_publishment_window.auto_publishment_window import AutoPublishmentWindow
import random
from api_requests.TokenAPI import Token
import re
import base64
from api_requests.RedisAPI import RedisDb
import logging
import json
import copy
import tldextract


class AutoPublishment(Ui_Form):
    def __init__(self, page, parent_ui, main_page):
        super().setupUi(page)
        self.ui = page
        self.parent_ui = parent_ui
        self.main_page = main_page
        SetTable(self.tableWidget, self.tableWidget_2, main_page).main()

        self.cookies = main_page.cookies
        self.headers = main_page.headers
        self.auto_publish_list = []
        self.web_cate_sum_d = {}
        self.fail_attempt = 3
        self.spinBox_2.setValue(3)
        self.redis = RedisDb()
        self.session = requests.session()
        self.init_button()
        self.page = 0
        self.page_2 = 0         # 已推送的表
        self.row_limit = 100
        self.max_page = 0
        self.max_page_2 = 0     # 已推送表的max_page
        self.tasks_list = []
        self.published_l = []
        self.linkageid_refer_web_cate_d = {}

        self.job_cate_articles_l, self.web_refer_sector_d = [], {}
        self.task_running = False           # 不直接开始任务
        self.pushButton.setEnabled(False)
        self.token_api = Token()
        self.timer_slave = TimerSlave(self)
        self.ui_auto_publish_window = AutoPublishmentWindow(self)
        self.connect_slot()

    def fail_attmpt_changed(self):
        self.fail_attempt = self.spinBox_2.value()

    def init_thread(self):          # 初始化发布任务
        schedule.clear()
        self.timer_slave.start_timer()               # 重新计时
        self.pushButton.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.return_msg_trigger("正在初始化发布数据...")
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.clearContents()
        self.tasks_list = []
        self.published_l = []
        self.t_init = InitThread(self)
        self.t_init.start()
        self.t_init.finished.connect(self.init_sub_ui)

    def init_sub_ui(self):
        self.get_check_popup_msg()
        self.return_msg_trigger("发布任务初始化完成")
        self.pushButton.setEnabled(True)
        self.pushButton_6.setEnabled(True)
        print("确认属性, 已自动初始化完毕, 准备清除已有任务并开启新一天任务: ", self.task_running)

        if self.tasks_list:
            if self.task_running:
                schedule.clear()            # 清除上一天的计划任务
                self.ui_auto_publish_window.run()
        else:
            self.main_page.return_msg_update("无自动发布任务或域名")
            schedule.clear()                # 清除上一天的计划任务

    def main(self):
        url = f'{self.main_page.domain}/index.php?m=automatic&c=apps&a=time&s=1'
        try:
            self.auto_publish_list = requests.get(url, headers=self.headers, cookies=self.cookies).json()
        except Exception as e:
            my_logger.error(e)
            self.main_page.return_msg_update(str(e))

    def execute_publish(self):
        if not self.tasks_list:
            for auto_publish in self.auto_publish_list:
                single_domain_task_l = []
                start_time = datetime.datetime.strptime(auto_publish['start_time'], '%H:%M:%S')
                end_time = datetime.datetime.strptime(auto_publish['start_times'], '%H:%M:%S')
                # settle_time_l = self.get_settle_time(end_time, int(auto_publish['num']))                    # 在自动发布时间段内
                # settle_time_l = self.get_settle_time(end_time, int(auto_publish['num']), start_time)        # 如果不在自动发布时间段内, 明日这个时间段发
                settle_time_l = self.get_random_settle_time(start_time, end_time, int(auto_publish['num']))
                for settle_time in settle_time_l:
                    d = {}
                    d['web'] = auto_publish['web']
                    d['num'] = int(auto_publish['num'])
                    d['api'] = auto_publish['api']
                    d['id'] = auto_publish['id']
                    d['settle_time'] = int(settle_time.timestamp())
                    d['published'] = "否"
                    d['typeid'] = auto_publish['typeid']
                    d['token'] = auto_publish['token']
                    d['order'] = auto_publish['order']
                    d['release'] = auto_publish['release']
                    d['baidu_rule'] = auto_publish['baidu_rule']
                    d['title'] = ''     # 后续插表使用
                    d['posids'] = ['-1']
                    d['published_url'] = ''
                    single_domain_task_l.append(d)
                single_domain_task_l = self.random_pos_ids(single_domain_task_l)
                self.tasks_list += single_domain_task_l

            # print("self.task_list: ", self.tasks_list)       # self.insert_l = self.tasks_list

            self.tasks_list.sort(key=lambda x: x['settle_time'])
            self.insert_table(self.tasks_list)

            self.redis.handle_redis_token(f"{self.main_page.username}_automatic_task_list", json.dumps(self.tasks_list), self.get_current_to_tmr_seconds())
            # self.init_schedule()
        else:
            self.insert_table(self.tasks_list)
        if self.checkBox.isChecked():         # 判断是否刷新
            redis_response = None
        else:
            redis_response = self.redis.handle_redis_token(f"jw_refer_d")
        if redis_response:
            combin_d = json.loads(redis_response)
            self.job_cate_articles_l, self.web_refer_sector_d = combin_d['job_cate_articles_l'], combin_d['web_refer_sector_d']
        else:
            self.job_cate_articles_l, self.web_refer_sector_d = GetAvailableLinkageId(self, self.tasks_list).get_refers()
            combin_d = {'job_cate_articles_l': self.job_cate_articles_l, 'web_refer_sector_d': self.web_refer_sector_d}
            self.redis.handle_redis_token(f"jw_refer_d", json.dumps(combin_d), self.get_current_to_tmr_seconds())
        # print("j: ", self.job_cate_articles_l)
        # print("w: ", self.web_refer_sector_d)
        self.get_linkageid_refer_web_cate()

    def get_check_popup_msg(self):
        empty_sites = []
        for k, v in self.web_refer_sector_d.items():
            if not v:
                empty_sites.append(k)
        if empty_sites:
            site_str = "\n".join(empty_sites)
            print(empty_sites)
            print(site_str)
            reply = QMessageBox.information(self.ui, '提示报告', f'以下站点未检测到可用栏目 详情见日志！{site_str} ', QMessageBox.Ok)

    def get_linkageid_refer_web_cate(self):         # linkage id refer_cate
        self.linkageid_refer_web_cate_d = {}
        for k, v in self.web_refer_sector_d.items():
            self.linkageid_refer_web_cate_d[k] = {}
            for v_l in v:
                self.linkageid_refer_web_cate_d[k][v_l['refer_id']] = {'name': v_l['name'], 'catid': v_l['catid']}

    def get_current_to_tmr_seconds(self):
        now = datetime.datetime.now()
        # 获取明天的0点时间
        tomorrow_start = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        # tomorrow_start = now + datetime.timedelta(seconds=20)

        # 计算相差的秒数
        seconds_until_midnight = (tomorrow_start - now).seconds - 10            # 10秒钟维护时间  23:59:50
        return seconds_until_midnight

    def random_pos_ids(self, single_domain_task_l):
        if single_domain_task_l:
            random_int = random.randint(1, 3)
            for _ in range(random_int):
                single_domain_task_l[random.randint(0, len(single_domain_task_l) - 1)]['posids'] = [str(random.randint(2, 9)), '0']
        return single_domain_task_l

    def insert_table(self, insert_l):
        TableInsertion(self, self.tableWidget, self.tableWidget_2).main(insert_l[self.row_limit * self.page: self.row_limit * (self.page + 1)])     # [0: 100]
        self.published_l = self.get_publish_list_only(insert_l)
        TableInsertion(self, self.tableWidget, self.tableWidget_2).main_2(self.published_l[self.row_limit * self.page_2: self.row_limit * (self.page_2 + 1)])
        self.max_page = len(insert_l) // self.row_limit + 1 if len(insert_l) % self.row_limit > 0 else len(insert_l) // self.row_limit        # 更新max_page
        self.max_page_2 = len(self.published_l) // self.row_limit + 1 if len(self.published_l) % self.row_limit > 0 else len(self.published_l) // self.row_limit        # 更新max_page
        self.update_label_info()
        self.update_label_info_2()

    def get_publish_list_only(self, insert_l):
        return [ele for ele in insert_l if ele['published'] == '已推送']

    def t1_next_page(self):
        self.page += 1
        TableInsertion(self, self.tableWidget, self.tableWidget_2).t1_insertion(self.tasks_list[self.row_limit * self.page: self.row_limit * (self.page + 1)])     # [0: 100]
        self.update_label_info()

    def t1_previous_page(self):
        self.page -= 1
        TableInsertion(self, self.tableWidget, self.tableWidget_2).t1_insertion(self.tasks_list[self.row_limit * self.page: self.row_limit * (self.page + 1)])     # [0: 100]
        self.update_label_info()

    def t2_next_page(self):
        self.page_2 += 1
        TableInsertion(self, self.tableWidget, self.tableWidget_2).main_2(self.published_l[self.row_limit * self.page_2: self.row_limit * (self.page_2 + 1)])     # [0: 100]
        self.update_label_info_2()

    def t2_previous_page(self):
        self.page_2 -= 1
        TableInsertion(self, self.tableWidget, self.tableWidget_2).main_2(self.published_l[self.row_limit * self.page_2: self.row_limit * (self.page_2 + 1)])     # [0: 100]
        self.update_label_info_2()

    def update_label_info(self):            # 用于翻页前或翻页后更新 button和label的数据
        if self.page == 0:
            self.pushButton_2.setEnabled(False)
        else:
            self.pushButton_2.setEnabled(True)
        if self.page == self.max_page - 1:
            self.pushButton_3.setEnabled(False)
        else:
            self.pushButton_3.setEnabled(True)
        self.label_5.setText(f"当前第{self.page + 1}页")

    def update_label_info_2(self):  # 用于翻页前或翻页后更新 button和label的数据
        if self.page_2 == 0:
            self.pushButton_4.setEnabled(False)
        else:
            self.pushButton_4.setEnabled(True)
        if self.page_2 == self.max_page_2 - 1:
            self.pushButton_5.setEnabled(False)
        else:
            self.pushButton_5.setEnabled(True)
        self.label_6.setText(f"当前第{self.page_2 + 1}页")

    def init_button(self):
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)

    def get_settle_time(self, end_time, num, start_time=datetime.datetime.now()):
        now = start_time
        seconds_today = (now - datetime.datetime(now.year, now.month, now.day)).total_seconds()
        end_time_seconds = end_time.hour * 3600 + end_time.minute * 60 + end_time.second
        time_diff = end_time_seconds - seconds_today
        ratio = int(time_diff / (num + 1))
        settle_datetime_l = []
        for i in range(num):
            settle_datetime = now + datetime.timedelta(seconds=ratio * i) + datetime.timedelta(seconds=15)
            # settle_datetime = now + datetime.timedelta(seconds=ratio * i)           # 即时启动
            settle_datetime_l.append(settle_datetime.replace(microsecond=0))

        return settle_datetime_l

    def get_random_settle_time_2(self, start_time, end_time, num, gap_time=180):
        gap = (end_time - start_time).total_seconds()
        l = []      # 返回
        s = []      # 去重用
        for i in range(num):
            n = random.randrange(0, gap)
            if n not in s:
                l.append(start_time + datetime.timedelta(seconds=n))
                s += [j for j in range(n - gap_time, n + gap_time)]       # 前后3mins gap
        l.sort()
        return l

    def get_random_settle_time(self, start_time, end_time, num):
        gap = (end_time - start_time).total_seconds()
        now = datetime.datetime.now()
        now_start_time = start_time.replace(year=now.year, month=now.month, day=now.day)
        l = []      # 返回
        s = []      # 去重用
        i = 0
        while i < num:
            n = random.randrange(0, gap)
            if n not in s:
                l.append(now_start_time + datetime.timedelta(seconds=n))
                i += 1
                s += [n]       # 前后3mins gap
        l.sort()
        return l

    def update_published_site(self, task_info, content_data_id):
        url = f'{self.main_page.domain}/index.php?m=automatic&c=oauth&a=json_published'
        push_data = {}
        push_data['id'] = int(content_data_id)
        push_data['web'] = int(task_info['id'])
        # push_data = {'id': int(content_data_id), 'web': int(task_info['id'])}
        print("更新数据库 publish_sites", push_data)
        res = self.session.post(url, headers=self.headers, cookies=self.cookies, data=push_data)
        print("更新已发布站点的数据库返回", res.text)

    def update_images(self, content, web_info):
        print("web_info: ", web_info)
        pattern_img = r'<img[^>]+src="([^">]+)"'
        pattern_md = r'!\[.*?\]\((.*?)\)'
        domain = 'http://' + web_info['web'] if 'http' not in web_info['web'] else web_info['web']
        api_url = web_info['api']
        matches_1 = re.findall(pattern_img, content)
        matches_2 = re.findall(pattern_md, content)
        images_l = matches_1 + matches_2
        d = {}

        for image in images_l:
            try:
                image_url = self.main_page.domain + image if 'http' not in image else image
                print(3333333333333, image_url)
                res = requests.get(image_url)
                if res.status_code == 200:
                    image_base64 = base64.b64encode(res.content).decode('utf-8')
                    image_data = base64.b64decode(image_base64)

                    client_data = self.token_api.generateToken(web_info['token'])
                    client_data['model'] = 'attachment'
                    file = (image_url.split("/")[-1], image_data, 'application/octet-stream')
                    client_data['upload'] = file

                    res = self.token_api.HttpPostCookie(api_url, client_data)
                    print("上传图片返回", res)            # 这里重复文件的意思为 数据库已有该图片的md5记录, 直接返回url
                    if res['msg'].get('url'):
                        # img_domain_l = res['msg']['url'][2:].split("/")
                        # path = tldextract.extract(img_domain_l[0]).registered_domain.replace(".", "_")
                        # print(path, img_domain_l)
                        # url = "//" + img_domain_l[0] + "/" + path + "/" + "/".join(img_domain_l[1:])
                        d[image] = res['msg']['url']
                    else:
                        d[image] = ''
                        self.main_page.return_msg_update(
                            f"站点任务 - 站点ID: {web_info['id']}, 域名: {web_info['web']} 上传图片失败！")
                else:
                    d[image] = ''
                    self.main_page.return_msg_update(
                        f"站点任务 - 站点ID: {web_info['id']}, 域名: {web_info['web']} 上传图片失败！")
            except Exception as e:
                logging.error(e, exc_info=True)
                d['image'] = ''
                self.main_page.return_msg_update(
                    f"站点任务 - 站点ID: {web_info['id']}, 域名: {web_info['web']} 获取图片失败！")
        return d

    def content_push(self, task_info, content_data, image_refer_d):
        # print("content: ", content_data)
        try:
            self.fail_attempt = int(self.spinBox_2.value())
        except Exception as e:
            self.fail_attempt = 3
        push_response = {'status': False, "msg": '推送失败', 'url': '推送失败'}
        url = task_info['api']
        for old_image in image_refer_d:
            if not image_refer_d[old_image]:
                return {'status': False, "msg": '推送失败！错误信息: 图片上传失败, 此文章将不会上传！'}
            content_data['content'] = content_data['content'].replace(old_image, image_refer_d[old_image])
        for i in range(self.fail_attempt):
            try:
                client = self.token_api.generateToken(task_info['token'])
                client['model'] = 'content'
                client['act'] = 'submit'
                client['info'] = {'catid': self.get_web_cate_id(task_info, content_data),
                                  'title': content_data['title'],
                                  'description': content_data['description'],
                                  'keywords': content_data['keywords'],
                                  'content': content_data['content'],
                                  'username': content_data['username'],
                                  'posids': task_info['posids'],
                                  'islink': '0',
                                  }
                client['auto_thumb'] = content_data['auto_thumb'] if 'auto_thumb' in content_data else '1'
                client['auto_thumb_no'] = content_data['auto_thumb_no'] if 'auto_thumb_no' in content_data else '1'
                # print("参数", client)
                push_response = self.token_api.sendPostRequestWithToken(url, client)
                print("上传", push_response)
                if push_response.get('status'):
                    task_info['published'] = '已推送'
                    task_info['title'] = content_data['title']
                    task_info['published_url'] = task_info['web'] + push_response['url']
                    self.published_l.append(task_info)
                    return push_response

                else:
                    # task_info['published'] = push_response.get('msg')
                    task_info['published'] = '推送失败'
                    return {'status': False, "msg": push_response.get('msg')}
            except Exception as e:
                logging.error(e, exc_info=True)
                time.sleep(1)
                my_logger.error(e)
                return {'status': False, "msg": str(e)}
        else:
            task_info['published'] = '推送失败'
            return {'status': False, "msg": push_response.get('msg')}

    def get_web_cate_id(self, web_info, content):
        if content['webcatid'] == '0':
            if self.linkageid_refer_web_cate_d.get(web_info['web']):
                return self.linkageid_refer_web_cate_d[web_info['web']][content['linkageid']]['catid']
            else:
                self.main_page.return_msg_update(
                    f"站点任务 - 站点ID: {web_info['id']}, 域名: {web_info['web']} {content['title']}获取网站栏目ID错误，请手动检查！")
                return '0'
        else:
            return content['webcatid']

    def get_random_content(self, web_info):
        res = {'status': False, 'msg': f"未获取到该站点{web_info['web']}下可用的栏目, 可能原因: 网站无法连接或无可用文章"}
        linkage_id_l = self.get_random_linkageid(web_info)
        if linkage_id_l:
            web_id = web_info['id']
            order = web_info['order']
            try:
                url = f'{self.main_page.domain}/index.php?m=automatic&c=oauth&a=json_release'
                params = {'linkageid[]': linkage_id_l, 'order': order, 'web': web_id}
                res = requests.get(url, headers=self.headers, cookies=self.cookies, params=params, timeout=5).json()
                print("1111111111111111111111， ", res)
            except Exception as e:
                logging.error(e, exc_info=True)
                my_logger.error(e)
                self.main_page.return_msg_update(f"未获取到数据库连接")
                res = {'status': False, 'msg': str(e)}
        return res

    def return_task_l_publish(self, task):        # 返回数据, 并更新至ui
        self.check_published_info()
        self.update_label_info_2()
        self.redis.handle_redis_token(f"{self.main_page.username}_automatic_task_list", json.dumps(self.tasks_list),
                                      self.get_current_to_tmr_seconds())          # 更新redis中的内容
        if not task['published'] == '已推送':
            self.return_msg_trigger(f"站点任务 - 站点ID: {task['id']}, 域名: {task['web']} 推送失败")
        self.update_table(task)

    def update_insert_l(self, task, status):
        for insert_task in self.tasks_list:
            if task['web'] == insert_task['web'] and insert_task['settle_time'] == task['settle_time']:
                if status:
                    insert_task['published'] = '已推送'
                else:
                    insert_task['published'] = '推送失败'
        self.redis.handle_redis_token(f"{self.main_page.username}_automatic_task_list", json.dumps(self.tasks_list),
                                      self.get_current_to_tmr_seconds())          # 更新redis中的内容

    def check_published_info(self):
        self.max_page_2 = len(self.published_l) // self.row_limit + 1 if len(self.published_l) % self.row_limit > 0 else len(self.published_l) // self.row_limit

    def update_table(self, task_info, status=True):
        TableInsertion(self, self.tableWidget, self.tableWidget_2).update_table(task_info, status)

    def init_schedule(self):
        self.schedule_t = SchduleThread()
        self.schedule_t.start()

    def return_msg_trigger(self, msg):
        self.main_page.return_msg_update(str(msg))

    def start_stop_task(self):
        if self.task_running:
            self.task_running = False
            schedule.clear()                # 清除任务
            self.schedule_t.checkSign = False
            self.pushButton.setText("开始运行")
            self.ui_auto_publish_window.pushButton.setText("开始运行")
            self.ui_auto_publish_window.tray_icon.hide()
            self.ui_auto_publish_window.actual_close = True
            self.ui_auto_publish_window.close()
        else:
            self.task_running = True
            self.pushButton.setText("停止运行")
            self.ui_auto_publish_window.actual_close = False
            self.ui_auto_publish_window.show()
            self.ui_auto_publish_window.tray_icon.show()
            self.ui_auto_publish_window.pushButton.setText("停止运行")
            self.ui_auto_publish_window.run()

    def connect_slot(self):
        self.pushButton.clicked.connect(self.start_stop_task)
        self.pushButton_2.clicked.connect(self.t1_previous_page)
        self.pushButton_3.clicked.connect(self.t1_next_page)
        self.pushButton_4.clicked.connect(self.t2_previous_page)
        self.pushButton_5.clicked.connect(self.t2_next_page)
        self.pushButton_6.clicked.connect(self.init_thread)
        self.spinBox_2.valueChanged.connect(self.fail_attmpt_changed)

    def get_lanmu_web(self, response_content):
        d = {}
        for k, v_d in response_content['url'].items():
            for s_k, s_v in v_d.items():
                d[s_v] = s_k
        return d

    def get_random_linkageid(self, web_info):
        try:
            linkage_l = [ele['refer_id'] for ele in self.web_refer_sector_d[web_info['web']]]
            available_linkage_l = []
            for item in self.job_cate_articles_l:
                if item['count'] != '0' and item['catid'] in linkage_l:
                    available_linkage_l.append(item['catid'])
                    item['count'] = str(int(item['count']) - 1)
        except Exception as e:
            logging.error(e, exc_info=True)
            available_linkage_l = []
        return available_linkage_l


class SchduleThread(QThread):
    def __init__(self):
        super(SchduleThread, self).__init__()
        self.checkSign = True

    def run(self):
        while self.checkSign:
            schedule.run_pending()
            time.sleep(1)


class InitThread(QThread):
    finished_trigger = pyqtSignal()
    def __init__(self, parent_ui):
        super(InitThread, self).__init__()
        self.parent_ui = parent_ui

    def run(self):
        try:
            self.parent_ui.main()
            if self.parent_ui.checkBox.isChecked():
                self.parent_ui.tasks_list = []
            else:
                task_list_from_redis = self.parent_ui.redis.handle_redis_token(f"{self.parent_ui.main_page.username}_automatic_task_list")
                self.parent_ui.tasks_list = json.loads(task_list_from_redis) if task_list_from_redis else []            # 重新初始化task_list
            self.parent_ui.execute_publish()
            self.finished_trigger.emit()
        except Exception as e:
            logging.error(e, exc_info=True)


class GetAvailableLinkageId:
    def __init__(self, ui, task_info_l):
        self.task_info_l = task_info_l
        self.ui = ui
        self.token_api = Token()
        self.web_cate_sum_d = {}                # web下属的栏目 refer -> 本身对应的域名下属栏目id -> 行业的栏目id  域名下栏目名称与行业下栏目id对照表
        self.job_refer_d = {}
        self.total_job_cate_l = []
        self.cate_article_count_d = {}          # 行业栏目下的文章数量统计
        self.job_cate_articles_l = []
        self.session = requests.session()

        self.job_l = self.get_init_jobs()

        self.get_sum_info()
        self.get_article_count()

    def get_refers(self):
        return self.job_cate_articles_l, self.web_cate_sum_d

    def get_sum_info(self):
        temp_l = []
        for web_info in self.task_info_l:
            if web_info['web'] in self.web_cate_sum_d:
                continue
            self.get_web_cate_info(web_info)
            if self.job_refer_d[web_info['web']]['linkageid'] not in temp_l:
                self.get_web_sector_id(self.job_refer_d[web_info['web']]['linkageid'])
                temp_l.append(self.job_refer_d[web_info['web']]['linkageid'])

    def get_article_count(self):        # 获取web下的文章数量
        url = f'{self.ui.main_page.domain}/index.php?m=automatic&c=oauth&a=json_linkage_web_all'
        linkageid_l = ",".join(list(set([ele['linkageid'] for ele in self.total_job_cate_l])))
        params = {'linkageid': linkageid_l}
        try:
            response = self.session.get(url, params=params).json()
        except Exception as e:
            logging.error(e, exc_info=True)
        else:
            if response.get('status'):
                for item in self.total_job_cate_l:
                    if item['linkageid'] in response['number']:
                        d = {'name': item['name'], 'catid': item['linkageid'],
                                  'count': str(response['number'][item['linkageid']]) if response['number'].get(item['linkageid']) else 0}
                        if d not in self.job_cate_articles_l:
                            self.job_cate_articles_l.append(d)

    def get_web_sector_id(self, web_type_id):
        url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_submenu&keyid={web_type_id}'
        response = self.session.get(url).json()
        for item in response:
            # item['parentid'] == '0' and item['arrchildid'] == item['linkageid'] 为检测自身就是子类目的一级类目

            # if item not in self.total_job_cate_l and (
            #         item['parentid'] == '0' and item['arrchildid'] == item['linkageid']) or (
            #         item['parentid'] != '0' and item['arrchildid'] != item['linkageid']):
            if item not in self.total_job_cate_l and item['arrchildid'] == item['linkageid']:
                self.total_job_cate_l.append(item)

    def get_web_cate_info(self, current_web_info):
        if current_web_info['web'] in self.web_cate_sum_d:
            return self.web_cate_sum_d.get(current_web_info['web'])
        client = self.token_api.generateToken(current_web_info['token'])
        client.update({'model': 'content', 'func': 'json'})
        for i in range(3):
            try:
                response = self.token_api.sendPostRequestWithToken(current_web_info['api'], client)
                if response.get('status'):
                    self.web_cate_sum_d[current_web_info['web']] = self.get_lanmu_web(response)
                else:
                    self.web_cate_sum_d[current_web_info['web']] = []
                    self.ui.main_page.return_msg_update(f"域名 {current_web_info['web']} 自动发布错误, 错误信息: {response['msg']}")
                break
            except Exception as e:
                logging.error(e, exc_info=True)
        else:
            self.web_cate_sum_d[current_web_info['web']] = []
            self.ui.main_page.return_msg_update(
                f"域名 {current_web_info['web']} 自动发布错误, 错误信息: 站点无法连接！")

    def get_lanmu_web(self, response_content):
        l = []
        if response_content.get('url'):
            for k, v_d in response_content['url'].items():
                l.append(v_d)
        return l

    def get_init_jobs(self):
        url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_init'  # 获取行业， 放入comboBox中
        response = self.session.get(url).json()
        for web_info in self.task_info_l:
            for job_info in response:
                if self.job_refer_d.get(web_info['web']):
                    continue
                else:
                    if web_info['typeid'] == job_info['typeid']:
                        self.job_refer_d[web_info['web']] = {'linkageid': job_info['linkageid'], 'typeid': job_info['typeid']}
        return response


class TimerSlave(QTimer):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.timeout.connect(self.ui.init_thread)
        self.start_timer()

    def start_timer(self):
        # 设置目标时间为每天固定时间，例如18:00
        time_to_wait = self.ui.get_current_to_tmr_seconds() + 10
        # time_to_wait = self.get_current_to_tmr_seconds()

        # 启动定时器
        self.start(time_to_wait * 1000)           # 以ms计数 所以 * 1000

