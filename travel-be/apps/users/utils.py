from datetime import timedelta

from travel import settings


def get_expired_time(token):
    return token.created + timedelta(seconds=settings.EXPIRED_TOKEN_TIME)
