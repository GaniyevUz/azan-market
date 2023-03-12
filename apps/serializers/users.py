from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import User
from apps.shared.verification import send_verification_code


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'phone',

    def create(self, validated_data):
        phone = validated_data['phone']
        user, _ = User.objects.get_or_create(phone=phone)
        user.set_password(phone)
        user.save()
        send_verification_code(phone, fake=True)
        return user
