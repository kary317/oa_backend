from rest_framework import viewsets
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status

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
        queryset = self.queryset.select_related('author').prefetch_related('reads', 'departments').filter(
            Q(public=True) | Q(departments=self.request.user.department) | Q(author=self.request.user))
        return queryset
        # for inform in queryset:
        #     inform.is_read = InformRead.objects.filter(inform=inform, user=self.request.user).exsits()
        # return queryset

    # 只允许删除当前登录用户本人的
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.uid == request.user.uid:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
