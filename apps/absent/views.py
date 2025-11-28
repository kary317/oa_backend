from django.shortcuts import render

# 1. 发起考勤（create）
# 2. 处理考勤（update）
# 3. 查看自己的考勤列表（list?who=my）
# 4. 查看下属的考勤列表（list?who=sub）

from rest_framework import viewsets
from rest_framework import mixins

from .models import Absent, AbsentType, AbsentStatusChoices
from .serializers import AbsentSerializer


class AbsentViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Absent
    serializer_class = AbsentSerializer

    def update(self, request, *args, **kwargs):
        # 默认情况下，如果要修改某一条数据，那么要把这个数据的序列化中指定的字段都上传
        # 如果想只修改一部分数据，那么可以在kwargs中设置partial为True
        # DRF 序列化器默认要求全字段提交与验证。通过设置 partial=True 可开启部分更新模式，此时仅验证所提交的字段。
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
