import binascii
import os

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser

from travel import settings

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


class Token(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=TOKEN_LENGTH, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='tokens',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        db_table = 'token'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        num_bytes = TOKEN_LENGTH // 2
        return binascii.hexlify(os.urandom(num_bytes)).decode()

    def __str__(self):
        return 'Token (user {}): {}'.format(self.user_id, self.key)
