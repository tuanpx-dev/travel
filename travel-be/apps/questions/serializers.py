from rest_framework import serializers
from .models import Question, QuestionLikes, QuestionAreas, QuestionCategories
from apps.users.serializers import UserSerializer
from apps.answers.models import Answer
from apps.area.serializers import ProvinceSerializer, CitySerializer, AreaSerializer, StationSerializer
from apps.category.serializers import CategorySerializer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'total_likes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total_likes', 'created_at', 'updated_at']
        
    def to_representation(self, instance):
        ret = super(QuestionSerializer, self).to_representation(instance)
        ret['categoies'] = QuestionCategoriesSerializer(instance.categories.all(), many=True).data
        ret['areas'] = QuestionAreasSerializer(instance.areas.all(), many=True).data
        ret['total_answers'] = Answer.objects.filter(question=instance).count()
        ret['user'] = UserSerializer(instance.user).data
        return ret

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance


class QuestionAreaSerializer(serializers.Serializer):
    province_id = serializers.IntegerField(required=False, min_value=0)
    city_id = serializers.IntegerField(required=False, min_value=0)
    area_id = serializers.IntegerField(required=False, min_value=0)
    station_id = serializers.IntegerField(required=False, min_value=0)


class CreateQuestionSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    body = serializers.CharField(required=False)
    categories = serializers.ListField(child=serializers.IntegerField(min_value=0), allow_empty=True, default=[])
    areas = serializers.ListField(child=QuestionAreaSerializer(), allow_empty=True, default=[])


class LazyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'category', 'created_at', 'updated_at']
        read_only_fields = ['id', 'title', 'body', 'category', 'created_at', 'updated_at']


class LikeQuestionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=True)


class QuestionCategoriesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = QuestionCategories
        fields = '__all__'
        editable = False


class QuestionAreasSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()
    city = CitySerializer()
    area = AreaSerializer()
    station = StationSerializer()

    class Meta:
        model = QuestionAreas
        fields = '__all__'
        editable = False
