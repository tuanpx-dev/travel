import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from .models import Province, City, Area, Station, InterestArea
from .serializers import ProvinceSerializer, CitySerializer, AreaSerializer, StationSerializer, \
    CreateInterestAreaSerializer, InterestAreaSerializer
from travel.errors.common import ErrorResponse
from travel.auth.core import JwtAuthentication
from travel.permissions.core import IsOwnerOrReadOnly

# Create your views here.
_logger = logging.getLogger(__name__)


class ProvinceModelViewSet(ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    authentication_classes = []


class CityModelViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        try:
            province_id = int(request.GET.get('province_id', 0))
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if province_id > 0:
            self.queryset = self.queryset.filter(province__id=province_id)
        serializers = self.get_serializer(self.queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class AreaModelViewSet(ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        try:
            city_id = int(request.GET.get('city_id', 0))
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if city_id > 0:
            self.queryset = self.queryset.filter(city__id=city_id)
        serializers = self.get_serializer(self.queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class StationModelViewSet(ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        try:
            city_id = int(request.GET.get('city_id', 0))
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if city_id > 0:
            self.queryset = self.queryset.filter(city__id=city_id)
        serializers = self.get_serializer(self.queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class InterestAreaViewSet(ModelViewSet):
    queryset = InterestArea.objects.all()
    serializer_class = CreateInterestAreaSerializer
    authentication_classes = [JwtAuthentication, ]
    permission_classes = [IsOwnerOrReadOnly, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        try:
            province_id = validated_data.get('province_id', None)
            province = None
            if province_id:
                province = Province.objects.get(id=province_id)

            city_id = validated_data.get('city_id', None)
            city = None
            if city_id:
                city = City.objects.get(id=city_id)

            area_id = validated_data.get('area_id', None)
            area = None
            if area_id:
                area = Area.objects.get(id=area_id)

            station_id = validated_data.get('station_id', None)
            station = None
            if station_id:
                station = Station.objects.get(id=station_id)

            if province or city or area or station:
                interest = InterestArea.objects.create(user=request.token.user, province=province, city=city, area=area, station=station)
                return Response(InterestAreaSerializer(interest).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            _logger.info(e)

        return ErrorResponse(message="Parameters invalid")

    def list(self, request, *args, **kwargs):
        user = request.token.user
        areas = user.interest_areas.all()
        return Response(InterestAreaSerializer(areas, many=True).data, status=status.HTTP_200_OK)
