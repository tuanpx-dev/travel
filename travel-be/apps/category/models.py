from django.db import models
from django.utils.translation import gettext as _
from apps.users.models import User

# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(User, related_name=_('create_by'), on_delete=models.CASCADE)
    name = models.CharField(blank=True, null=True, max_length=256)
    description = models.CharField(blank=True, null=True, max_length=256)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'category'


class InterestCategory(models.Model):
    user = models.ForeignKey(User, related_name='interest_categories', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
