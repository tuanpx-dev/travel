from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hnt_db_test',
        'USER': 'ntq01',
        'PASSWORD': 'ntq123456',
        'HOST': '192.168.16.87',
        'PORT': '3306',
    }
}