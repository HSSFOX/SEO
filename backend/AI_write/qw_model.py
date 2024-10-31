import time
import random
from http import HTTPStatus

import requests
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0
import dashscope
from model.utils import ai_logger as my_logger
from concurrent.futures import ThreadPoolExecutor
import logging
import re
import json

import threading
import time

APP_KEY = 'sk-83a84ea88cc34698b95357513cdffdf9'
dashscope.api_key = APP_KEY


class QWModel:
    frequency = 60
    def __init__(self, ui, api_refer_d, msg_trigger, output_trigger, requests_config, content_config, words, keys, model, proxy_type=None, proxy=None):
        self.ui = ui
        self.api_refer_d = api_refer_d
        self.msg_trigger = msg_trigger
        self.output_trigger = output_trigger
        self.requests_config = requests_config
        self.content_config = content_config
        self.words = words
        self.keys = keys
        self.model = model
        self.proxy_type = proxy_type
        self.proxy = proxy
        self.ban_words = []  # 违禁词
        # self.APP_KEY = 'sk-83a84ea88cc34698b95357513cdffdf9'
        # self.headers = {'Content-Type': 'application/json',
        #                 'Authorization': 'Bearer ' + self.APP_KEY}
        self.session = requests.session()
        # QWModel.frequency = int(self.api_refer_d[self.model]['frequency'])  # 更新为api返回的频率
        self.app_key_list = self.api_refer_d[self.model]['key'].split("\r\n")

        self.rate_limiter = RateLimiter(int(self.api_refer_d[self.model]['frequency']), 60)
        self.running_sign = True

    def main(self):
        self.get_ban_word()
        pool = ThreadPoolExecutor(max_workers=self.requests_config['threads'])
        # for word in self.words:
        words_l = self.ui.redis.r.lrange(f'{self.ui.main_page.username}_AiKeywordsQueue', 0, -1)

        # while self.ui.redis.r.llen(f'{self.ui.main_page.username}_AiKeywordsQueue'):             # 当redis中有值
        # for word in words_l:
        #     pool.submit(self.thread_wrapper, word)
        # pool.shutdown(wait=True)

        self.msg_trigger.emit("任务进程已结束", "", "")

    def thread_wrapper(self, word):
        if self.running_sign:
            self.ui.redis.r.lpop(f'{self.ui.main_page.username}_AiKeywordsQueue')         # 直接pop出队列
            print("pop出来的: ", word)
            title_l = self.get_title(word.strip().replace(" ", ""))
            try:
                for title in title_l:
                    status, res = self.get_content(title)
                    res_content = res['choices'][0]['message']['content']
                    res_content = self.sub_title_from_articles(res_content, title)
                    res_content = self.remove_p_label_and_ban_word(res_content)
                    if status:
                        if res.get('error'):
                            msg = f"关键词 {word} ->创作失败, 请重试。 错误信息: {res['error']['message']}。"
                            self.ui.redis.r.rpush(f'{self.ui.main_page.username}_AiKeywordsQueue', word)  # 失败的加入回去！
                        else:
                            msg = f"关键词 {word} ->创作完毕，已导出至文章文件夹中。"
                            self.output_trigger.emit(
                                word + self.content_config['front_sep'] + title.replace('"', "").strip() + self.content_config[
                                    'back_sep'], res_content)
                    else:
                        msg = f"关键词 {word} ->创作失败, 请重试。 错误信息: {res}。"
                        self.ui.redis.r.rpush(f'{self.ui.main_page.username}_AiKeywordsQueue', word)            # 失败的加入回去！
                    self.msg_trigger.emit(msg, word, title)
            except Exception as e:
                logging.error(e, exc_info=True)
            time.sleep(0.5)             # 强制线程睡眠0.5s 避免超频

    def sub_title_from_articles(self, article, origin_title):
        pattern = re.compile(r'(?=新标题：).*?(?=\n)')
        res_content = re.sub(pattern, '', article).strip()
        if origin_title in res_content.split("\n")[0] or '标题' in res_content.split("\n")[0]:
            return "\n".join(res_content.split("\n")[1:]).strip()
        return res_content.strip()

    def remove_p_label_and_ban_word(self, content):
        if self.requests_config.get('remove_p_label'):
            content = content.replace("<p>", '').replace("</p>", "")
        if self.requests_config.get('ban_word'):
            for ele in self.ban_words:
                content = content.replace(ele, "**")
        return content

    def get_ban_word(self):
        parent_id = self.ui.job_l[self.ui.comboBox.currentIndex()]['typeid']
        try:
            url = f'{self.ui.main_page.domain}/index.php?m=seoconfig&c=oauth&a=json_seoconfig_ke&sectorid={parent_id}&typeid=67'       # type_id=67为违禁词id
            self.ban_words = requests.get(url).json()
            self.ban_words = list(set(self.ban_words))
        except Exception as e:
            my_logger.error(e)
            self.ban_words = []

    def get_content(self, word):
        system_content = self.content_config['character_define'] if self.content_config['content_custom'] else 'assistant'
        user_content = self.content_config['content_sentence'].replace('{标题}', word) + f" 要求不少于{self.content_config['words_limit']}"
        messages = [{'role': 'system', 'content': system_content},
                    {'role': 'user', 'content': user_content}]
        status, res = self.api_request(messages)
        return status, res

    def get_title(self, word):
        return_titles_l = []
        if self.requests_config['running_choices'] == 1:
            user_content = self.content_config['double_title_sentence'].replace('{标题}', word)
        else:
            user_content = self.content_config['triple_title_sentence'].replace("{标题}", word)
        for i in range(self.requests_config['running_choices'] + 1):
            status, res = self.get_title_response(user_content)
            if status:
                if res.get('error'):
                    self.msg_trigger.emit(f"关键词 {word} ->创作失败, 请重试。 错误信息: {res['error']['message']}。", word, '')
                    self.ui.redis.r.rpush(f'{self.ui.main_page.username}_AiKeywordsQueue', word)  # 失败的加入回去！

                else:
                    new_title = res['choices'][0]['message']['content'].split("新标题:")[-1]
                    return_titles_l.append(new_title)
            else:
                self.msg_trigger.emit(f"关键词 {word} ->创作失败, 请重试。 错误信息: {res}", word, '')
                self.ui.redis.r.rpush(f'{self.ui.main_page.username}_AiKeywordsQueue', word)  # 失败的加入回去！

        return return_titles_l

    def get_title_response(self, title_sentence):
        system_content = self.content_config['character_define'] if self.content_config['title_custom'] else 'assistant'
        messages = [{'role': 'system', 'content': system_content},
                    {'role': 'user', 'content': title_sentence}]
        status, res = self.api_request(messages)
        return status, res

    def api_request(self, messages):
        if self.running_sign:
            # self.rate_limiter.wait()  # 在工作前调用wait方法来限制速率
            if self.rate_limiter.can_call():
                if self.requests_config['fail_attempt']:
                    attempt = self.requests_config['attempt']
                else:
                    attempt = 1
                for i in range(attempt):
                    if self.running_sign:
                        if self.app_key_list:
                            app_key = self.app_key_list[-1]
                            headers = {'Content-Type': 'application/json',
                                       'Authorization': 'Bearer ' + app_key}
                        else:
                            self.running_sign = False
                            return False, "无可用APP_KEY, 任务已终止"
                        url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
                        err = ""
                        data = {'model': self.model,
                                'messages': messages,
                                'seed': random.randint(1, 10000),
                                'result_format': 'message',
                                'app_key': app_key}
                        try:
                            self.rate_limiter.called()
                            response = self.session.post(url, headers=headers, data=json.dumps(data), proxies=self.proxy).json()
                        except Exception as e:
                            print(str(e))
                            err = str(e)
                            my_logger.error(e)
                        else:
                            if response.get('error') and response['error']['code'] == 'Arrearage':
                                if app_key in self.app_key_list:
                                    self.app_key_list.remove(app_key)
                                    self.msg_trigger.emit(f"检测到目标APP_KEY{app_key.replace(app_key[6:-4], '*'*len(app_key[6:-4]))}失效，失效原因: {response['error']['message']} 正在检测是否有可替换的APP_KEY...", '', '')
                                if self.app_key_list:
                                    self.msg_trigger.emit(f"已检测到新的APP_KEY, 正在应用APP_KEY...", '', '')
                                else:
                                    self.running_sign = False
                                    self.msg_trigger.emit(f"未检测到可用APP_KEY, 程序终止", '', '')
                                    return False, '任务已终止'
                            else:
                                return True, response
                    else:
                        return False, "任务已终止"
                return False, err
            else:
                time.sleep(10)
                return self.api_request(messages)
        else:
            return False, "任务已终止"


class QWCheckKey:
    def __init__(self, model_l, gpt, model, trigger, proxy_type=None, proxy=None):
        self.models_l = model_l
        self.gpt = gpt
        self.trigger = trigger
        self.model = model
        self.proxy_type = proxy_type
        self.proxy = proxy

    def main(self):
        # app_keys = list(set([self.models_l[ele]['key'] for ele in self.models_l]))
        app_keys = []
        # [self.models_l[ele]['key'].split("\r\n") for ele in self.models_l[0]]
        for k,  v_l in self.models_l.items():
            app_keys = v_l['key'].split("\r\n")
            break

        print("app keys: ", app_keys)
        for app_key in app_keys:
            if app_key:
                self.get_response(app_key)
            else:
                self.trigger.emit("未找到该AI模型的APP KEY！")

    def get_response(self, app_key):
        messages = [{'role': 'system', 'content': 'assistant'},
                    {'role': 'user', 'content': "test"}]            # 测试是否有连接

        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + app_key}

        url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
        data = {'model': self.model,
                'messages': messages,
                'seed': random.randint(1, 10000),
                'result_format': 'message',
                'app_key': app_key}
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data), proxies=self.proxy).json()
            print(response)
        except Exception as e:
            my_logger.error(e, exc_info=True)
            self.trigger.emit(f"连接失败")
        else:
            hidden_key = app_key[:].replace(app_key[7:-4], "*" * len(app_key[7:-4]))
            if response.get('error') and response['error']['code'] == 'Arrearage':
                self.trigger.emit(f"检测到{self.gpt} APP_KEY - {hidden_key} 已失效，请确认该账户余额")
            else:
                if response.get('error'):
                    self.trigger.emit(f"检测到{self.gpt} APP_KEY - {hidden_key} 已失效，请确认该账户是否可用，错误信息: {response['error']['message']}")
                else:
                    self.trigger.emit(f"{self.gpt} APP_KEY - {hidden_key} 可用")


class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = 0
        self.reset_time = time.time()

    def can_call(self):
        current_time = time.time()
        if current_time - self.reset_time > self.period:
            self.reset_time = current_time
            self.calls = 0
        return self.calls < self.max_calls

    def called(self):
        self.calls += 1
