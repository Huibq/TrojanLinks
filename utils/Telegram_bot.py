# -------------------------------------------------------------------------------
# Copyright (c) 2024. 挥杯劝, Inc. All Rights Reserved
# @作者         : 挥杯劝(Huibq)
# @邮件         : huibq120@gmail.com
# @文件         : TrojanLinks - Telegram_bot.py
# @创建时间     : 2024/01/17 8:20
# -------------------------------------------------------------------------------
from datetime import datetime
import requests


def send_message(chat_id, text, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.get(url, params=payload)
    return response.json()


if __name__ == '__main__':
    chat_id = ''
    bot_token = ''
    message = datetime.now().strftime("%Y年%m月%d日%H:%M:%S") + '\n' + 'Trojan订阅已更新：' + '\n' + 'https://raw.staticdn.net/Huibq/TrojanLinks/master/links/ss_with_plugin'
    send_message(chat_id, message, bot_token)



