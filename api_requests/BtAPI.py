# -*- coding: UTF-8 -*-
import logging

import requests
import hashlib
import time
import json
import os
from urllib3 import encode_multipart_formdata


class Bt:
    def __init__(self, bt_panel=None, bt_key=None, proxy=None):
        # 初始化宝塔面板地址和API密钥
        self.BT_PANEL = bt_panel
        self.BT_KEY = bt_key
        self.proxy = proxy
        # 配置项
        self.config = {
            # 自定义处理类
            'Public_config': '/panel/public/get_public_config',  #: 读取面板设置
            'getSiteCat': '/site?action=get_site_types',  #: 获取站点分类列表
            'selectCat': '/datalist/data/get_data_list',  #: 获取站点选择分类列表
            'uploadFile': '/files?action=upload',  #: 文件上传
            'CopyFile': '/files?action=CopyFile',  #: 复制文件
            'UnZip': '/files?action=UnZip',  #: 解压
            'addSites': '/site?action=create_website_multiple',  #: 批量添加网站
            'newFile': '/files?action=CreateFile',  #: 新建文件
            'SaveFileBody': '/files?action=SaveFileBody',  #: 保存or修改文件or伪静态规则内容(保存文件内容)
            'DeleteFile': '/files?action=DeleteFile',  #: 删除文件
            'MvFile': '/files?action=MvFile',  #: 移动文件 or 重命名
            'setSiteType':'/site?action=set_site_type',
            'GetDirNew': '/files?action=GetDirNew',          # 搜索文件名
            'SetFileAccess': '/files?action=SetFileAccess',      # 设置文件权限
            'AddIpWhiteList': '/config?action=set_token',            # 添加ip至白名单
            'GetDir': '/files?action=GetDir',                    # 获取目录下所有文件/文件夹
            'GetData': '/data?action=getData',
            'AddSiteType': '/site?action=add_site_type',            # 添加分类
            'AddDatabase': '/database?action=AddDatabase',              # 添加Database
            'InputSql': '/database?action=InputSql',                    # 导入MYSQL
            'RemoveSitesType': '/site?action=remove_site_type',         # 删除网站分类
            'GetFileBody': '/files?action=GetFileBody',                 #
            'DownloadFile': '/files?action=DownloadFile',               # 下载 -> 加入到下载队列中
            'GetTaskList': '/task?action=get_task_lists',               # 获取下载队列
            'SetToken': '/config?action=set_token',                     # 更新Key
            'GetCertList': '/ssl?action=get_cert_list',                 # SSL证书
            'GetSiteDomains': '/site?action=GetSiteDomains',            # 获取一个域名下的子域名
            'ApplyCertApi': '/acme?action=apply_cert_api',              # 申请SSL证书
            'GetRedirectList': '/site?action=GetRedirectList',          # 获取重定向列表
            'CreateRedirect': '/site?action=CreateRedirect',            # 创建重定向表
        }

    def get_key_data(self):
        # 构造带有签名的关联数组
        now_time = int(time.time())
        p_data = {
            'request_token': hashlib.md5(
                (str(now_time) + hashlib.md5(self.BT_KEY.encode()).hexdigest()).encode()).hexdigest(),
            'request_time': now_time
        }
        return p_data

    def http_post_cookie(self, url, data, timeout=60):
        # 发起POST请求
        header = {}
        header['Accept'] = '*/*'
        header['Accept-Language'] = 'zh-CN,zh;q=0.9'
        # header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        # header['Referer'] = 'https://45.204.112.33:40542/files'
        # header['x-http-token'] = '50YAv15zrLrwPldcs81ttitQTpVx8eAK2hP1XjE2llsXfveE'
        # header['Cookie'] = '9e55720616a43daad26ac134d21b75a0=014ac2d4-fcbd-4f7e-a25c-9ddd9660327f.HvcV6t5lQ_mTmsWcF042mOnyEiE; sites_path=/www/wwwroot; serverType=nginx; distribution=; pro_end=-1; ltd_end=-1; force=0; serial_no=; load_type=null; load_page=1; load_search=phpMyadmin; commandInputViewUUID=rcSAYFWRNSPraNi; pnull=1not_load; rank=list; record_paste=null; record_paste_type=null; Path=/www/server/panel/vhost/rewrite'

        for i in range(3):
            try:
                response = requests.post(url, headers=header, data=data, files=data, timeout=timeout, verify=False)
                print(33333, response.text)
            except Exception as e:
                time.sleep(0.5)
                logging.error(e)
            else:
                return response.text

        # 解析JSON数据
        return str({'status': False, 'msg': f'宝塔请求失败 url: {url} 请检查网络或者域名是否解析！'})

    def common_request(self, params, config, default_params, preprocess=None):
        # 通用请求处理
        try:
            params = {**default_params, **params}
            if preprocess:
                params = preprocess(params)
            url = self.BT_PANEL + self.config[config]
            result = self.http_post_cookie(url, {**self.get_key_data(), **params})
            # print(result.text)
            return json.loads(result)
        except Exception as e:
            return {'error': str(e)}

    #################################"""方法"""#################################
    def get_public_config(self, params={}):
        print("真跑这里啊？")
        """读取面板设置"""
        return self.common_request(params, "Public_config", {})

    def get_site_cat(self, params={}):
        print("寄")
        """获取网站分类"""
        return self.common_request(params, "getSiteCat", {})

    def set_site_type(self, params={}):
        """获取网站分类"""
        default_params = {'site_ids': [], 'id': 0}
        params = {**default_params, **params}
        return self.common_request(params, "setSiteType", {})

    def select_cat(self, params={}):
        """选取网站分类"""
        default_params = {'page': 1, 'limit': 100, 'search': '', 'type': '-1', 'table': 'sites'}
        params = {**default_params, **params}
        return self.common_request(params, "selectCat", default_params)

    def upload_file(self, params={}, cover=False):
        """上传文件"""
        default_params = {'f_path': '/www/wwwroot/', 'f_name': '', 'f_size': 0, 'f_start': 0, 'blob': ''}
        params = {**default_params, **params}
        if not cover:       # 如果不覆盖的话，检查是否已存在
            url = self.BT_PANEL + '/files?action=upload_file_exists'
            p_data = {**self.get_key_data(), 'filename': params['f_name']}
            data = json.loads(self.http_post_cookie(url, p_data))
            # 如果文件存在，取消上传任务
            if data['status']:
                return data
            url = self.BT_PANEL + self.config["uploadFile"]         # 不存在就继续上传
            params['blob'] = (params['f_name'], open(os.path.join(params['blob']), 'rb+'), 'application/octet-stream')
        else:
            url = self.BT_PANEL + self.config["uploadFile"]     # 直接上传
            params['blob'] = (params['f_name'], open(os.path.join(params['blob']), 'rb+'), 'application/octet-stream')
        return json.loads(self.http_post_cookie(url, {**self.get_key_data(), **params}))

    def upload_file_dir(self, params={}):
        """上传文件"""
        default_params = {'f_path': '/www/wwwroot/', 'f_name': '', 'f_size': 0, 'f_start': 0, 'blob': ''}
        params = {**default_params, **params}

        url = self.BT_PANEL + self.config["uploadFile"]     # 直接上传
        # params['blob'] = (params['f_name'], open(os.path.join(params['blob']), 'rb+'), 'application/octet-stream')
        return json.loads(self.http_post_cookie(url, {**self.get_key_data(), **params}))

    def copy_file(self, params={}):
        """复制文件"""
        return self.common_request(params, "CopyFile", {'sfile': '', 'dfile': ''})

    def set_file_access(self, params={}):
        default_params = {'filename': '', 'user': '', 'access': '', 'all': True}
        params = {**default_params, **params}
        # print(11111111111, params)
        return self.common_request(params, "SetFileAccess", params)


    def unZip(self, params={}):
        """压缩包解压"""
        default_params = {'sfile': '', 'dfile': '', 'type': 'zip', 'coding': 'UTF-8', 'password': ''}
        params = {**default_params, **params}
        return self.common_request(params, "UnZip", default_params)

    def add_sites(self, params={}):
        """批量添加网站"""
        default_params = {'websites_content': '', 'create_type': 'txt'}
        params = {**default_params, **params}
        # params['websites_content'] = params['websites_content'].replace("\\", "")
        return self.common_request(params, "addSites", default_params)

    def search_file(self, params={}):
        default_params = {'p': '1', 'showRow': '2000', 'path': '/www/wwwroot', 'sort': '', 'reverse': True}
        # all为True 包括子目录, False不包括
        params = {**default_params, **params}
        # params['websites_content'] = params['websites_content'].replace("\\", "")
        return self.common_request(params, "GetDirNew", default_params)

    def new_file(self, params={}):
        """新建文件"""
        default_params = {'path': '/www/wwwroot/', 'file_name': '123.txt'}
        params = {**default_params, **params}
        params['path'] = params['path'] + params['file_name']
        del params['file_name']
        return self.common_request(params, "newFile", default_params)

    def save_file_body(self, params={}):
        """保存伪静态规则内容(保存文件内容or修改内容)"""
        return self.common_request(params, "SaveFileBody",
                                   {'path': '/www/wwwroot/123.txt', 'data': '123', 'encoding': 'utf-8',
                                    'force': 0})

    def delete_file(self, params={}):
        """删除文件"""
        return self.common_request(params, "DeleteFile", {'path': ''})

    def move_file(self, params={}):
        """移动文件 or 重命名"""
        default_params = {'sfile': '', 'dfile': ''}
        params = {**default_params, **params}
        params['rename'] = params.get('rename', True)
        return self.common_request(params, "MvFile", default_params)

    def add_ip_white_list(self, params={}):
        default_params = {'t_type': '3', 'limit_addr': ''}
        params = {**default_params, **params}
        return self.common_request(params, "AddIpWhiteList", {})

    def get_dir_files(self, params={}):
        default_params = {'p': '1', 'showRow': '500', 'path': '', 'file_btn': True}
        params = {**default_params, **params}
        return self.common_request(params, "GetDir", default_params)

    def get_db_data(self, params={}):
        default_params = {'p': '1', 'showRow': '500', 'table': 'databases', 'search': '', 'order': ''}
        params = {**default_params, **params}
        return self.common_request(params, "GetData", default_params)

    def add_site_type(self, params={}):
        default_params = {'name': ''}
        params = {**default_params, **params}
        return self.common_request(params, "AddSiteType", default_params)

    def add_database(self, params={}):
        default_params = {'name': '', 'db_user': '', 'password': '', 'dataAccess': '127.0.0.1', 'address': '127.0.0.1', 'codeing': 'utf8mb4',
                          'dtype': 'MySql', 'ps': '', 'sid': 0, 'listen_ip': '0.0.0.0/0', 'host': ''}
        params = {**default_params, **params}
        return self.common_request(params, "AddDatabase", default_params)

    def import_database(self, params={}):
        default_params = {'file': '', 'name': ''}
        params = {**default_params, **params}
        return self.common_request(params, "InputSql", default_params)

    def remove_sites_type(self, params={}):
        default_params = {'id': ''}
        params = {**default_params, **params}
        return self.common_request(params, "RemoveSitesType", default_params)

    def get_file_body(self, params={}):
        default_params = {'path': ''}
        params = {**default_params, **params}
        return self.common_request(params, "GetFileBody", default_params)

    def download_file(self, params={}):
        default_params = {'path': '', 'url': '', 'filename': ''}
        params = {**default_params, **params}
        return self.common_request(params, "DownloadFile", default_params)

    def get_task_list(self, params={}):
        default_params = {'status': '-3'}
        params = {**default_params, **params}
        return self.common_request(params, "GetTaskList", default_params)

    def reset_key(self, params={}):
        default_params = {'t_type': '1'}
        params = {**default_params, **params}
        return self.common_request(params, "SetToken", default_params)

    def get_cert_list(self, params={}):
        default_params = {'search_limit': '0', 'search_name': '', 'force_refresh': '0'}
        params = {**default_params, **params}
        return self.common_request(params, "GetCertList", default_params)

    def get_sites_domain(self, params={}):
        default_params = {'id': '0'}
        params = {**default_params, **params}
        return self.common_request(params, "GetSiteDomains", default_params)

    def apply_cert_api(self, params={}):
        default_params = {'id': '0', 'auth_type': 'http', 'auth_to': '', 'auto_wildcard': '1'}
        params = {**default_params, **params}
        return self.common_request(params, "ApplyCertApi", default_params)

    def get_redirection_list(self, params={}):
        default_params = {'sitename': ''}
        params = {**default_params, **params}
        return self.common_request(params, "GetRedirectList", default_params)

    def create_redirection_list(self, params={}):
        default_params = {'type': '1', 'holdpath': '1', 'domainorpath': '', 'redirecttype': '', 'tourl': '', 'redirectdomain': [], 'sitename': '', 'redirectname': str(int(time.time() * 1000))}
        params = {**default_params, **params}
        return self.common_request(params, "CreateRedirect", default_params)





if __name__ == "__main__":
    from urllib.parse import urlparse
    from urllib import parse
    # bt = Bt(bt_panel="http://61.136.101.157:32462", bt_key="wYkz071PHgru5OUQBfKVBxfVa1tT6Vj9")
    bt = Bt('http://1.13.160.70:36800', 'xsJeTajXsNtckZSD8k0ryx3SFEa0HWcY')
    bt = Bt('https://45.204.112.33:40542', '9jb6UIWXjortYeNCJO0JJPD8r8WLkKci')
    # path = '/www/server/panel/vhost/rewrite/' + 'nc3fitness.com' + '.conf'
    path = '/www/wwwroot/nc3fitness.com/404.html'
    path = '/www/wwwroot/nc3fitness.com/caches/configs/database.php'
    # params = {'path': parse.quote_plus(path)}
    params = {'path': path}
    # params = {'path': '%2Fwww%2Fwwwroot%2Fnc3fitness.com%2Fcaches%2Fconfigs%2Fdatabase.php'}

    data = '''location / {
	###以下为PHPCMS Nginx伪静态化rewrite法则
	##栏目
  	rewrite ^(.*)/([0-9A-Za-z_]*)/$ $1/index.php?m=content&c=index&a=lists&catdir=$2;
	rewrite ^(.*)/([0-9A-Za-z_]*)/list_([0-9]+)\.html$ $1/index.php?m=content&c=index&a=lists&catdir=$2&page=$3;
	##内容
	rewrite ^(.*)/([0-9A-Za-z_]*)/([0-9]+)\.html$ $1/index.php?m=content&c=index&a=show&catdir=$2&id=$3;
#	rewrite ^(.*)/([0-9A-Za-z_]*)/([0-9]+)_([0-9]+)\.html$ $1/index.php?m=content&c=index&a=show&catdir=$2&id=$3&page=$4;
	##sitemap
  	rewrite ^(.*)sitemap.xml$ $1/index.php?m=admin&c=sitemap&a=sitemap;
	rewrite ^(.*)sitemap_([0-9]+)\.xml$ $1/index.php?m=admin&c=sitemap&a=sitemap&modelid=$2;
	##标签伪静态
    rewrite ^(.*)/tags/$ $1/index.php?m=content&c=tag;
    rewrite ^(.*)/tags/p([0-9]+)/$ $1/index.php?m=content&c=tag&a=init&page=$2;
    rewrite ^(.*)/tags/([0-9]+)\.html$ $1/index.php?m=content&c=tag&a=lists&id=$2;
    rewrite ^(.*)/tags/([0-9]+)-([0-9]+)\.html$ $1/index.php?m=content&c=tag&a=lists&id=$2&page=$3;
    
}'''
    # params = {'data': '12312', 'encoding': 'utf-8', 'path': path, 'force': 1}
    # params = {'data': '12312', 'encoding': 'utf-8', 'path': path}

    print(params)
    res = bt.get_file_body(params)
    print(11111, res)
    # url = self.BT_PANEL + self.config["uploadFile"]  # 直接上传
    # params['blob'] = (params['f_name'], open(os.path.join(params['blob']), 'rb+'), 'application/octet-stream')


