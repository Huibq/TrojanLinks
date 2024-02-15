# -------------------------------------------------------------------------------
# Copyright (c) 2024. 挥杯劝, Inc. All Rights Reserved
# @作者         : 挥杯劝(Huibq)
# @邮件         : huibq120@gmail.com
# @文件         : TrojanLinks - get_ss_with_plugin.py
# @创建时间     : 2024/01/13 16:51
# -------------------------------------------------------------------------------
import base64
import json
import os
import random
from datetime import datetime
import requests
from Telegram_bot import send_message


def custom_encode(s):
    custom_charset = ss_key_1
    binary_string = ''.join(format(byte, '08b') for byte in s.encode('UTF-8'))
    while len(binary_string) % 8 != 0:
        binary_string += '0'
    padding_length = 0
    while len(binary_string) % 24 != 0:
        binary_string += '0'
        padding_length += 1
    encoded_string = ''
    for i in range(0, len(binary_string), 6):
        six_bit_segment = binary_string[i:i + 6]
        if int(six_bit_segment, 2) == 0 and i >= len(binary_string) - padding_length:
            encoded_string += '='
        else:
            encoded_string += custom_charset[int(six_bit_segment, 2)]
    return encoded_string


def a(s, object0):
    return s + str(object0)


def h(s, object0):
    return a(s, object0)


def binary_to_bytes(binary_str):
    return bytes(int(binary_str[i:i + 8], 2) for i in range(0, len(binary_str), 8))


def node_decrypt(base64str):
    c = "="
    d = ss_key_1
    v = len(base64str) - 1
    s1 = ""
    if v >= 0:
        v2 = 0
        while True:
            v3 = v2 + 1
            v4 = base64str[v2]
            if v4 != c[0]:
                s2 = format(d.find(v4), '06b')
                while len(s2) != 6:
                    s2 = h('0', s2)
                s1 = h(s1, s2)
            v2 = v3
            if v3 > v:
                break
    byte_data = binary_to_bytes(s1)
    try:
        return byte_data.decode('utf-8')
    except UnicodeDecodeError:
        return byte_data


def get_node():
    rand = str(random.randint(0, 144470))
    url = ss_api_1
    info = f'{rand};{ss_key_2};{str(round(datetime.now().timestamp()))};{ss_key_3};15605292 '
    data = f'{"{"}"country":"MO","ac":4,"channel":"google","apiver":31,"it":{str(round(datetime.now().timestamp()) - 180)},"pkg":"{ss_str_1}","version":1675,"cpuabi":"arm64-v8a","rand":"{rand}","sig":"{custom_encode(info)}","uid":{userid},"lang":"ZH","vip":true,"device":{email}{"}"}'
    req = requests.post(url, data=custom_encode(data), headers=headers)
    return req.json()['data']


def register():
    data = f'{"{"}"email":"{email}@qq.com","password":"asd{email}","invite_user_id":1705362,"register_device":"{android_id}_{selected_model}","country":"CN","channel":"google","lang":"ZH","pkg":"com.kuto.vpn","device":"{email}","version":"1675"{"}"}'
    encoded = custom_encode(data)
    url = ss_api_2
    req = requests.post(url, headers=headers, data=encoded)
    return req.json()['data']['id']


if __name__ == '__main__':
    ss_key_1 = os.environ['ss_key_1']
    ss_key_2 = os.environ['ss_key_2']
    ss_key_3 = os.environ['ss_key_3']
    ss_api_2 = os.environ['ss_api_2']
    ss_api_1 = os.environ['ss_api_1']
    ss_str_1 = os.environ['ss_str_1']
    ss_str_2 = os.environ['ss_str_2']
    ss_str_3 = os.environ['ss_str_3']
    ss_str_4 = os.environ['ss_str_4']
    ss_str_5 = os.environ['ss_str_5']
    ss_str_6 = os.environ['ss_str_6']
    ss_str_7 = os.environ['ss_str_7']
    email = str(random.randint(10000000, 999999999))
    models = ['Redmi+5', 'LIO+AN00', 'PFEM10', 'MI+6', 'EVR+AL00', 'JKM+AL00b', 'COR+TL10', 'VCE+AL00',
              'HMA+AL00',
              'SKW+A0', 'M1813', 'CLT+AL01', 'Mi+4c', 'COL+AL10', 'HLK+AL10', 'SEA+AL10', 'OPPO+A79k',
              'vivo+X9s', 'MI+PLAY', 'OPPO+A57', 'V1916A', 'M1822', 'HUAWEIT+AL10', 'Redmi+5', 'CLT+TL01',
              'vivo+X21', 'JKM+AL00a']
    selected_model = random.choice(models)
    ID = '0123456789abcdef'
    android_id = ''
    for n in range(16):
        android_id = android_id + random.choice(ID)
    headers = {
        'User-Agent': f'Dalvik/2.1.0 (Linux; U; Android 9.1.0; {selected_model} MIUI/V9.5.6.0.OEACNFA)',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        userid = register()
        first = node_decrypt(get_node())
        second = json.loads(first[first.find(ss_str_2) + 9:first.find(ss_str_3) - 3].replace(r'\"', '"'))
        third = json.loads(first[first.find(ss_str_3) + 12:first.find(ss_str_4) - 3].replace(r'\"', '"'))
        ss = ''
        for node in third[1:]:
            ip = second[node["host"]]
            method = node["method"] + ':' + node['password'].replace(r'g12sQi#ss#\u00261', 'g12sQi#ss#&1')
            if node['plugin'] == ss_str_5:
                s_node = 'ss://' + base64.urlsafe_b64encode(method.encode()).decode() + '@' + ip + ':' + str(node[
                    'port']) + '?plugin=v2ray-plugin%3Bhost%3D' + ip + '#' + node['name'] + '|Github%E6%90%9C%E7%B4%A2TrojanLinks'
            elif node['plugin'] == ss_str_6:
                s_node = 'ss://' + base64.urlsafe_b64encode(method.encode()).decode() + '@' + ip + ':' + str(node[
                    'port']) + '?plugin=v2ray-plugin%3Bhost%3D' + node['cdn'].replace("@", "") + '%3Btls#' + node['name'] + '|Github%E6%90%9C%E7%B4%A2TrojanLinks'
            elif node['plugin'] == ss_str_7:
                s_node = 'ss://' + base64.urlsafe_b64encode(method.encode()).decode() + '@' + ip + ':' + str(node[
                    'port']) + '?plugin=obfs-local%3Bhost%3D' + ip + '#' + node['name'] + '|Github%E6%90%9C%E7%B4%A2TrojanLinks'
            else:
                s_node = 'ss://YWVzLTEyOC1nY206NTYzNTYzMg@1.1.1.1:80?plugin=obfs-local%3Bobfs%3Dhttp%3Bobfs-host%3D1.1.1.1#%E6%96%B0%E5%8D%8F%E8%AE%AE'
            ss += s_node + '\n'
        with open("./links/ss_with_plugin", "w") as f:
            f.write(base64.b64encode(ss.encode()).decode())
    except Exception as e:
        print(e)
    message = '#ss' + '\n' + datetime.now().strftime("%Y年%m月%d日%H:%M:%S") + '\n' + 'ss_with_plugin订阅每6小时自动更新：' + '\n' + 'https://raw.githubusercontent.com/Huibq/TrojanLinks/master/links/ss_with_plugin'
    send_message(os.environ['chat_id'], message, os.environ['bot_token'])
