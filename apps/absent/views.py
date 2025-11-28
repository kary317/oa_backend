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
