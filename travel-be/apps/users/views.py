import logging

from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users import serializers as user_sers
from travel.auth.token import create_token, decode_token

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

        jwt_token = create_token(user.id, user.username)
        data = {
            'access_token': jwt_token,
            'expired_time': decode_token(jwt_token).expire_at,
            'user': user
        }
        serializer = user_sers.TokenSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


# TODO create API
class GetProfile(APIView):

    def get(self):
        pass
