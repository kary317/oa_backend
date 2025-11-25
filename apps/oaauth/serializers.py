from rest_framework import serializers
from .models import OAUser, UserStatusChoice, OADepartment


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=20, min_length=6, write_only=True)

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
