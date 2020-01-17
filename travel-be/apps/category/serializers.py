from rest_framework import serializers
from .models import Category, InterestCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class CreateInterestCategorySerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=True, min_value=0)


class InterestCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = InterestCategory
        fields = '__all__'