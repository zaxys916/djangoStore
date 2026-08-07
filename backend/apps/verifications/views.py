from django.shortcuts import render
from django.views import View

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