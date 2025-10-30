# -------------------------------------------------------------------------------
# Copyright (c) 2024. 挥杯劝, Inc. All Rights Reserved
# @作者         : 挥杯劝(Huibq)
# @邮件         : huibq120@gmail.com
# @文件         : TrojanLinks - getvless.py
# @创建时间     : 2024/01/10 20:08
# -------------------------------------------------------------------------------
import json
import os
import time
import uuid
from datetime import datetime
import requests
import urllib3
from urllib.parse import urljoin, urlparse
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util.Padding import unpad
import base64
from Telegram_bot import send_message

urllib3.disable_warnings()

def _normalise_base(candidate: str) -> str:
    candidate = candidate.strip()
    if not candidate:
        raise ValueError("BASE_URL environment variable is set but empty")

    parsed = urlparse(candidate)
    if not parsed.scheme:
        candidate = f"https://{candidate.lstrip('/')}"
        parsed = urlparse(candidate)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("BASE_URL must contain a valid domain or host name")

    return f"{parsed.scheme}://{parsed.netloc}/"


def _resolve_base_url(api_url: str) -> str:
    env_base = os.environ.get("BASE_URL")
    if env_base:
        return _normalise_base(env_base)

    if api_url:
        try:
            return _normalise_base(api_url)
        except ValueError:
            parsed = urlparse(api_url)
            if parsed.scheme and parsed.netloc:
                return f"{parsed.scheme}://{parsed.netloc}/"

    raise ValueError("BASE_URL environment variable is not set and could not be derived from vless_api")


def invite(api_url: str):
    base_url = _resolve_base_url(api_url)
    url = urljoin(base_url, 'addRefereeToUserReferral/')
    headers = {
        'accept': 'application/json',
        'accept-charset': 'UTF-8',
        'cache-control': 'max-age=1800',
        'user-agent': 'Ktor client',
        'content-type': 'application/x-www-form-urlencoded',
        'content-length': '0',
        'accept-encoding': 'gzip'

    }
    number = 0
    while number < 3:
        Id = uuid.uuid4()
        data = {
            'uniqueId': Id,
            'referralCode': 'D4GOLG'
        }
        req = requests.post(url, data=data, headers=headers, verify=False)
        print(req.text)
        number += 1
        time.sleep(3)


def decrypt_rsa(data):
    key = RSA.importKey(base64.urlsafe_b64decode(private_key))
    cipher = PKCS1_OAEP.new(key)
    decrypted_message = cipher.decrypt(base64.b64decode(data))
    return decrypted_message.decode()


def decrypt_aes(key, data):
    key = MD5.new(key.encode()).digest()
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(base64.b64decode(data)), AES.block_size)
    return decrypted_data.decode()


def get_node():
    url = api
    header = {
        'authorization': authorization,
        'cache-control': 'no-cache',
        'accept': 'application/json',
        'accept-charset': 'UTF-8',
        'user-agent': 'Ktor client',
        'content-type': 'text/plain;charset=UTF-8',
        'content-length': '0',
        'accept-encoding': 'gzip'
    }
    req = requests.post(url, data=text, headers=header, verify=False).json()
    key = req['key']
    key = decrypt_rsa(key)
    node_info = decrypt_aes(key, req['data'])
    Vless = ''
    for server_list in json.loads(node_info):
        if server_list['servers']:
            for servers in server_list['servers']:
                if servers:
                    server = servers['server']
                    ip = servers['ip']
                    if ip:
                        url = f'https://ip125.com/api/{ip}?lang=zh-CN'
                        head = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
                            'Cookie': '_ga=GA1.2.348223593.1668760697; _ga_XYJPKQNDKR=GS1.1.1669809730.4.1.1669809752.0.0.0; __gads=ID=e9cb6076c0188403-228d0f367edf00b9:T=1683097828:RT=1701660864:S=ALNI_MZoNQcRpP-66ZZidp6BAlct92mbOw; __gpi=UID=00000c011afd3f29:T=1683097828:RT=1701660864:S=ALNI_MZSTguCSNwyc6d4WgMIcm7m-Xepvg'
                        }
                        country_info = requests.get(url, headers=head).json()
                        address = country_info['country'] + country_info['city']
                        a = server.split('@')
                        b = a[1].split(':')[1].split('#')
                        vless = a[0] + '@' + ip + ':' + b[0] + '#' + address + '|Github搜索TrojanLinks'
                        Vless += vless + '\n'
                    else:
                        print(server)
                else:
                    print(servers)
        else:
            print(server_list)
    with open("./links/vless", "w") as f:
        f.write(base64.b64encode(Vless.encode()).decode())


if __name__ == '__main__':
    api = os.environ['vless_api']
    private_key = os.environ['vless_private_key']
    authorization = os.environ['vless_authorization']
    text = os.environ['vless_text']
    invite(api)
    get_node()
    message = '#vless ' + '#订阅' + '\n' + datetime.now().strftime("%Y年%m月%d日%H:%M:%S") + '\n' + 'vless订阅每天自动更新：' + '\n' + 'https://raw.githubusercontent.com/Huibq/TrojanLinks/master/links/vless'
    send_message(os.environ['chat_id'], message, os.environ['bot_token'])
