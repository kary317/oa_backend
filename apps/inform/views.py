from rest_framework import viewsets
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Inform, InformRead
from .serializers import InformSerializer, ReadInformSerializer


class InformViewSet(viewsets.ModelViewSet):
    queryset = Inform.objects.all()
    serializer_class = InformSerializer

    # 要获取的通知列表需满足以下条件：
    # 1. inform.public=True 通知是公开的
    # 2. inform.departments 包含了用户所在的部门
    # 3. inform.author = request.user 通知的作者是当前登录用户
    def get_queryset(self):
        queryset = self.queryset.select_related('author').prefetch_related('reads', 'departments').filter(
            Q(public=True) | Q(departments=self.request.user.department) | Q(author=self.request.user)).distinct()
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['read_count'] = InformRead.objects.filter(inform_id=instance.id).count()

        return Response(data=data)


# 阅读通知功能
class ReadInformView(APIView):
    def post(self, request):
        serializer = ReadInformSerializer(data=request.data)
        if serializer.is_valid():
            inform_pk = serializer.validated_data.get('inform_pk')
            if InformRead.objects.filter(inform_id=inform_pk, user_id=request.user.uid).exists():
                return Response()
            else:
                try:
                    InformRead.objects.create(inform_id=inform_pk, user_id=request.user.uid)
                except Exception as e:
                    print(e)
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                return Response()
        else:
            return Response(data={'detail': list(serializer.errors.values())[0][0]}, status=status.HTTP_400_BAD_REQUEST)
