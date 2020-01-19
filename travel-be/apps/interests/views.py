import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q
from .models import Interest, InterestCategory
from .serializers import CreateInterestsSerializer, InterestSerializer
from apps.category.models import Category
from apps.area.models import Province, City, Area, Station
from travel.auth.core import JwtAuthentication
from travel.errors.common import ErrorResponse

_logger = logging.getLogger(__name__)

class InterestsModelViewSet(ModelViewSet):
    authentication_classes = [JwtAuthentication, ]
    serializer_class = CreateInterestsSerializer

    def _create_interest_area(self, user, province_id, city_id, area_id, station_id):
        province = None
        if province_id:
            province = Province.objects.get(id=province_id)

        city = None
        if city_id:
            city = City.objects.get(id=city_id)

        area = None
        if area_id:
            area = Area.objects.get(id=area_id)

        station = None
        if station_id:
            station = Station.objects.get(id=station_id)

        interest = Interest.objects.create(user=user, province=province, city=city, area=area, station=station)
        return interest

    def _create_interest_categories(self, interest, categories):
        for category_id in categories:
            category = Category.objects.get(id=category_id)
            InterestCategory.objects.create(interest=interest, category=category)

    def _create_interests(self, user, interests_data):
        interests = []
        for interest_data in interests_data:
            categories_serializer = interest_data.get('categories')
            province_id = interest_data.get('province_id', None)
            city_id = interest_data.get('city_id', None)
            area_id = interest_data.get('area_id', None)
            station_id = interest_data.get('station_id', None)

            interest = self._create_interest_area(user, province_id, city_id, area_id, station_id)
            self._create_interest_categories(interest, categories_serializer)
            interests.append(interest)

        return interests


    def create(self, request, *args, **kwargs):
        serializer = CreateInterestsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        interests_data = validated_data.get('interests')

        user = request.token.user
        interests = user.interests.all()

        try:
            with transaction.atomic():
                interests.delete()
                interests = self._create_interests(user, interests_data)
                serializer = InterestSerializer(interests, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            _logger.info(e)
            return ErrorResponse(message="Parameters invalid")

    def list(self, request, *args, **kwargs):
        user = request.token.user
        interests = user.interests.all()
        serializer = InterestSerializer(interests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
