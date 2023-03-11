from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import User
from apps.shared.verification import send, check


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'phone',

    def create(self, validated_data):
        phone = validated_data['phone']
        user = User.objects.create(phone=phone, is_active=False)
        user.set_password(phone)
        user.save()
        send(phone, True)
        return user


class UserAccountActivatonSerializer(Serializer):
    phone = CharField(max_length=11)
    code = CharField(max_length=4)
