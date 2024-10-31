# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import QApplication, QTableWidget, QMenu
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import os
import re
import random
import jieba as jb
import jieba.analyse as analyse
import json
import requests
import string
import collections
from api_requests.TokenAPI import Token
import datetime
import time
import markdown
from requests_toolbelt.multipart.encoder import MultipartEncoder
import base64
import re
import logging
from api_requests.TokenAPI import Token
true, false, null = True, False, None
from urllib.parse import urlsplit
import tldextract
import copy
import base64
import os
from ping3 import ping
import selenium
from selenium import webdriver
from api_requests.RedisAPI import RedisDb
import re
import base64
import json
import requests


def generate_random_string(length):
    # 字符集包括小写字母、大写字母和数字
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

for i in range(20):
    a = random.randint(5, 16)
    b = generate_random_string(a)
    print(b)