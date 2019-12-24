from rest_framework import serializers
from apps.users import models as user_models


class LoginEmailValidator(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)


class LoginFacebookValidator(serializers.Serializer):
    fb_access_token = serializers.CharField(required=True, allow_blank=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = ('id', 'username', 'display_name', 'email', 'age',
                  'place', 'created_at', 'created_at', 'updated_at')


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    expired_time = serializers.DateTimeField()
    user = UserSerializer(read_only=True)
