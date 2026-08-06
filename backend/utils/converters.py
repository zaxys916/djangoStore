from django.urls import converters

# 自定义用户名转换器
class UsernameConverter:
    regex = r'^[a-zA-Z0-9_]{5,20}$'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value