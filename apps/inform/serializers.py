from rest_framework import serializers

from .models import Inform, InformRead
from apps.oaauth.serializers import OAUserSerializer, DepartmentSerializer
from apps.oaauth.models import OADepartment


class InformSerializer(serializers.ModelSerializer):
    author = OAUserSerializer(read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    # ListField字段接受列表,获取前端传过来的部门列表
    department_ids = serializers.ListField(write_only=True)

    class Meta:
        model = Inform
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        department_ids = validated_data.pop('department_ids')
        # 将前端上传的部门id列表中的每个元素转为int类型
        map(lambda value: int(value), department_ids)

        # 如果部门列表中有0,代表所有人可见
        if 0 in department_ids:
            inform = Inform.objects.create(pullic=True, author=request.user, **validated_data)
        else:
            departments = OADepartment.objects.filter(id__in=department_ids).all()
            inform = Inform.objects.create(public=False, author=request.user, **validated_data)
            inform.departments.set(departments)
            inform.save()
        return inform
