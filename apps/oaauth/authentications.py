import jwt
import time
from django.conf import settings
from rest_framework.authentication import TokenAuthentication, BaseAuthentication, get_authorization_header
from rest_framework import exceptions

from .models import OAUser


def generate_jwt(user):
    timestamp = int(time.time()) + 60 * 60 * 24 * 7
    token = jwt.encode({'user_id': user.pk, 'exp': timestamp}, settings.SECRET_KEY, algorithm='HS256')
    return token


class UserTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return request._request.user, request._request.auth


class JWTAuthentication(BaseAuthentication):
    keyword = 'JWT'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Authorization头不可用'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Authorization格式不对'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')

            try:
                user_id = payload.get('user_id')
                user = OAUser.objects.get(pk=user_id)
                return (user, None)
            except:
                msg = '用户不存在'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        except jwt.ExpiredSignatureError:
            msg = 'token过期了'
            raise exceptions.AuthenticationFailed(msg)

        except:
            msg = '未知的错误'
            raise exceptions.AuthenticationFailed(msg)
