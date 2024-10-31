import time
import logging
from frontend.content_publish.article_count.article_count import Ui_Form
import requests
from backend.content_publish.article_count.set_table import SetTable
from backend.content_publish.article_count.table_insertion import TableInsertion
from backend.auto_publish.auto_publishment.auto_publishment import GetAvailableLinkageId            # 用于获取文章内容数量
import os
from model.utils import content_publish_logger as my_logger
import random
import re
import datetime
from PyQt5.QtCore import *
from collections import OrderedDict
from api_requests.RedisAPI import RedisDb
import json
import tldextract


class ArticleCount(Ui_Form):
    def __init__(self, page, parent_ui):
        super().__init__()
        self.setupUi(page)
        self.page = page
        self.parent_ui = parent_ui
        self.redis = RedisDb()
        self.main_page = parent_ui.main_page
        # self.cate_article_count_d = {}
        # self.web_article_count_d = {}
        self.job_cate_articles_l, self.web_refer_sector_d = [], {}
        self.tableWidget_2.hide()
        self.redis_response = [{}, {}]          # init cate_articles_d和web_article_count_d
        SetTable(self.tableWidget, self.main_page).main()
        SetTable(self.tableWidget_2, self.main_page).main()
        # self.get_content_count_left()

    def get_cate_article_left(self):
        # redis_response = self.redis.handle_redis_token(f'{self.main_page.username}_ArticlesCountList')
        # if redis_response:
        #     self.redis_response = json.loads(redis_response)

        if self.parent_ui.comboBox_5.currentIndex() >= 0:           # 确认行业栏目 >= 0
            current_job_info = self.parent_ui.job_l[self.parent_ui.comboBox_5.currentIndex()]
            model_index = self.parent_ui.comboBox_6.currentIndex()          # 根据栏目或者站点  0根据栏目  1根据web
            if self.parent_ui.comboBox_7.currentIndex() > -1 and self.parent_ui.comboBox_6.currentIndex() != 0 and model_index == 1:          # 当查看的不是个别站点栏目 以及 当前是查看站点的情况下跑这个
                self.tableWidget_2.show()
                self.tableWidget.hide()
                self.t_get_web_cate_articles_left = GetWebCateArticleLeft(self)
                self.t_get_web_cate_articles_left.start()
                self.t_get_web_cate_articles_left.finish_trigger.connect(self.return_web_cate_article_left)
                # self.get_articles_left_under_web_cate()
            else:
                self.tableWidget.show()
                self.tableWidget_2.hide()
                self.t_get_article_left = GetCateArticleLeft(self, self.parent_ui, model_index)
                self.t_get_article_left.start()
                self.t_get_article_left.finish_trigger.connect(self.return_article_left)
            # else:
            #     TableInsertion(self.tableWidget).table_main(self.redis_response[model_index].get(current_job_info['typeid']))

    def return_web_cate_article_left(self, return_l):
        TableInsertion(self.tableWidget_2).table_main(return_l)

    def return_article_left(self, return_l):
        current_job_info = self.parent_ui.job_l[self.parent_ui.comboBox_5.currentIndex()]  #
        model_index = self.parent_ui.comboBox_6.currentIndex()  # 根据栏目或者站点  0根据栏目  1根据web
        self.redis_response[model_index][current_job_info['typeid']] = return_l
        self.redis.handle_redis_token(f'{self.main_page.username}_ArticleCountList', json.dumps(self.redis_response), 24*60*60)      # 存一天
        TableInsertion(self.tableWidget).table_main(self.redis_response[model_index][current_job_info['typeid']])

    def get_articles_left_under_web_cate(self):
        try:
            current_web_info = self.parent_ui.web_l[self.parent_ui.comboBox_2.currentIndex() - 1]
            current_web_refer_id_d = {ele['catid']: ele['refer_id'] for ele in self.web_refer_sector_d[current_web_info['web']]}
            params = {'web': current_web_info['id'], 'webcatid': ",".join(ele['catid'] for ele in self.parent_ui.lanum_d_under_web)}
            url = f'{self.main_page.domain}/index.php?m=automatic&c=oauth&a=json_site_content_star'
            res = requests.get(url, headers=self.parent_ui.headers, cookies=self.parent_ui.cookies, params=params).json()
            l = []
            if res.get('status'):
                d = {}
                for item in res['data']['all']:
                    d[item['webcatid']] = {'count': item['num'],
                                           'left_count': self.find_web_cate_left_count(item['webcatid'], res['data']['unpub'], item['num']),
                                           }
                for item in self.parent_ui.lanum_d_under_web:
                    if item['catid'] in d:
                        l.append({'name': item['name'], 'count': d[item['catid']]['count'],
                                  'left_count': d[item['catid']]['left_count'],
                                  'catid': current_web_refer_id_d[item['catid']],
                                  'web': False})
                    else:
                        l.append({'name': item['name'],
                                  'count': '0',
                                  'left_count': '0',
                                  'catid': current_web_refer_id_d[item['catid']],
                                  'web': False})
                return l
            else:
                if res.get('msg') == '未查询到数据!':
                    for item in self.parent_ui.lanum_d_under_web:
                        l.append({'name': item['name'],
                                  'count': '0',
                                  'left_count': '0',
                                  'catid': current_web_refer_id_d[item['catid']],
                                  'web': False})
                return l
        except Exception as e:
            logging.error(e)
            return []

    def get_articles_left_under_web(self):
        url = f'{self.main_page.domain}/index.php?m=automatic&c=oauth&a=json_web_unpub&web={",".join([ele["id"] for ele in self.parent_ui.web_l])}'
        try:
            res = requests.get(url, headers=self.parent_ui.headers, cookies=self.parent_ui.cookies).json()
        except Exception as e:
            logging.error(e, exc_info=True)
            self.main_page.return_msg_update(str(e))
        else:
            return res['data']

    def find_web_cate_left_count(self, cate_id, unpub, count):
        for ele in unpub:
            if ele['webcatid'] == cate_id:
                return ele['num']
        else:
            return count

    def get_content_count_left(self):
        url = f'{self.main_page.domain}/index.php?m=automatic&c=apps&a=time&s=1'
        try:
            auto_publish_list = requests.get(url, headers=self.parent_ui.headers, cookies=self.parent_ui.cookies).json()
        except Exception as e:
            logging.error(e, exc_info=True)
            self.main_page.return_msg_update(str(e))
            auto_publish_list = []
        redis_response = self.redis.handle_redis_token(f"jw_refer_d")
        # redis_response = None
        if redis_response:
            combin_d = json.loads(redis_response)
            self.job_cate_articles_l, self.web_refer_sector_d = combin_d['job_cate_articles_l'], combin_d['web_refer_sector_d']
        else:
            self.job_cate_articles_l, self.web_refer_sector_d = GetAvailableLinkageId(self.parent_ui, auto_publish_list).get_refers()
            combin_d = {'job_cate_articles_l': self.job_cate_articles_l, 'web_refer_sector_d': self.web_refer_sector_d}
            print("job cate: ", self.job_cate_articles_l)
            print("web refer: ", self.web_refer_sector_d)
            self.redis.handle_redis_token(f"jw_refer_d", json.dumps(combin_d), self.get_current_to_tmr_seconds())
        return self.calculate_content_count([ele['id'] for ele in auto_publish_list], {ele['catid']: ele['count'] for ele in self.job_cate_articles_l}, self.web_refer_sector_d)

    def calculate_content_count(self, domain_l, cate_content_count_d, web_refer_d):
        d = {}
        for web, web_cate_l in web_refer_d.items():
            for cate_info in web_cate_l:
                if cate_info['refer_id'] in cate_content_count_d:
                    if d.get(cate_info['refer_id']) and d[cate_info['refer_id']].get('count'):
                        d[cate_info['refer_id']]['count'] += int(cate_content_count_d[cate_info['refer_id']])
                        d[cate_info['refer_id']]['left_count'] += int(cate_content_count_d[cate_info['refer_id']])

                    else:
                        d[cate_info['refer_id']] = {}
                        d[cate_info['refer_id']]['count'] = int(cate_content_count_d[cate_info['refer_id']])
                        d[cate_info['refer_id']]['left_count'] = int(cate_content_count_d[cate_info['refer_id']])
        linkage_id_articles_l = self.get_db_linkage_articles_count(domain_l)
        for item in linkage_id_articles_l:
            if item['count'] != '0' and item['linkageid'] in d:
                d[item['linkageid']]['left_count'] -= int(item['count'])
        return d

    def get_db_linkage_articles_count(self, domain_l):
        try:
            url = f'{self.main_page.domain}/index.php?m=automatic&c=oauth&a=json_site_list_stat&webids={",".join(domain_l)}'
            res = requests.get(url, headers=self.main_page.headers, cookies=self.main_page.cookies).json()
            if res.get('status'):
                return res['data']
            else:
                return []
        except Exception as e:
            logging.error(e, exc_info=True)
            return []

    def get_current_to_tmr_seconds(self):
        now = datetime.datetime.now()
        # 获取明天的0点时间
        tomorrow_start = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        # 计算相差的秒数
        seconds_until_midnight = (tomorrow_start - now).seconds
        return seconds_until_midnight


class GetCateArticleLeft(QThread):
    finish_trigger = pyqtSignal(list)

    def __init__(self, ui, parent_ui, model_index):
        super().__init__()
        self.ui = ui
        self.parent_ui = parent_ui
        self.model_index = model_index
        self.session = requests.session()

    def run(self):
        l = []
        url = f'{self.parent_ui.main_page.domain}/index.php?m=automatic&c=oauth&a=json_linkage_web_all'
        if self.model_index:
            web_l = ",".join([ele['id'] for ele in self.parent_ui.web_l])
            params = {}
            params['web'] = web_l
        else:
            linkageid_l = ",".join([ele['linkageid'] for ele in self.parent_ui.cate_l])
            params = {}
            params['linkageid'] = linkageid_l

        try:
            response = self.session.get(url, headers=self.parent_ui.headers, cookies=self.parent_ui.cookies, params=params).json()
        except Exception as e:
            logging.error(e, exc_info=True)
        else:
            try:
                if response.get('status'):
                    if self.model_index:           # model index == 1 也就是根据网页来
                        web_left_d = self.ui.get_articles_left_under_web()
                        print(1111111111111, web_left_d)
                        for item in self.parent_ui.web_l:
                            if item['id'] in response['number']:
                                count = int(response['number'][item['id']]) if response['number'].get(item['id']) else 0
                                l.append({'name': tldextract.extract(item['web']).registered_domain, 'count': count,
                                         'left_count': web_left_d[item['id']], 'catid': item['id'], 'web': True})
                    else:
                        left_articles_d = self.ui.get_content_count_left()
                        print(222222222222222)
                        for item in self.parent_ui.cate_l:
                            d = {}
                            if response['number'].get(item['linkageid']):
                                count = str(response['number'][item['linkageid']]) if response['number'].get(item['linkageid']) else 0
                                d = {'name': item['name'], 'count': count, 'catid': item['linkageid'], 'web': False}
                            if left_articles_d.get(item['linkageid']):
                                d['left_count'] = f"{left_articles_d[item['linkageid']]['left_count']}/ {left_articles_d[item['linkageid']]['count']}"
                            else:
                                d['left_count'] = 'N/A'
                            l.append(d)
                self.finish_trigger.emit(l)
            except Exception as e:
                logging.error(e, exc_info=True)


class GetWebCateArticleLeft(QThread):
    finish_trigger = pyqtSignal(list)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        l = self.ui.get_articles_left_under_web_cate()
        self.finish_trigger.emit(l)