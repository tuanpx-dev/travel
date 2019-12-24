from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser

TOKEN_LENGTH = 64


class User(AbstractUser):
    username = models.CharField(_('username'), max_length=150, unique=True)

    display_name = models.CharField(blank=True, null=True, max_length=150)
    email = models.EmailField(max_length=150, blank=True, null=True, unique=True)
    age = models.PositiveSmallIntegerField()
    facebook_id = models.CharField(blank=True, null=True, max_length=1000)
    area = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'user'


class Interest(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.TextField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
