import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from .models import Province, City, Area, Station
from .serializers import ProvinceSerializer, CitySerializer, AreaSerializer, StationSerializer, \
    CreateInterestAreaSerializer
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
