# -------------------------------------------------------------------------------
# Copyright (c) 2023. 挥杯劝, Inc. All Rights Reserved
# @作者         : 挥杯劝(Huibq)
# @邮件         : huibq120@gmail.com
# @文件         : TrojanLinks - getlinks.py
# @创建时间     : 2023/11/30 16:09
# -------------------------------------------------------------------------------
from datetime import datetime
import requests
import random
import base64
import json
import os
from Telegram_bot import send_message

url = os.environ['trojan_url']


class Decode:
    @staticmethod
    def decode_link(my_link):
        try:
            my_link = json.loads(Decode.decode_base64(my_link))['c']
            sb = list(my_link[:-4])
            charAt = ord(my_link[-4]) - ord('A') + 1
            substring = my_link[-3:]
            if substring[0] == sb[11 % len(sb)] and substring[1] == sb[31 % len(sb)] and substring[2] == sb[61 % len(sb)]:
                for i in range(len(sb)):
                    if i % 3 == 2:
                        sb[i] = Decode.founction_l(sb[i], charAt - 1)
                for i in range(len(sb)):
                    if i & 1 == 1:
                        sb[i] = Decode.founction_r(sb[i], charAt)
                    else:
                        sb[i] = Decode.founction_l(sb[i], charAt)
                for i in range(len(sb) // 2):
                    if i & 1 == 1:
                        length = len(sb) - i - 1
                        sb[i], sb[length] = sb[length], sb[i]
                if len(sb) % 4 != 0:
                    length2 = 4 - len(sb) % 4
                    for _ in range(length2):
                        sb.append('=')
                return Decode.decode_base64(''.join(sb))
        except Exception as e:
            print(e)
        return "失败"

    @staticmethod
    def decode_base64(string):
        missing_padding = len(string) % 4
        if missing_padding:
            string += '=' * (4 - missing_padding)
        return base64.b64decode(string)

    @staticmethod
    def founction_l(c, i):
        i2 = i % 26
        if 'A' <= c <= 'Z':
            i3 = ord(c) - i2
            if i3 < 65:
                i3 += 26
            return chr(i3)
        elif 'a' <= c <= 'z':
            i4 = ord(c) - i2
            if i4 < 97:
                i4 += 26
            return chr(i4)
        else:
            return c

    @staticmethod
    def founction_r(c, i):
        i2 = i % 26
        if 'A' <= c <= 'Z':
            i3 = ord(c) + i2
            if i3 > 90:
                i3 -= 26
            return chr(i3)
        elif 'a' <= c <= 'z':
            i4 = ord(c) + i2
            if i4 > 122:
                i4 -= 26
            return chr(i4)
        else:
            return c


def getlink():
    try:
        headers = {"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; MI 8 MIUI/20.9.4)"}
        response = requests.get(url, headers=headers)
        return response.text
    except Exception as e:
        print(e)
    return None


def main():
    try:
        links = getlink()
        links = Decode.decode_link(links).decode('utf-8')
        data = json.loads(links)['h']
        sb = []
        for link in data:
            sb.append("trojan://")
            sb.append(link['b'])
            sb.append("@")
            sb.append(link['a'])
            sb.append(":")
            port = link['c']
            result = int(random.random() * len(port))
            sb.append(str(port[result]))
            sb.append("?security=tls&alpn=h2,http/1.1&type=tcp&sni=www.myethblog.com&headerType=none#")
            sb.append(link['d'] + '|Github搜索TrojanLinks')
            sb.append("\n")
        trojan_links = base64.b64encode((''.join(sb)).encode('utf-8')).decode()
        with open("./links/trojan", "w") as f:
            f.write(trojan_links)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
    message = '#trojan ' + '#订阅' + '\n' + datetime.now().strftime("%Y年%m月%d日%H:%M:%S") + '\n' + 'Trojan订阅已更新：' + '\n' + 'https://raw.github.com/Huibq/TrojanLinks/master/links/trojan'
    send_message(os.environ['chat_id'], message, os.environ['bot_token'])
