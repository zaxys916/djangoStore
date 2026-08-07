# -*- coding:utf-8 -*-
import os

try:
    from .SmsSDK import SmsSDK
except ImportError:
    from SmsSDK import SmsSDK

accId = os.environ.get('SMS_ACCID')
accToken = os.environ.get('SMS_ACCTOKEN')
appId = os.environ.get('SMS_APPID')

def send_message():
    sdk = SmsSDK(accId, accToken, appId)
    datas = ('2233', '3')
    tid = '1'
    mobile = os.environ.get('SMS_MOBILE')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)


if __name__ == '__main__':
    send_message()
