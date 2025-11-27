from django.http import JsonResponse
from rest_framework.views import APIView
from .serializers import LoginSerializer, OAUserSerializer, ResetPwdSerializer
from rest_framework.response import Response
from rest_framework import status
import datetime
from rest_framework.permissions import IsAuthenticated

from .authentications import generate_jwt


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            user.last_login = datetime.datetime.now()
            user.save()
            token = generate_jwt(user)
            return Response({'token': token, 'user': OAUserSerializer(user).data}, status=status.HTTP_200_OK)
        else:
            error_detail = list(serializer.errors.values())[0][0]
            return Response({'detail': error_detail}, status=status.HTTP_400_BAD_REQUEST)


# class AuthenticateRequireView:
#     permission_classes = [IsAuthenticated]


class ResetPwdView(APIView):
    def post(self, request):
        # print(request)
        # print(request.user)
        serializer = ResetPwdSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            pwd = serializer.validated_data.get('pwd1')
            request.user.set_password(pwd)
            request.user.save()
            return Response({'detail': '密码修改成功'})
        else:
            error_detail = list(serializer.errors.values())[0][0]
            return Response({'detail': error_detail}, status.HTTP_400_BAD_REQUEST)
