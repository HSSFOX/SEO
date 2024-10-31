from unicodedata import name
import winreg
import requests
import json
import re
import zipfile
import os


class ChromeDriverDownloadDetect:
    def __init__(self, msg_trigger):
        # self.url = "https://registry.npmmirror.com/-/binary/chromedriver/"          # 镜像源
        # self.url = 'https://registry.npmmirror.com/binary.html?path=chrome-for-testing/'
        self.msg_trigger = msg_trigger
        self.url = 'https://registry.npmmirror.com/-/binary/chrome-for-testing/'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

    def detect_chrome_version(self):
        try:
            FullChromeVersion = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                                                   'SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome'),
                                                    'DisplayVersion')[0]
            ChromeVersion = FullChromeVersion.split('.')[0]
            print('Chrome version: ' + FullChromeVersion)
            return FullChromeVersion, ChromeVersion
        except Exception as e:
            try:
                # Software\Google\Chrome\BLBeacon
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
                version, types = winreg.QueryValueEx(key, 'version')
                print(version, types)
            except Exception as e:
                print("无法找到Chrome对应版本...")
                self.msg_trigger.emit("无法找到Chrome对应版本...")
            else:
                ChromeVersion = version.split('.')[0]
                return version, ChromeVersion
        return None, None

    def check_mirror_chromes(self):
        response = requests.get(self.url, headers=self.headers, verify=False)
        content = response.content.decode('utf8')
        contents = json.loads(content)
        names = []
        for i in contents:
            name = i['name']
            a = re.match('1', name)
            try:
                aa = a.group()
                if aa == '1':
                    names.append(name)
            except:
                continue
                # print('不存在')
                # print(name)
        return names

    def main(self):
        full_chrome_version, chrome_version = self.detect_chrome_version()
        if full_chrome_version and chrome_version:
            mirror_source_chrome_version = self.check_mirror_chromes()

            if full_chrome_version in mirror_source_chrome_version:           # 完整版本的在里边儿
                print('在里面', full_chrome_version)
                url = 'https://registry.npmmirror.com/-/binary/chrome-for-testing/{}/win64/chromedriver-win64.zip'.format(full_chrome_version)

                response = requests.get(url, headers=self.headers).content
                file_name = "{}.zip".format(chrome_version)
                file_name = str(file_name).replace("/", '')
                with open(file_name, 'wb') as f:
                    f.write(response)
            else:
                print('不在里面', chrome_version)
                for mirror_version in mirror_source_chrome_version:
                    if str(chrome_version) in mirror_version.split(".")[0]:
                        break
                else:
                    mirror_version = None
                if not mirror_version:
                    print("无匹配的Chrome版本")
                    return False
                url = 'https://registry.npmmirror.com/-/binary/chrome-for-testing/{}/win64/chromedriver-win64.zip'.format(mirror_version.strip("/"))
                print(url)

                response = requests.get(url, headers=self.headers).content
                file_name = "{}.zip".format(mirror_version)
                file_name = str(file_name).replace("/", '')
                print(file_name)
                with open(file_name, 'wb') as f:
                    f.write(response)
            self.un_zip(file_name)

    def un_zip(self, file_name):                # zip解压
        """unzip zip file"""
        zip_file = zipfile.ZipFile(file_name)
        if not os.path.isdir("config/"):
            os.mkdir("config/")
        for names in zip_file.namelist():
            zip_file.extract(names,"config/")
        zip_file.close()


if __name__ == '__main__':
    ChromeDriverDownloadDetect().main()