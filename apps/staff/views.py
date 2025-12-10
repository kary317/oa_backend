from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from apps.oaauth.models import OADepartment
from apps.oaauth.serializers import DepartmentSerializer
from .serializers import AddStaffSerializer

OAUser = get_user_model()


class DepartmentListView(ListAPIView):
    queryset = OADepartment.objects.all()
    serializer_class = DepartmentSerializer


class StaffView(APIView):
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
            user = OAUser.objects.create_user(email=email, realname=realname, password=password)
            department = request.user.department
            user.department = department
            user.save()

            send_mail('OA员工激活', message='xxx', from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email])
            return Response()
        else:
            return Response({'detail': list(serializer.errors.values())[0][0]}, status=status.HTTP_400_BAD_REQUEST)
