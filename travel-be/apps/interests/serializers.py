from rest_framework import serializers
from .models import Interest
from apps.category.models import Category
from apps.category.serializers import CategorySerializer
from apps.area.serializers import ProvinceSerializer, CitySerializer, AreaSerializer, StationSerializer


class InterestSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()
    city = CitySerializer()
    area = AreaSerializer()
    station = StationSerializer()

    class Meta:
        model = Interest
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(InterestSerializer, self).to_representation(instance)
        category_ids = instance.categories.all().values_list('category_id', flat=True)
        categories = Category.objects.filter(id__in = category_ids)
        ret['categoies'] = CategorySerializer(categories, many=True).data
        return ret


class CreateInterestSerializer(serializers.Serializer):
    categories = serializers.ListField(child=serializers.IntegerField(min_value=0), allow_empty=True, default=[])
    province_id = serializers.IntegerField(required=False, min_value=0)
    city_id = serializers.IntegerField(required=False, min_value=0)
    area_id = serializers.IntegerField(required=False, min_value=0)
    station_id = serializers.IntegerField(required=False, min_value=0)

    def validate(self, attrs):
        if attrs.get('categories') or attrs.get('province_id', None) or attrs.get('city_id', None)\
                or attrs.get('area_id', None) or attrs.get('station_id', None):
            return attrs
        raise serializers.ValidationError("Parameters are empty")


class CreateInterestsSerializer(serializers.Serializer):
    interests = serializers.ListField(child=CreateInterestSerializer(), allow_empty=False)
