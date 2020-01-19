from django.db import models
from apps.users.models import User
from apps.category.models import Category
from apps.area.models import Province, City, Area, Station

# Create your models here.

ANSWER_TYPE = 1
LIKE_QUESTION_TYPE = 2
LIKE_ANSWER_TYPE = 3

POINT_MAP = {
    ANSWER_TYPE: 5,
    LIKE_QUESTION_TYPE: 3,
    LIKE_ANSWER_TYPE : 1
}


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(blank=True, null=True, max_length=256)
    body = models.TextField(blank=True, null=True)
    total_likes = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'question'

    def add_point(self, type):
        point = POINT_MAP.get(type, 0)
        self.point += point

    def subtract_point(self, type):
        point = POINT_MAP.get(type, 0)
        self.point -= point


class QuestionLikes(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'question_likes'


class QuestionCategories(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)


class QuestionAreas(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='areas')
    province = models.ForeignKey(Province, null=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, null=True, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, null=True, on_delete=models.CASCADE)
