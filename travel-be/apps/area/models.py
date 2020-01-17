from django.db import models

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
