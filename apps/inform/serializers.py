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
        # 如果前端使用json格式上传数据,可以不用指定read_only_fields
        # 如果前端使用表单方式提交数据,表单方式提交数据默认会携带有public=false,需要将public字段指定为只读字段
        read_only_fields = ('public',)

    def create(self, validated_data):
        request = self.context.get('request')
        department_ids = validated_data.pop('department_ids')
        # 将前端上传的部门id列表中的每个元素转为int类型
        department_ids = list(map(lambda value: int(value), department_ids))

        # 如果部门列表中有0,代表所有人可见
        if 0 in department_ids:
            inform = Inform.objects.create(public=True, author=request.user, **validated_data)
        else:
            departments = OADepartment.objects.filter(id__in=department_ids).all()
            # 如果不指定public为read_only_fields,那么前端使用表单方式提交数据,validated_data中会自带有public=false的键值对
            # json格式提交数据不会自带有public=false的键值对,
            # 猜测是序列化器有校验字段的功能,我们的Inform模型类中public有默认default=False,所以表单上传数据后序列化器帮你添加了public=false
            inform = Inform.objects.create(public=False, author=request.user, **validated_data)
            inform.departments.set(departments)
            inform.save()
        return inform
