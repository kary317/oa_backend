from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.views import View
from django.shortcuts import render
from django.http.response import JsonResponse

from apps.oaauth.models import OADepartment, UserStatusChoice
from apps.oaauth.serializers import DepartmentSerializer
from .serializers import AddStaffSerializer, ActiveStaffSerializer
from utils import aeser
from oa_backend.celery import debug_task
from .tasks import send_mail_task

OAUser = get_user_model()
aes = aeser.AESCipher(settings.SECRET_KEY)


class DepartmentListView(ListAPIView):
    queryset = OADepartment.objects.all()
    serializer_class = DepartmentSerializer


# 激活员工邮箱
# 激活员工的过程：
# 1. 用户访问激活的链接的时候，会返回一个含有表单的页面，视图中可以获取到token，为了在用户提交表单的时候，post函数中能知道这个token
# 我们可以在返回页面之前，先把token存储在cookie中
# 2. 校验用户上传的邮箱和密码是否正确，并且解密token中的邮箱，与用户提交的邮箱进行对比，如果都相同，那么就是激活成功
# class ActiveStaffView(APIView):
class ActiveStaffView(View):
    # 获取激活页面
    def get(self, request):
        token = request.GET.get('token')
        response = render(request, 'active.html')
        response.set_cookie('token', token)
        return response

    # 激活员工
    def post(self, request):
        try:
            token = request.COOKIES.get('token')
            email = aes.decrypt(token)
            serializer = ActiveStaffSerializer(data=request.POST)
            if serializer.is_valid():
                # 这种方式不可取，如果serializer.is_valid通过验证，应该直接从清洗数据中提取数据
                # form_email = request.POST.get('email')

                form_email = serializer.validated_data.get('email')
                user = serializer.validated_data.get('user')
                if email != form_email:
                    return JsonResponse({'code': 400, 'detail': '邮箱错误!'})

                user.status = UserStatusChoice.ACTIVED
                user.save()
                return JsonResponse({'code': 200, 'detail': ''})
            else:
                detail = list(serializer.errors.values())[0][0]
                return JsonResponse({'code': 400, 'detail': detail})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'detail': 'token错误!'})


class StaffView(APIView):
    # 获取员工列表
    def get(self, request):
        pass

    # 新增员工
    def post(self, request):
        # 如果用的是视图集，那么视图集会自动把request放到context中
        # 如果是直接继承自APIView，那么就需要手动将request对象传给serializer.context中
        serializer = AddStaffSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            realname = serializer.validated_data.get('realname')
            password = serializer.validated_data.get('password')

            # user = OAUser.objects.create(email=email, realname=realname)
            # user.set_password(password)
            # user.save()
            # 1. 保存用户数据
            user = OAUser.objects.create_user(email=email, realname=realname, password=password)
            department = request.user.department
            user.department = department
            user.save()

            # 2.发送激活邮件
            self.send_active_email(email)

            return Response()
        else:
            return Response({'detail': list(serializer.errors.values())[0][0]}, status=status.HTTP_400_BAD_REQUEST)

    # 发送激活邮件
    def send_active_email(self, email):
        token = aes.encrypt(email)

        # '/staff/active/?token='xxx'
        active_path = reverse('staff:active_staff') + '?token=' + token
        # 通过self.request.build_absolute_uri构建绝对路径url ==> http://127.0.0.1:8000/staff/active/?token='xxx'
        active_url = self.request.build_absolute_uri(active_path)

        message = f'请点击以下链接激活账号：{active_url}'

        subject = 'OA员工激活'
        # 发送一个链接，让用户点击这个链接后，跳转到激活的页面，才能激活。
        # 为了区分用户，在发送链接邮件中，该链接中应该要包含这个用户的邮箱
        # 针对邮箱要进行加密：AES加密
        # send_mail('OA员工激活', message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email])
        send_mail_task.delay(email, subject, message)


# 测试celery是否集成到django项目
class TestCeleryView(APIView):
    def get(self, request):
        # 用celery异步执行debug_task任务
        debug_task.delay()
        return Response({'detail': '测试celery成功'})
