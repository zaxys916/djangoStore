"""
URL configuration for djangoStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, register_converter
from utils.converters import UsernameConverter

# 必须在 import users/urls 之前注册 converter，
# 否则 users/urls.py 里的 <username:username> 解析时找不到 converter
register_converter(UsernameConverter, 'username')

from apps.users import urls as users_urls
from apps.verifications import urls as verifications_urls
from apps.qq_oauth import urls as qq_oauth_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(users_urls)),
    path('', include(verifications_urls)),
    path('', include(qq_oauth_urls)),
]
