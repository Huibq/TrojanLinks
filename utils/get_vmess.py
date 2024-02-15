# -------------------------------------------------------------------------------
# Copyright (c) 2024. 挥杯劝, Inc. All Rights Reserved
# @作者         : 挥杯劝(Huibq)
# @邮件         : huibq120@gmail.com
# @文件         : TrojanLinks - get_vmess.py
# @创建时间     : 2024/01/14 08:58
# -------------------------------------------------------------------------------
import base64
import json
import os
from urllib.parse import urlencode
import time
import requests
from datetime import datetime
import urllib3
from Crypto.Cipher import AES
from base64 import b64decode
from Telegram_bot import send_message

urllib3.disable_warnings()


def get_vmess():
    base_url = vmess_api
    url = base_url + urlencode(params)
    response = requests.get(url, headers=headers, timeout=10, verify=False)
    return response.text


def decrypt(cipher_text: str, key: str) -> str:
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, key.encode('utf-8'))
    decrypted_text = cipher.decrypt(b64decode(cipher_text))
    return decrypted_text.decode('utf-8').rstrip()


def get_address(ip):
    url = f'https://ip125.com/api/{ip}?lang=zh-CN'
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Cookie': '_ga=GA1.2.348223593.1668760697; _ga_XYJPKQNDKR=GS1.1.1669809730.4.1.1669809752.0.0.0; __gads=ID=e9cb6076c0188403-228d0f367edf00b9:T=1683097828:RT=1701660864:S=ALNI_MZoNQcRpP-66ZZidp6BAlct92mbOw; __gpi=UID=00000c011afd3f29:T=1683097828:RT=1701660864:S=ALNI_MZSTguCSNwyc6d4WgMIcm7m-Xepvg'
    }
    country_info = requests.get(url, headers=head).json()
    add = country_info['country'] + country_info['city']
    return add


if __name__ == "__main__":
    vemss_key = os.environ['vemss_key']
    vmess_name = os.environ['vmess_name']
    vmess_token = os.environ['vmess_token']
    vmess_code = os.environ['vmess_code']
    vemss_id = os.environ['vemss_id']
    vmess_api = os.environ['vmess_api']
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9.1.0; MI 9 MIUI/V9.5.6.0.OEACNFA)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    params = {'vip': 'false', 'proto': 'v4', 'platform': 'android', 'ver': '8.3.71125',
              'deviceid': vemss_id, 'unicode': vemss_id, 't': str(round(datetime.now().timestamp() * 1000)),
              'code': vmess_code, 'recomm_code': '', 'f': '2024-01-14',
              'install': '2024-01-14', 'token': vmess_token,
              'package': vmess_name, 'width': '362.72726', 'height': '770.1818',
              'apps': '1883c547acfdcce30ead290c2b149fca'}

    nodes = []
    for i in range(20):
        try:
            vmess_dict = json.loads(base64.b64decode(decrypt(get_vmess(), vemss_key)[8:]).decode())
            try:
                address = get_address(vmess_dict['add'])
            except Exception as e:
                print(e)
                address = vmess_dict['add']
            vmess_dict['ps'] = address + '|Github搜索TrojanLinks'
            nodes.append("vmess://" + base64.b64encode(json.dumps(vmess_dict).encode()).decode() + '\n')
        except Exception as e:
            print(e)
        time.sleep(3)

    vmess = ''.join(list(set(nodes)))
    with open("./links/vmess", "w") as f:
        f.write(base64.b64encode(vmess.encode()).decode())
    message = '#vmess ' + '#订阅' + '\n' + datetime.now().strftime("%Y年%m月%d日%H:%M:%S") + '\n' + 'vmess订阅每4小时自动更新：' + '\n' + 'https://raw.githubusercontent.com/Huibq/TrojanLinks/master/links/vmess'
    send_message(os.environ['chat_id'], message, os.environ['bot_token'])
