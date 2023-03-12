from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import update_last_login
from rest_framework import serializers, exceptions
from rest_framework_simplejwt import settings, serializers as jwt_serializers, tokens

from apps.shared.verification import check_verification_code

User = get_user_model()


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, phone=None, verification_code=None, **kwargs):
        phone = phone if phone else kwargs.get(User.USERNAME_FIELD)
        verification_code = request.data.get('verification_code')

        if not phone or not verification_code:
            raise serializers.ValidationError('Phone number and verification code are required')

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid phone number')
        if not verification_code.isdigit() or not check_verification_code(phone, verification_code, fake=True):
            raise exceptions.AuthenticationFailed('Invalid verification code')
        if self.user_can_authenticate(user):
            return user


class CustomTokenObtainSerializer(jwt_serializers.TokenObtainSerializer):  # noqa pylint: disable=abstract-method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['verification_code'] = serializers.CharField(write_only=True)
        self.fields.pop('password', None)

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'verification_code': attrs.get('verification_code')
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not settings.api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}


class PhoneVerificationTokenObtainPairSerializer(CustomTokenObtainSerializer):
    token_class = tokens.RefreshToken
    phone = serializers.CharField(write_only=True)
    verification_code = serializers.CharField(write_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if settings.api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
