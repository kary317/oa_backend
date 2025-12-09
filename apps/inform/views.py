from rest_framework import viewsets
from django.db.models import Q

from .models import Inform
from .serializers import InformSerializer


class InformViewSet(viewsets.ModelViewSet):
    queryset = Inform.objects.all()
    serializer_class = InformSerializer

    # 要获取的通知列表需满足以下条件：
    # 1. inform.public=True 通知是公开的
    # 2. inform.departments 包含了用户所在的部门
    # 3. inform.author = request.user 通知的作者是当前登录用户
    def get_queryset(self):
        queryset = self.queryset.prefetch_related('reads').filter(
            Q(public=True) | Q(departments=self.request.user.department) | Q(author=self.request.user))
        return queryset
        # for inform in queryset:
        #     inform.is_read = InformRead.objects.filter(inform=inform, user=self.request.user).exsits()
        # return queryset
