from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings


def generate_access_token(openid):
    """
    生成保存用户数据的token
    :param openid:
    :return:
    """
    s = Serializer(settings.SECRET_KEY, 3600)
    data = {'openid': openid}
    token = s.dumps(data)
    # 将bytetoken转换成str
    return token.decode()

def check_access_token(access_token):
    """
    检查token并返回openid
    :param access_token:
    :return:
    """
    s = Serializer(settings.SECRET_KEY, 3600)
    try:
        data = s.loads(access_token)
    except Exception as e:
        return None
    else:
        return data.get('openid')