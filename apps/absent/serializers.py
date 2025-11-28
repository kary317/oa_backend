from rest_framework import serializers
from .models import Absent, AbsentType
from apps.oaauth.serializers import OAUserSerializer


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

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
