# -------------------------------------------------------------------------------
# Copyright (c) 2024. 挥杯劝, Inc. All Rights Reserved
# @作者         : 挥杯劝(Huibq)
# @邮件         : huibq120@gmail.com
# @文件         : TrojanLinks - get_ovpn.py
# @创建时间     : 2024/01/17 08:55
# -------------------------------------------------------------------------------
import ast
import base64
import os
import random
import re
import string
import time
from base64 import b64encode, b64decode
import requests
from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad
from Telegram_bot import send_message
from datetime import datetime


def main():
    links_url = ovpn_api_1
    headers = {"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; MI 9 MIUI/20.9.4)", "version_name": f'{version}'}
    req = ast.literal_eval(requests.get(links_url, headers=headers).text)

    for link in req:
        time.sleep(2)
        try:
            url = ovpn_api_2
            url += f"?userId={ovpn_user}"
            url += f"&serverNumber={0}"
            key = k()
            url += "&key=" + e(key)
            url += f"&version={version}"
            data = g(url)
            config = d(data[0], key, data[1])
            ip_address = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', config)[0]
            url = f'https://ip125.com/api/{ip_address}?lang=zh-CN'
            head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
                'Cookie': '_ga=GA1.2.348223593.1668760697; _ga_XYJPKQNDKR=GS1.1.1669809730.4.1.1669809752.0.0.0; __gads=ID=e9cb6076c0188403-228d0f367edf00b9:T=1683097828:RT=1701660864:S=ALNI_MZoNQcRpP-66ZZidp6BAlct92mbOw; __gpi=UID=00000c011afd3f29:T=1683097828:RT=1701660864:S=ALNI_MZSTguCSNwyc6d4WgMIcm7m-Xepvg'
            }
            country_info = requests.get(url, headers=head).json()
            address = country_info['country'] + ip_address
            with open(f"./links/Openvpn/{address}.ovpn", "w") as conf:
                conf.write(base64.b64encode(config.encode()).decode())
        except Exception as E:
            print(E)


def g(url):
    headers = {"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; MI 9 MIUI/20.9.4)", "version_name": f'{version}'}
    response = requests.get(url, headers=headers)
    return response.text, response.headers.get('aesIV')


def k():
    return ''.join(random.choice(string.ascii_letters) for _ in range(16))


def e(message):
    rsa_key = RSA.importKey(b64decode(p))
    cipher = PKCS1_v1_5.new(rsa_key)
    encrypted_text = cipher.encrypt(message.encode())
    return b64encode(encrypted_text).decode()


def d(ciphertext, key, iv):
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    plaintext = unpad(cipher.decrypt(b64decode(ciphertext)), AES.block_size)
    return plaintext.decode()


def ra():
    url = ovpn_api_3
    header = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; MI 9 MIUI/20.9.4)"
    }
    req = requests.get(url, headers=header)
    print()
    return req.json()['rsa']


def a():
    url = ovpn_api_4
    headers = {
        'unique_id': ovpn_user,
        'tourist_id': '84385722',
        'unique_type': '2',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; MI 9 MIUI/V9.5.6.0.OEACNFA)',
        'Connection': 'Keep-Alive'
    }
    req = requests.get(url, headers=headers)
    print(req.text)


if __name__ == "__main__":
    version = '2.1.8.5'
    ovpn_api_1 = os.environ['ovpn_api_1']
    ovpn_api_2 = os.environ['ovpn_api_2']
    ovpn_api_3 = os.environ['ovpn_api_3']
    ovpn_api_4 = os.environ['ovpn_api_4']
    ovpn_user = os.environ['ovpn_user']
    p = ra()
    main()
    message = '#ovpn' + '\n' + datetime.now().strftime("%Y年%m月%d日%H:%M:%S") + '\n' + 'ovpn配置每天自动获取：' + '\n' + 'https://github.com/Huibq/TrojanLinks/tree/master/links/Openvpn'
    send_message(os.environ['chat_id'], message, os.environ['bot_token'])
