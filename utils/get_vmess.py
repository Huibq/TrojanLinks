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


def get_vmess(ii):
    params['area'] = ii
    base_url = vmess_api
    url = base_url + urlencode(params)
    response = session.get(url, verify=False, timeout=10)
    return response.text


def decrypt(cipher_text: str, key: str) -> str:
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, key.encode('utf-8'))
    decrypted_text = cipher.decrypt(b64decode(cipher_text))
    return decrypted_text.rstrip(b'\x00').decode('utf-8')


def getlist():
    node_list = []
    new_params = {'level': 2}
    del params['area']
    new_params.update(params)
    base_url = vmess_api2
    url = base_url + urlencode(new_params)
    response = session.get(url, verify=False, timeout=10).content
    alllist = json.loads(response)["res"]
    print(alllist)
    for i in range(len(alllist)):
        data = alllist[i]["data"]
        for x in data:
            if x:
                node_list.append(x["id"])
    return node_list


if __name__ == "__main__":
    vemss_key = os.environ['vemss_key']
    vmess_name = os.environ['vmess_name']
    vmess_token = os.environ['vmess_token']
    vmess_code = os.environ['vmess_code']
    recomm_code = os.environ['recomm_code']
    vemss_id = os.environ['vemss_id']
    vmess_api = os.environ['vmess_api']
    vmess_api2 = os.environ['vmess_api2']
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9.1.0; MI 9 MIUI/V9.5.6.0.OEACNFA)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    session = requests.Session()
    session.headers.clear()
    session.headers.update(
        headers
    )
    params = {'proto': 'v2', 'platform': 'android', 'ver': '4.1.12021', 'deviceid': vemss_id,
              'unicode': vemss_id, 't': str(round(datetime.now().timestamp() * 1000)),
              'code': vmess_code,
              'recomm_code': '', 'f': '2023-09-11', 'install': '2023-09-11',
              'token': vmess_token, 'package': vmess_name,
              'isvip': 'true', 'unlimit': 'true', 'apps': '2a6a1fc7bd66c9643075846c2d77bdd2', 'area': '2'}
    List = getlist()
    nodes = []
    for i in List:
        try:
            vmess_dict = json.loads(base64.b64decode(decrypt(get_vmess(i), vemss_key)[8:]).decode())
            vmess_dict['ps'] = 'Github搜索TrojanLinks'
            nodes.append("vmess://" + base64.b64encode(json.dumps(vmess_dict).encode()).decode() + '\n')
        except Exception as e:
            print(e)
        time.sleep(3)

    vmess = ''.join(list(set(nodes)))
    with open("./links/vmess", "w") as f:
        f.write(base64.b64encode(vmess.encode()).decode())
    message = '#vmess ' + '#订阅' + '\n' + datetime.now().strftime("%Y年%m月%d日%H:%M:%S") + '\n' + 'vmess订阅每天自动更新：' + '\n' + 'https://raw.githubusercontent.com/Huibq/TrojanLinks/master/links/vmess'
    send_message(os.environ['chat_id'], message, os.environ['bot_token'])
