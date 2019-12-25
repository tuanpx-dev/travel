import logging

from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.users import serializers as user_sers
from apps.users.models import User
from apps.users.utils import get_facebook_profile
from travel.auth.token import create_token, decode_token

_logger = logging.getLogger(__name__)


class LoginEmailAPI(GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = user_sers.LoginEmailValidator

    def post(self, request, format=None):
        """
        api login with email:
        """
        validator = user_sers.LoginEmailValidator(data=request.data)
        if not validator.is_valid():
            _logger.error(validator.errors)
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)

        email = validator.validated_data['email']
        password = validator.validated_data['password']
        user = User.objects.filter(email=email).first()
        if user is None or user.check_password(password) == False:
            _logger.error('Incorrect email: {} or password: ******'.format(email))
            return Response('Incorrect email or password', status=status.HTTP_401_UNAUTHORIZED)

        jwt_token = create_token(user.id, user.username)
        data = {
            'access_token': jwt_token.decode('utf-8'),
            'expired_time': decode_token(jwt_token).expire_at,
            'user': user
        }
        serializer = user_sers.TokenSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginFacebookAPI(GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = user_sers.LoginFacebookValidator

    def post(self, request, format=None):
        validator = user_sers.LoginFacebookValidator(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)

        fb_access_token = validator.validated_data['fb_access_token']
        try:
            profiles = get_facebook_profile(fb_access_token)
            fb_id = profiles['id']
            user_name = profiles['name']
        except Exception:
            return Response('Incorrect facebook id', status=status.HTTP_401_UNAUTHORIZED)
        user, created = User.objects.get_or_create(
            facebook_id=fb_id,
            default={'username': user_name}
        )
        jwt_token = create_token(user.id, user.username)
        data = {
            'access_token': jwt_token.decode('utf-8'),
            'expired_time': decode_token(jwt_token).expire_at,
            'user': user
        }
        serializer = user_sers.TokenSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


# TODO create API
class GetProfile(APIView):

    def get(self):
        pass
