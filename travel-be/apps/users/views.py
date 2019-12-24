import logging

from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users import models as user_models
from apps.users import serializers as user_sers
from apps.users import utils as user_utils

_logger = logging.getLogger(__name__)


class LoginEmailAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        validator = user_sers.LoginEmailValidator(data=request.data)
        if not validator.is_valid():
            _logger.error(validator.errors)
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)

        email = validator.validated_data['email']
        password = validator.validated_data['password']
        user = authenticate(email=email, password=password)
        if not user:
            _logger.error('Incorrect email: {} or password: ******'.format(email))
            return Response('Incorrect email or password', status=status.HTTP_401_UNAUTHORIZED)

        token = user_models.Token.objects.create(user=user)
        data = {
            'access_token': token.key,
            'expired_time': user_utils.get_expired_time(token),
            'user': user
        }
        serializer = user_sers.TokenSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginFacebookAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        validator = user_sers.LoginFacebookValidator(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)

        fb_access_token = validator.validated_data['fb_access_token']
        try:
            profiles = user_utils.get_facebook_profile(fb_access_token)
            fb_id = profiles['id']
            user_name = profiles['name']
        except Exception:
            return Response('Incorrect facebook id', status=status.HTTP_401_UNAUTHORIZED)
        user, created = user_models.User.objects.get_or_create(
            facebook_id=fb_id,
            default={'username': user_name}
        )
        token = user_models.Token.objects.create(user=user)
        data = {
            'access_token': token.key,
            'expired_time': user_utils.get_expired_time(token),
            'user': user
        }
        serializer = user_sers.TokenSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


# TODO create API
class GetProfile(APIView):

    def get(self):
        pass
