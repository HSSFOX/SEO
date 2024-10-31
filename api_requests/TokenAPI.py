import requests
import time
import hashlib


class Token:
    def __init__(self):
        self.BT_KEY = '123'
        self.LIFETIME = 86400  # 令牌的生命周期（秒）
        self.headers = {'Connection': 'close'}

    def generateToken(self, key):
        now_time = int(time.time()) + self.LIFETIME
        return {
            'request_token': hashlib.sha256((str(now_time) + hashlib.sha256(key.encode()).hexdigest()).encode()).hexdigest(),
            'request_time': now_time,
        }

    def HttpPostCookie(self, url, data, timeout=60):

        try:
            if data.get('model') == 'attachment':
                response = requests.post(url, data=data, timeout=timeout, files=data)
            else:
                response = requests.post(url, headers=self.headers, json=data, timeout=timeout)
            print("token response", response.text)
        except requests.exceptions.RequestException as e:
            print(f'Request error: {str(e)}')
            print(url, data)
            return {'msg': f'Request error {str(e)}'}
        return response.json()

    def sendPostRequestWithToken(self, url, token_data):
        return self.HttpPostCookie(url, token_data)

