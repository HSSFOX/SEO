import os

import os
import subprocess
import sys
import re
import argparse
import time
import logging
import datetime
import random
import copy
from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtCore import QStringListModel, Qt


site = ['nc3fitness.com|1|1|1|74#0', 'nc3fitne1231ss.com|1|1|1|74#0']
num = 4
prefix_len = 5
l = []
letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
while len(l) < num * len(site):
    s = ''.join(random.sample(letters, prefix_len))
    if s not in l:
        l.append(s)
print(l)
new_site = []
while site:
    url = site.pop()
    for _ in range(num):
        prefix = l.pop()
        new_site.append(f'{prefix}.{url}')
print(new_site)
