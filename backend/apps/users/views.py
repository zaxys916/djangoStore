from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import User
import json
import re

# Create your views here.
# 判断用户名是否重复
class UsernameCountView(View):
    def get(self, request, username):
        """
        判断用户名是否重复
        """
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            # 👇 关键修改：把真实的错误信息返回给前端
            return JsonResponse({'code': 0 'count': 1, 'errmsg': f'数据库异常: {str(e)}'})
        
        return JsonResponse({'code': 0, 'count': count})

class RegisterView(View):

    def post(self, request):
        """
        注册用户
        """
        # 1. 获取前端传递的参数
        body_bytes = request.body
        body_str = body_bytes.decode('utf-8')
        body_dict = json.loads(body_str)

        # 2. 获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')

        # 3. 验证数据
        if not all([username, password, password2, mobile, allow]):
            # 有空值
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            # 用户名格式不正确
            return JsonResponse({'code': 400, 'errmsg': '用户名格式不正确'})
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,20}$', password):
            # ？=.* 表示至少有一个小写字母，至少有一个大写字母，至少有一个数字
            # 密码格式不正确
            return JsonResponse({'code': 400, 'errmsg': '密码格式不正确'})
        if password != password2:
            # 密码不一致
            return JsonResponse({'code': 400, 'errmsg': '密码不一致'})
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            # 手机号格式不正确
            return JsonResponse({'code': 400, 'errmsg': '手机号格式不正确'})
        if not allow:
            # 没有勾选用户协议
            return JsonResponse({'code': 0, 'errmsg': '请勾选用户协议'})

        # 4. 保存数据
        # 方式1：使用create方法
        # user = User.objects.create(username=username, password=password, mobile=mobile)
        # return JsonResponse({'code': 0, 'errmsg': '注册成功'})
        # 方式2：使用save方法
        # user = User(username=username, password=password, mobile=mobile)
        # user.save()
        # return JsonResponse({'code': 0, 'errmsg': '注册成功'})
        # 方式3：使用update_or_create方法
        # user, created = User.objects.update_or_create(username=username, defaults={'password': password, 'mobile': mobile})
        # return JsonResponse({'code': 0, 'errmsg': '注册成功'})
        # 方式4：使用bulk_create方法
        # users = [User(username=username, password=password, mobile=mobile) for username, password, mobile in zip(usernames, passwords, mobiles)]
        # User.objects.bulk_create(users)
        # return JsonResponse({'code': 0, 'errmsg': '注册成功'})
        # 方式5：使用create_user方法，会自动处理密码的加密，上面密码不会加密
        user = User.objects.create_user(username=username, password=password, mobile=mobile)
        return JsonResponse({'code': 0, 'errmsg': '注册成功'})