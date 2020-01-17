from django.db import models
from apps.users.models import User
from apps.category.models import Category
from apps.area.models import Province, City, Area, Station

# Create your models here.
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(blank=True, null=True, max_length=256)
    body = models.TextField(blank=True, null=True)
    total_likes = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'question'


class QuestionLikes(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'question_likes'


class QuestionCategories(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class QuestionAreas(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='areas')
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
