from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

'''
验证码
前端：
发送请求，携带uuid
后端：
接收携带uuid的请求，生成验证码，返回给前端
1. 创建验证码对象
2. 保存验证码到redis
3. 返回验证码图片
'''
# Create your views here.
class ImageCodeView(View):

    def get(self, request, uuid):
        from libs.captcha.captcha import Captcha
        
        # 1. 创建验证码对象
        text, image = Captcha.generate_captcha()
        # 2. 保存验证码
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex(uuid, 100, text)
        # 3. 返回验证码
        return HttpResponse(image, content_type='image/jpeg')

class SmsCodeView(View):

    def get(self, request, mobile):
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection('verify_codes')
        image_code_server = redis_conn.get(uuid)
        if image_code_server is None:
            return JsonResponse({'code': 400, 'errmsg': '图片验证码已过期'})

        # 数据类型转换
        if image_code_server.decode().lower() != image_code.lower():
            return JsonResponse({'code': 400, 'errmsg': '图片验证码错误'})
        # 检查短信验证码是否已发送
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag is not None:
            return JsonResponse({'code': 400, 'errmsg': '不要频繁发送短信'})

        from random import randint
        sms_code = "%04d" % randint(0, 9999)
        redis_conn.setex(mobile, 300, sms_code)
        redis_conn.setex('send_flag_%s' % mobile, 60, 1)
        from libs.ronglian_sms_sdk import send_sms
        res = send_sms(mobile, sms_code)
        if res['code'] != 0:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码发送失败'})
        return JsonResponse({'code': 0, 'sms_code': 'ok'})
