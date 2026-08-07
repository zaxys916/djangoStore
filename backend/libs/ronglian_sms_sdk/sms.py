# -*- coding:utf-8 -*-


try:
    from .SmsSDK import SmsSDK
except ImportError:
    from SmsSDK import SmsSDK

accId = '2c94811c9f3cb456019fda42accf2e73'
accToken = '3d532762002d4d57aef909c38d28aa36'
appId = '2c94811c9f3cb456019fda42ad4e2e7a'

def send_message():
    sdk = SmsSDK(accId, accToken, appId)
    datas = ('2233', '3')
    tid = '1'
    mobile = '17519190513'
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)


if __name__ == '__main__':
    send_message()
