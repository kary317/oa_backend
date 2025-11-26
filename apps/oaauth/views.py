from rest_framework.views import APIView
from .serializers import LoginSerializer, OAUserSerializer
from rest_framework.response import Response
from rest_framework import status
import datetime

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
