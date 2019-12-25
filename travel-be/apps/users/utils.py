import requests
from datetime import timedelta

from travel import settings


def get_expired_time(token):
    return token.created + timedelta(seconds=settings.EXPIRED_TOKEN_TIME)


def get_facebook_profile(fb_access_token):
    response = requests.get(settings.URL_GET_ID_FACEBOOK + fb_access_token).json()
    data = {
        'id': response['id'],
        'name': response['name']
    }
    return data
