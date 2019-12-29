from rest_framework import serializers
from .models import Question, QuestionLikes
from apps.users.serializers import UserSerializer
from apps.answers.models import Answer


class QuestionSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=False)
    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'category_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def to_representation(self, instance):
        ret = super(QuestionSerializer, self).to_representation(instance)
        ret['total_likes'] = QuestionLikes.objects.filter(question=instance).count()
        ret['total_answers'] = Answer.objects.filter(question=instance).count()
        ret['user'] = UserSerializer(instance.user).data
        return ret

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance

class LazyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'category', 'created_at', 'updated_at']
        read_only_fields = ['id', 'title', 'body', 'category', 'created_at', 'updated_at']


class LikeQuestionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=True)
