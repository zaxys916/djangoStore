from QQLoginTool import OAuthQQ
from django.views import View
from django.conf import settings
from django.http import JsonResponse

# Create your views here.
# 生成用户绑定链接
class QQLoginURLView(View):
    """
    QQ登录视图
    """
    def get(self, request):
        """
        生成用户绑定链接
        client_id=settings.QQ_CLIENT_ID, # 客户端ID
        client_secret=settings.QQ_CLIENT_SECRET, # 客户端密钥
        redirect_uri=settings.QQ_REDIRECT_URI, # 重定向URI
        state=None # 状态参数
        """
        qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID, 
        client_secret=settings.QQ_CLIENT_SECRET, 
        redirect_uri=settings.QQ_REDIRECT_URI, 
        state=None)
        qq_login_url = qq.get_login_url()
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'login_url': qq_login_url})

from apps.qq_oauth.models import OAuthQQUser
from django.contrib.auth import login
class QQAuthURLView(View):
    """
    QQ登录授权视图
    """
    def get(self, request):
        """
        获取QQ登录用户的openid
        """
        code = request.GET.get('code')
        if not code:
            return JsonResponse({'code': 400, 'errmsg': 'code不能为空'})
        qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID, 
        client_secret=settings.QQ_CLIENT_SECRET, 
        redirect_uri=settings.QQ_REDIRECT_URI, 
        state=None)
        token = qq.get_access_token(code)
        openid = qq.get_open_id(token)
        
        # 检查用户是否绑定
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '用户未绑定', 'openid': openid})
        else:
            # 登录用户
            user = qquser.user
            login(request, user)
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            
            response.set_cookie('username', user.username, max_age=14*24*3600)

            return response

import json
from django.contrib.auth import login
from apps.qq_oauth.models import OAuthQQUser
from apps.users.models import User

class OauthQQView(View):
    """
    QQ用户视图
    """
    def poset(self, request):
        """
        获取QQ用户信息
        """
        data = json.loads(request.body)
        mobile = data.get('mobile')
        password = data.get('password')
        sms_code = data.get('sms_code')
        openid = data.get('access_token')

        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)
            # 绑定QQ用户
            OAuthQQUser.objects.create(user=user, openid=openid)
            login(request, user)
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('username', user.username, max_age=14*24*3600)
            return response
        else:
            return JsonResponse({'code': 400, 'errmsg': '用户已绑定，请直接登录！'})
            
