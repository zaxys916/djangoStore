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
            # 👇 关键修改：把真实的错误信息返回给前端
            return JsonResponse({'code': 200, 'count': 0, 'errmsg': f'数据库异常: {str(e)}'})
        
        return JsonResponse({'code': 0, 'count': count})

