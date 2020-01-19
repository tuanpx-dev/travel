from django.db import models
from apps.users.models import User
from apps.category.models import Category
from apps.area.models import Province, City, Area, Station

# Create your models here.

class Interest(models.Model):
    user = models.ForeignKey(User, related_name='interests', on_delete=models.CASCADE)
    province = models.ForeignKey(Province, null=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, null=True, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, null=True, on_delete=models.CASCADE)


class InterestCategory(models.Model):
    interest = models.ForeignKey(Interest, related_name='categories', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
