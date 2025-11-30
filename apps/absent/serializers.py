from rest_framework import serializers
from rest_framework import exceptions

from .models import Absent, AbsentType, AbsentStatusChoices
from apps.oaauth.serializers import OAUserSerializer
from .utils import get_responder


class AbsentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsentType
        fields = '__all__'


class AbsentSerializer(serializers.ModelSerializer):
    absent_type = AbsentTypeSerializer(read_only=True)
    absent_type_id = serializers.IntegerField(write_only=True)

    requester = OAUserSerializer(read_only=True)
    responder = OAUserSerializer(read_only=True)

    class Meta:
        model = Absent
        fields = '__all__'

    def validate_absent_type_id(self, value):
        # if not Absent.objects.filter(pk=value).exists():
        if not AbsentType.objects.filter(pk=value).exists():
            raise exceptions.ValidationError('考勤类型不存在!')
        return value

    def create(self, validated_data):
        request = self.context['request']
        # 当前登录用户是考勤发起者requester
        user = request.user

        # 获取审批者
        responder = get_responder(request)

        # 如果是董事会的leader,请假直接通过
        if responder is None:
            validated_data['status'] = AbsentStatusChoices.PASS
        else:
            validated_data['status'] = AbsentStatusChoices.AUDITING

        absent = Absent.objects.create(**validated_data, requester=user, responder=responder)
        return absent

    def update(self, instance, validated_data):
        if instance.status != AbsentStatusChoices.AUDITING:
            raise exceptions.APIException(detail='不能修改已经确定的请假数据!')
        request = self.context['request']
        user = request.user

        if instance.responder.uid != user.uid:
            raise exceptions.AuthenticationFailed('您无权处理该考勤!')

        instance.status = validated_data.get('status')
        instance.response_content = validated_data.get('response_content')
        instance.save()
        return instance
