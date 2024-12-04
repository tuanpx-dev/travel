import os
import logging

from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from django.conf import settings
from django.db.models import Q
from apps.users import serializers as user_sers
from apps.users.models import User
from apps.questions.models import Question
from apps.answers.models import Answer
from apps.questions.dto import UserQuestions
from apps.answers.dto import UserAnswers
from apps.users.utils import get_facebook_profile
from travel.auth.token import create_token, decode_token
from travel.auth.core import JwtAuthentication
from travel.errors.common import ErrorResponse
from travel.pagination.core import DEFAULT_LIMIT, DEFAULT_OFFSET, Paginator

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
            defaults={'username': user_name}
        )
        jwt_token = create_token(user.id, user.username)
        data = {
            'access_token': jwt_token.decode('utf-8'),
            'expired_time': decode_token(jwt_token).expire_at,
            'user': user
        }
        serializer = user_sers.TokenSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = user_sers.ProfileSerializer
    authentication_classes = [JwtAuthentication, ]

    def retrieve(self, request, *args, **kwargs):
        user = request.token.user
        serializer = user_sers.ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _remove_old_avatar(self, old_url):
        try:
            old_avatar_path = os.path.join(settings.BASE_DIR, old_url)
            os.remove(old_avatar_path)
        except Exception as e:
            _logger.error(e.__str__())


    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.token.user
        old_avatar_url = user.avatar.path

        validated_data = serializer.validated_data
        user.display_name = validated_data.get('display_name', user.display_name)
        user.email = validated_data.get('email', user.email)
        user.age = validated_data.get('age', user.age)
        user.avatar = validated_data.get('avatar', user.avatar)
        user.save()

        if old_avatar_url and old_avatar_url != '':
            self._remove_old_avatar(old_avatar_url)

        result = user_sers.ProfileSerializer(user)
        return Response(result.data, status=status.HTTP_200_OK)


class ChangePasswordViewSet(mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = user_sers.RequestChangePassword
    authentication_classes = [JwtAuthentication, ]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.token.user
        validated_data = serializer.validated_data
        old_password = validated_data.get('old_password')
        new_password = validated_data.get('new_password')
        if not user.check_password(old_password):
            return ErrorResponse(message="Old password is incorrect")
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)


class UserQuestionsViewSet(mixins.ListModelMixin, GenericViewSet):
    authentication_classes = [JwtAuthentication, ]

    def list(self, request, *args, **kwargs):
        user = request.token.user

        try:
            limit = int(request.GET.get("limit", DEFAULT_LIMIT))
            offset = int(request.GET.get("offset", DEFAULT_OFFSET))
            search = request.GET.get("search", None)
        except ValueError:
            return ErrorResponse(message="Parameters invalid")

        queryset = Question.objects.filter(user=user)

        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(body__icontains=search))

        total_length = queryset.count()
        queryset = queryset.order_by('-created_at')[offset:offset + limit]
        data = UserQuestions(request.token.user, list(queryset)).data()

        page = Paginator(content=data, limit=limit, offset=offset, total_length=total_length)
        return Response(page.data, status=status.HTTP_200_OK)


class UserAnswersViewSet(mixins.ListModelMixin, GenericViewSet):
    authentication_classes = [JwtAuthentication, ]

    def list(self, request, *args, **kwargs):
        user = request.token.user

        try:
            limit = int(request.GET.get("limit", DEFAULT_LIMIT))
            offset = int(request.GET.get("offset", DEFAULT_OFFSET))
            search = request.GET.get("search", None)
        except ValueError:
            return ErrorResponse(message="Parameters invalid")

        queryset = Answer.objects.filter(user=user)

        if search:
            queryset = queryset.filter(body__icontains=search)

        total_length = queryset.count()
        queryset = queryset.order_by('-created_at')[offset:offset + limit]
        data = UserAnswers(request.token.user, list(queryset)).data()

        page = Paginator(content=data, limit=limit, offset=offset, total_length=total_length)
        return Response(page.data, status=status.HTTP_200_OK)
