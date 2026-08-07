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
            return JsonResponse({'code': 0, 'count': 1, 'errmsg': f'数据库异常: {str(e)}'})
        
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


        # 使用create_user方法，会自动处理密码的加密，上面密码不会加密
        user = User.objects.create_user(username=username, password=password, mobile=mobile)
        
        # 用户状态保持
        # 设置session
        # request.session['user_id'] = user.id
        # request.session.save()

        # 使用django自带的登录方法
        from django.contrib.auth import login
        login(request, user)
        
        return JsonResponse({'code': 0, 'errmsg': '注册成功'})


class loginView(View):
    def post(self, request):
        """
        用户登录
        """
        # 1. 获取前端传递的参数
        body_bytes = request.body
        body_str = body_bytes.decode('utf-8')
        body_dict = json.loads(body_str)

        # 2. 获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        remember = body_dict.get('remember')

        # 3. 验证数据
        if not all([username, password]):
            # 有空值
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})

        # 4.验证账号密码
        from django.contrib.auth import authenticate
        # 返回用户对象，如果验证失败，返回None
        user = authenticate(username=username, password=password)

        # 多种登录方式验证
        if re.match(r'^1[3-9]\d{9}$', username):
            # 账号格式正确
            User.USERNAME_FIELD = 'mobile'
        else:
            # 账号格式错误
            User.USERNAME_FIELD = 'username'

        if user is None:
            # 账号密码错误
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})
        
        # 5.状态保持
        from django.contrib.auth import login
        login(request, user)
        if remember is not None:
            # 0 表示关闭浏览器就过期
            # None 采取系统默认值，默认2周
            # 其他数据为秒数
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)
        
        return JsonResponse({'code': 0, 'errmsg': '登录成功'})
