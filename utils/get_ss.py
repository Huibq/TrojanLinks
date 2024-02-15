# -------------------------------------------------------------------------------
# Copyright (c) 2024. 挥杯劝, Inc. All Rights Reserved
# @作者         : 挥杯劝(Huibq)
# @邮件         : huibq120@gmail.com
# @文件         : TrojanLinks - get_ss.py
# @创建时间     : 2024/02/14 22:22
# -------------------------------------------------------------------------------
import json
import os
import uuid
from datetime import datetime
import requests
import urllib3
from Crypto.Hash import MD5
from Crypto.Cipher import AES
import base64
import urllib.parse
from Telegram_bot import send_message

urllib3.disable_warnings()


def encode_url(input_str):
    return urllib.parse.quote(input_str, safe='')


class AESCipher:
    def __init__(self, key):
        md5_hash = MD5.new()
        md5_hash.update(key.encode('utf-8'))
        self.key = md5_hash.digest()

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=ss_iv.encode('utf-8'))
        encrypted_bytes, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
        return base64.b64encode(encrypted_bytes + tag).decode('utf-8')

    def decrypt(self, data):
        try:
            data_bytes = base64.b64decode(data.encode('utf-8'))
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=ss_iv.encode('utf-8'))
            decrypted_bytes = cipher.decrypt_and_verify(data_bytes[:-16], data_bytes[-16:])
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            print("Error during decryption:", e)
            return None


def encode(s):
    cipher = AESCipher(ss_key)
    return cipher.encrypt(s)


def decode(s):
    cipher = AESCipher(ss_key)
    return cipher.decrypt(s)


def get_address(ip):
    tap_url = f'https://ip125.com/api/{ip}?lang=zh-CN'
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Cookie': '_ga=GA1.2.348223593.1668760697; _ga_XYJPKQNDKR=GS1.1.1669809730.4.1.1669809752.0.0.0; __gads=ID=e9cb6076c0188403-228d0f367edf00b9:T=1683097828:RT=1701660864:S=ALNI_MZoNQcRpP-66ZZidp6BAlct92mbOw; __gpi=UID=00000c011afd3f29:T=1683097828:RT=1701660864:S=ALNI_MZSTguCSNwyc6d4WgMIcm7m-Xepvg'
    }
    country_info = requests.get(tap_url, headers=head).json()
    return country_info['query']


if __name__ == '__main__':
    ss_key = os.environ['ss_key']
    ss_iv = os.environ['ss_iv']
    userinfo = json.loads(os.environ['ss_userinfo'])
    userinfo['uuid'] = str(uuid.uuid4()).replace('-', '')
    encoded_str = encode_url(encode(json.dumps(userinfo, separators=(',', ':'), ensure_ascii=False)))
    text = requests.post(os.environ['ss_url'], data=f'value={encoded_str}', headers=json.loads(os.environ['ss_headers']), verify=False).text
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari'
    }
    ss = ''
    for line in base64.b64decode(requests.get(json.loads(decode(text))['data']['data']['token'][1], headers=headers, verify=False).text).decode('utf-8').split('\n')[3:-1]:
        domain = line.strip().split('@')[1].split(':')[0]
        ss += line.replace(domain, get_address(domain)).strip() + '|Github%E6%90%9C%E7%B4%A2TrojanLinks\n'
    with open("./links/ss", "w") as f:
        f.write(base64.b64encode(ss.encode()).decode())
    message = '#ss ' + '#订阅' + '\n' + datetime.now().strftime(
        "%Y年%m月%d日%H:%M:%S") + '\n' + 'ss订阅已更新：' + '\n' + 'https://raw.staticdn.net/Huibq/TrojanLinks/master/links/ss'
    send_message(os.environ['chat_id'], message, os.environ['bot_token'])
