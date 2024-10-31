import requests
import time
import logging

class CertificateApi:
    def __init__(self):
        self.token = '43369bcb1547f4fa56e00a8c26de8489'
        self.user = '3865176@qq.com'
        self.headers = {'Authorization': f'Bearer {self.token}:{self.user}',
                        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
                        }
        self.base_url = 'https://api.xwamp.com/'
        self.config = {'AccountInfo': '/api/user/Account/info',                         # 获取账号信息
                       'OrderList': '/api/user/Order/list',                             # 证书列表
                       'OrderApply': '/api/user/Order/apply',                           # 申请证书
                       'OrderDetail': '/api/user/Order/detail',                         # 证书详情
                       'SetOrderVerifyType': '/api/user/OrderDetail/setVerfyType',      # 设置证书类型
                       'SetOrderAutoRenew': '/api/user/OrderDetail/setRenew',           # 证书自动重申
                       'OrderVerify': '/api/user/OrderDetail/verify',                   # 证书验证
                       # 'SetOrderRenew': '/api/user/OrderDetail/setRenew',
                       'OrderDownload': '/api/user/OrderDetail/down',                   # 证书下载
                       }

    def common_request(self, method, params, payload, config):
        url = self.base_url + self.config[config]
        if method == 'GET':
            res = self.get_requests(url, params, payload)
        else:
            res = self.post_requests(url, params, payload)
        return res

    def get_requests(self, url, params, payload, timeout=60):
        default_failure_return = {"isOk": False,
                                  "isError": True,
                                  "data": {},
                                  'error': '请求失败！请确认账号请求是否已达上限或账号是否可用！'
                                  }
        for _ in range(3):
            try:
                res = requests.get(url, headers=self.headers, params=params, data=payload, timeout=timeout).json()
            except Exception as e:
                logging.error(e, exc_info=True)
                time.sleep(1)
            else:
                return res
        return default_failure_return

    def post_requests(self, url, params, payload, timeout=60):           # 防止之后更新到requests.POST
        default_failure_return = {"isOk": False,
                                  "isError": True,
                                  "data": {},
                                  'error': '请求失败！请确认账号请求是否已达上限或账号是否可用！'
                                  }
        for _ in range(3):
            try:
                res = requests.post(url, headers=self.headers, params=params, data=payload, timeout=timeout).json()
            except Exception as e:
                logging.error(e, exc_info=True)
                time.sleep(1)
            else:
                return res
        return default_failure_return

    def get_account_info(self, params={}, payload={}):

        return self.common_request('GET', params, payload, 'AccountInfo')

    def get_ca_list(self, params={}, payload={}):
        default_params = {'page': 1, 'sort': False}
        params = {**default_params, **params}
        return self.common_request('GET', params, payload, 'OrderList')

    def ca_detail(self, params={}, payload={}):
        return self.common_request('GET', params, payload, 'OrderDetail')

    def apply_ca(self, params={}, payload={}):
        default_params = {'acme': 1, 'algorithm': 'ECC', 'is_path': True, 'mark': ''}
        params = {**default_params, **params}
        return self.common_request('GET', params, payload, 'OrderApply')

    def set_ca_verify_type(self, params={}, payload={}):
        return self.common_request('GET', params, payload, 'SetOrderVerifyType')

    def ca_auto_renew(self, params={}, payload={}):
        default_params = {'is_renew': True}
        params = {**default_params, **params}
        return self.common_request('GET', params, payload, 'SetOrderAutoRenew')

    def ca_verify(self, params={}, payload={}):
        # 验证域名。
        # 1、不设置则验证全部。
        # 2、指定域名，id1;id2。如：434;13435;343232。当验证方式为自动HTTP代理时，用此方式。
        # 3、指定域名和验证方式，id1:http-01;id2:dns-01。如：252:http-01;2121:dns-01。当验证方式为手动验证时，用此方式。

        return self.common_request('GET', params, payload, 'OrderVerify')

    def ca_download(self, params={}, payload={}):
        default_params = {'day': 7, 'type': 'json'}
        params = {**default_params, **params}
        return self.common_request('GET', params, payload, 'OrderDownload')

