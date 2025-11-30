from django.shortcuts import render

# 1. 发起考勤（create）
# 2. 处理考勤（update）
# 3. 查看自己的考勤列表（list?who=my）
# 4. 查看下属的考勤列表（list?who=sub）

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Absent, AbsentType, AbsentStatusChoices
from .serializers import AbsentSerializer, AbsentTypeSerializer
from .utils import get_responder
from apps.oaauth.serializers import OAUserSerializer


class AbsentViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Absent.objects.all()
    serializer_class = AbsentSerializer

    def update(self, request, *args, **kwargs):
        # 默认情况下，如果要修改某一条数据，那么要把这个数据的序列化中指定的字段都上传
        # 如果想只修改一部分数据，那么可以在kwargs中设置partial为True
        # DRF 序列化器默认要求全字段提交与验证。通过设置 partial=True 可开启部分更新模式，此时仅验证所提交的字段。
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        who = request.query_params.get('who')
        if who and who == 'sub':
            result = queryset.filter(responder=request.user)
        else:
            result = queryset.filter(requester=request.user)
        serializer = self.serializer_class(result, many=True)
        return Response(serializer.data)


# 获取请假类型API
class AbsentTypeView(APIView):
    def get(self, request):
        types = AbsentType.objects.all()
        serializer = AbsentTypeSerializer(types, many=True)
        return Response(data=serializer.data)


# 获取审批者API
class ResponderView(APIView):
    def get(self, request):
        responder = get_responder(request)
        # 如果序列化的对象是一个None，那么不会报错，而是返回一个包含除了主键外的所有字段的空字典,有默认值得用默认值
        """
        {
            "department": {
                "name": "",
                "intro": "",
                "leader": null,
                "manager": null
            },
            "last_login": null,
            "is_superuser": false,
            "realname": "",
            "email": "",
            "telephone": "",
            "is_staff": false,
            "status": null,
            "is_active": false
        }
        """
        serializer = OAUserSerializer(responder)
        return Response(data=serializer.data)
