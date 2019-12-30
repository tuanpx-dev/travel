import os
import urllib
from rest_framework import serializers
from django.conf import settings
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
                  'place', 'created_at', 'updated_at')

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        avatar_path = instance.avatar.url
        if avatar_path and avatar_path != '':
            print(settings.DOMAIN_SERVER)
            ret['avatar'] = urllib.parse.urljoin(settings.DOMAIN_SERVER, avatar_path)
        return ret


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    expired_time = serializers.DateTimeField()
    user = UserSerializer(read_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = ('id', 'username', 'display_name', 'email', 'age',
                  'place', 'avatar', 'created_at', 'updated_at')
        read_only_fields = ['id', 'username', 'created_at', 'updated_at']

    def to_representation(self, instance):
        ret = super(ProfileSerializer, self).to_representation(instance)
        avatar_path = instance.avatar.url
        if avatar_path and avatar_path != '':
            print(settings.DOMAIN_SERVER)
            ret['avatar'] = urllib.parse.urljoin(settings.DOMAIN_SERVER, avatar_path)
        return ret

    def update(self, instance, validated_data):
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.email = validated_data.get('email', instance.email)
        instance.age = validated_data.get('age', instance.age)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class RequestChangePassword(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
