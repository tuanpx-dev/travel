from rest_framework import serializers
from apps.users.serializers import UserSerializer
from apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    answer_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['id', 'body', 'answer_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        ret = super(CommentSerializer, self).to_representation(instance)
        ret['user'] = UserSerializer(instance.user).data
        return ret

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance


class LazyCommetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_at', 'updated_at']
        read_only_fields = ['id', 'body', 'created_at', 'updated_at']