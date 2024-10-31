# -*- coding: UTF-8 -*-

import re
import redis

# Redis配置
# REDIS_HOST = "192.168.110.110"
# REDIS_PORT = 6379
# REDIS_PASSWD = ""
# token过期时间(单位：秒)
EXPIRE_TIME = None
# bind 127.0.0.1
# port 6379
# timeout 65
import configparser


def set_init_values():
    config = configparser.ConfigParser()
    try:
        config.read('config/config.ini')  # 读取 config.ini 文件
        if config.has_section('RedisSetting'):
            REDIS_HOST = config.get('RedisSetting', 'host')
            REDIS_PORT = config.get('RedisSetting', 'port')
            REDIS_PASSWD = config.get('RedisSetting', 'password')
            return REDIS_HOST, REDIS_PORT, REDIS_PASSWD
        else:
            REDIS_HOST = '192.168.110.110'
            REDIS_PORT = '6379'
            REDIS_PASSWD = ''
            return REDIS_HOST, REDIS_PORT, REDIS_PASSWD
    except Exception as e:
        print(str(e))
        REDIS_HOST = '192.168.110.110'
        REDIS_PORT = '6379'
        REDIS_PASSWD = ''
        return REDIS_HOST, REDIS_PORT, REDIS_PASSWD

# REDIS_HOST, REDIS_PORT, REDIS_PASSWD = set_init_values()

REDIS_HOST, REDIS_PORT, REDIS_PASSWD = set_init_values()
class RedisDb:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, passwd=REDIS_PASSWD, SWITCH=True):
        # 建立数据库连接
        self.r = redis.Redis(
            host=host,
            port=port,
            password=passwd,
            decode_responses=True,           # get() 得到字符串类型的数据
            socket_timeout=3,
        )
        self.switch = SWITCH

    def handle_redis_token(self, key, value=None, expire=EXPIRE_TIME):
        if self.switch:
            try:
                if value:               # 如果value非空，那么就设置key和value，EXPIRE_TIME为过期时间
                    self.r.set(key, value, ex=expire)
                else:                   # 如果value为空，那么直接通过key从redis中取值
                    redis_token = self.r.get(key)
                    return redis_token
            except Exception as e:
                return None
        else:
            return None

    def delete_key(self, key):
        try:
            self.r.delete(key)
        except Exception as e:
            return None



if __name__ == '__main__':
    import json
    r = RedisDb()
    # r.delete_key('大帅逼_automatic_task_list')


    # r.handle_redis_token('test', json.dumps(d))
    # a = r.handle_redis_token('大帅逼_AiContentConfig')
    # a = r.handle_redis_token('大帅逼_automatic_task_list')
    a = r.handle_redis_token('大帅逼_automatic_jw_refer_d')

    print(a)