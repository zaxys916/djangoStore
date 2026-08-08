# LoginRequiredMixin：返回重定向，因此重写dispatch方法，返回JSON响应
from django.contrib.auth.mixins import AccessMixin
from django.http import JsonResponse



class LoginRequiredJSONMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'code': 400, 'errmsg': '没有登录'})
        return super().dispatch(request, *args, **kwargs)



