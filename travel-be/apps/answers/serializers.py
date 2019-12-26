from rest_framework import serializers
from apps.users.serializers import UserSerializer
from apps.answers.models import Answer, AnswerLikes
from apps.comments.models import Comment


class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()

    class Meta:
        model = Answer
        fields = ['id', 'body', 'question_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        ret = super(AnswerSerializer, self).to_representation(instance)
        ret['total_likes'] = AnswerLikes.objects.filter(answer=instance).count()
        ret['total_commnets'] = Comment.objects.filter(answer=instance).count()
        ret['user'] = UserSerializer(instance.user).data
        return ret

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance


class LazyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'body', 'created_at', 'updated_at']
        read_only_fields = ['id', 'body', 'created_at', 'updated_at']


class LikeAnswerSerializer(serializers.Serializer):
    answer_id = serializers.IntegerField(required=True)
