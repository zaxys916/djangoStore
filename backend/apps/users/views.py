from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import User

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
            return JsonResponse({'code': 1, 'count': 0, 'msg': '数据库异常'})
        return JsonResponse({'code': 0, 'count': count})
