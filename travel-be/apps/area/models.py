from django.db import models
from apps.users.models import User

# Create your models here.
class Province(models.Model):
    name = models.CharField(blank=True, null=True, max_length=256)


class City(models.Model):
    name = models.CharField(blank=True, null=True, max_length=256)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)


class Area(models.Model):
    name = models.CharField(blank=True, null=True, max_length=256)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class Station(models.Model):
    name = models.CharField(blank=True, null=True, max_length=256)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class InterestArea(models.Model):
    user = models.ForeignKey(User, related_name='interest_areas', on_delete=models.CASCADE)
    province = models.ForeignKey(Province, null=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, null=True, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, null=True, on_delete=models.CASCADE)
