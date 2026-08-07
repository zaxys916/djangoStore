# 任务文件名必须叫tasks.py

from libs.ronglian_sms_sdk.sms import send_sms_code
from celery_tasks.main import app


# 任务装饰器
@app.task(name='celery_send_sms_code')
def celery_send_sms_code():
    # 发送短信验证码
    send_sms_code()
