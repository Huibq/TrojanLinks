# -------------------------------------------------------------------------------
# Copyright (c) 2023. 挥杯劝, Inc. All Rights Reserved
# @作者         : 挥杯劝(Huibq)
# @邮件         : huibq120@gmail.com
# @文件         : TrojanLingks - ssr.py
# @创建时间     : 2023/12/07 16:36
# -------------------------------------------------------------------------------
import base64
import json
import os
import time
import uuid
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from binascii import hexlify, unhexlify
from datetime import datetime
import urllib3
from Telegram_bot import send_message

# 忽略证书警告
urllib3.disable_warnings()


class AESCipher:
    def __init__(self, key):
        self.key = key.encode()

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_ECB)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        ct = hexlify(ct_bytes).decode('utf-8')
        return ct

    def decrypt(self, ct):
        try:
            ct = unhexlify(ct)
            cipher = AES.new(self.key, AES.MODE_ECB)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt.decode('utf-8')
        except Exception as e:
            print(e)
            return "Incorrect decryption"


k = os.environ['key']
host = os.environ['host']
host_1 = os.environ['host_1']
host_2 = os.environ['host_2']

AESecb = AESCipher(k)
Id = str(uuid.uuid4()).replace("-", "")


def web():
    url = f'https://{host}/?share=MjExMDc1NDMTUBEVPN'
    headers = {
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 7.1.0; zh-cn; MI 9 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.5.5',
        'x-miorigin': 'b',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,en-US;q=0.8',
    }
    requests.get(url, headers=headers, verify=False)


def add_share():
    url = f'https://{host_1}/share/add_share'
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 7.1.0; zh-cn; MI 9 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.5.5',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'content-length': '0',
        'accept-encoding': 'gzip, deflate',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'origin': f'https://{host_1}',
        'referer': f'https://{host_1}/?share=MjExMDc1NDMTUBEVPN',
        'accept-language': 'zh-CN,en-US;q=0.8',
    }
    data = {
        'str': 'MjExMDc1NDMTUBEVPN'
    }
    req = requests.post(url, headers=headers, data=data, verify=False)
    print(req.text)


def get_login():
    url = f'https://{host_2}/node/getInformation_ex'
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.0; MI 6 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'content-length': '0',
        'accept-encoding': 'gzip',
    }
    text = f'{{"imei":"{Id}","platform":"android","version_number":46,"models":"MI 9","sdk":"30","m":"1572F5F911FFDF9028B4A2F763C310F0","c":4}}'
    value = AESecb.encrypt(text).upper()
    now = datetime.now()
    formatted_time = now.strftime("%Y年%m月%d日%H:%M:%S")
    data = {
        't': formatted_time,
        'value': value,
    }
    req = requests.post(url, headers=headers, data=data, verify=False)
    return req.json()['data']


if __name__ == '__main__':
    try:
        web()
        add_share()
        time.sleep(4)
        node_list = json.loads(AESecb.decrypt(get_login()))['goserverlist']
        SSR = ''
        for i in node_list:
            name = i['name'] + '|Github搜索TrojanLinks'
            host = i['host']
            remotePort = i['remotePort']
            password = i['password']
            protocol = i['protocol']
            protocol_param = i['protocol_param']
            obfs = i['obfs']
            method = i['method']
            nodeinfo = host + ':' + str(
                remotePort) + ':' + protocol + ':' + method + ':' + obfs + ':' + base64.urlsafe_b64encode(
                password.encode()).decode() + '/?' + f'obfsparam=&protoparam={base64.urlsafe_b64encode(protocol_param.encode()).decode().strip("=")}&remarks={base64.urlsafe_b64encode(name.encode()).decode().rstrip("=")}&group='
            ssr = 'ssr://' + base64.urlsafe_b64encode(nodeinfo.encode()).decode().rstrip("=")
            SSR += ssr + '\n'
            if i == node_list[19]:
                break
        with open("./links/ssr", "w") as f:
            f.write(base64.b64encode(SSR.encode()).decode())
    except Exception as E:
        print(E)
    message = '#ssr ' + '#订阅' + '\n' + datetime.now().strftime("%Y年%m月%d日%H:%M:%S") + '\n' + 'ssr订阅每天自动更新：' + '\n' + 'https://raw.githubusercontent.com/Huibq/TrojanLinks/master/links/ssr'
    send_message(os.environ['chat_id'], message, os.environ['bot_token'])
