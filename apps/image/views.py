from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UploadImageSerializer


class UploadImageView(APIView):
    def post(self, request):
        serializer = UploadImageSerializer(data=request.data)
        if serializer.is_valid():
            pass
        else:
            print(serializer.errors)
            return Response({})
