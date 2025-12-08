import os

from rest_framework.views import APIView
from rest_framework.response import Response
from shortuuid import uuid
from django.conf import settings

from .serializers import UploadImageSerializer


# 上传图片接口 返回信息需要遵循wangEditor要求
class UploadImageView(APIView):
    def post(self, request):
        serializer = UploadImageSerializer(data=request.data)
        if serializer.is_valid():
            # 获取图片对象
            file = serializer.validated_data.get('image')
            # 图片原名字
            old_filename = file.name
            # 生成随机的图片名字,借助os模块获取文件扩展名
            # os.path.splitext('abc.png') = ('abc', '.png')
            new_filename = uuid() + os.path.splitext(old_filename)[-1]
            path = settings.MEDIA_ROOT / new_filename
            try:
                with open(path, 'wb') as fp:
                    for chunk in file.chunks():
                        fp.write(chunk)
            except Exception:
                # 上传失败,wangEditor要求返回的信息
                return Response({
                    "errno": 1,  # 只要不等于 0 就行
                    "message": "图片保存失败!"
                })

            file_url = settings.MEDIA_URL + new_filename
            # 上传成功,wangEditor要求返回的信息
            return Response({
                "errno": 0,  # 注意：值是数字，不能是字符串
                "data": {
                    "url": file_url,  # 图片 src ，必须
                    "alt": "",  # 图片描述文字，非必须
                    "href": file_url  # 图片的链接，非必须
                }
            })

        else:
            print(serializer.errors)
            # 上传失败,wangEditor要求返回的信息
            return Response({
                'errno': 1,  # 只要不等于 0 就行
                'message': list(serializer.errors.values())[0][0]
            })
