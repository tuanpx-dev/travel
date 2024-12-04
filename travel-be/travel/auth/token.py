import logging
from datetime import datetime, timedelta
import jwt
import pytz
from django.conf import settings
from rest_framework import exceptions
from apps.users.models import User

logger = logging.getLogger(__name__)


def create_token(id, username, algorithm='HS256'):
    iat = datetime.now().astimezone(tz=pytz.utc)
    exp = (datetime.now() + timedelta(seconds=settings.EXPIRED_TOKEN_TIME)).astimezone(tz=pytz.utc)
    payload = {
        'id': id,
        'username': username,
        'iat': iat,
        'exp': exp,
    }
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=algorithm
    )
    return token


def decode_token(token, algorithm='HS256'):
    try:
        raw_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[algorithm],
        )
    except jwt.exceptions.ExpiredSignatureError as e:
        raise exceptions.AuthenticationFailed(e.__str__())
    except Exception as e:
        raise exceptions.AuthenticationFailed(e.__str__())
    return Token(
        raw_token['id'],
        raw_token['username'],
        raw_token['exp'],
        raw_token['iat']
    )


class AbstractToken(object):
    def __init__(self):
        self._errors = []

    @property
    def id(self):
        return None

    @property
    def username(self):
        return None

    @property
    def expire_at(self):
        return None

    @property
    def created_at(self):
        return None

    @property
    def user(self):
        return None

    def is_valid(self):
        return False


class Token(AbstractToken):
    def __init__(self, id, username, expire_at, created_at):
        super(Token, self).__init__()
        self._id = id
        self._username = username
        self._created_at = created_at if isinstance(created_at, datetime)\
                else datetime.fromtimestamp(created_at)
        self._expire_at = expire_at if isinstance(expire_at, datetime)\
                else datetime.fromtimestamp(expire_at)

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def expire_at(self):
        return self._expire_at

    @property
    def created_at(self):
        return self._created_at

    @property
    def user(self):
        if hasattr(self, '_user'):
            return self._user
        try:
            self._user = self._get_user(self._id)
            return self._user
        except User.DoesNotExist:
            return None

    def _get_user(self, id):
        try:
            return User.objects.get(id=self._id)
        except User.DoesNotExist:
            return None

    def is_valid(self):
        if self.user is None:
            return False
        return True

class UnauthorizedToken(AbstractToken):

    def __init__(self, *errors):
        self._errors = errors
