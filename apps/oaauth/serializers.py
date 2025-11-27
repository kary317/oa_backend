from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import OAUser, UserStatusChoice, OADepartment


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True,
                                   error_messages={'required': "email必填", 'invalid': '邮箱格式不正确'})
    password = serializers.CharField(max_length=20, min_length=6, write_only=True,
                                     error_messages={'required': 'password必填', 'min_length': '密码需要6-20位之间',
                                                     'max_length': '密码需要6-20位之间'})

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        user = OAUser.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError('请输入正确的邮箱')
        if not user.check_password(password):
            raise serializers.ValidationError('请输入正确的密码')

        if user.status == UserStatusChoice.UNACTIVE:
            raise serializers.ValidationError('该用户尚未激活')
        elif user.status == UserStatusChoice.LOCKED:
            raise serializers.ValidationError("该用户已被锁定，请联系管理员！")

        attrs['user'] = user
        return attrs


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OADepartment
        fields = '__all__'


class OAUserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = OAUser
        # fields = "__all__"
        exclude = ('password', 'groups', 'user_permissions')


class ResetPwdSerializer(serializers.Serializer):
    oldpwd = serializers.CharField(min_length=6, max_length=20)
    pwd1 = serializers.CharField(min_length=6, max_length=20)
    pwd2 = serializers.CharField(min_length=6, max_length=20)

    def validate(self, attrs):
        oldpwd = attrs.get('oldpwd')
        pwd1 = attrs.get('pwd1')
        pwd2 = attrs.get('pwd2')

        request = self.context.get('request')
        if not request.user.check_password(oldpwd):
            raise ValidationError('原密码不正确')
        if pwd1 != pwd2:
            raise ValidationError('新密码不一致')
        return attrs
