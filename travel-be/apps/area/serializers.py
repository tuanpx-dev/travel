from rest_framework import serializers
from .models import Province, City, Area, Station


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'


class CreateInterestAreaSerializer(serializers.Serializer):
    province_id = serializers.IntegerField(required=False, min_value=0)
    city_id = serializers.IntegerField(required=False, min_value=0)
    area_id = serializers.IntegerField(required=False, min_value=0)
    station_id = serializers.IntegerField(required=False, min_value=0)
