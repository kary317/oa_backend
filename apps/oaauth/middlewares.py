import jwt
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
from rest_framework.status import HTTP_403_FORBIDDEN

from rest_framework.authentication import get_authorization_header

OAUser = get_user_model()


class LoginCheckMiddleware(MiddlewareMixin):
    keyword = 'JWT'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 开放url白名单
        self.white_list = ('/auth/register/', '/auth/login/')

    def process_request(self, request):
        if request.path in self.white_list:
            # if request.path == '/auth/login/':
            request.user = AnonymousUser()
            request.auth = None
            return None

        try:
            auth = get_authorization_header(request).split()

            if not auth or auth[0].lower() != self.keyword.lower().encode():
                raise exceptions.ValidationError('请传入JWT!')

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
                    request.user = user
                    request.auth = token
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
        except Exception as e:
            print(e)
            return JsonResponse({'detail': '请先登录!'}, status=HTTP_403_FORBIDDEN)
