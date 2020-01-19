from django.urls import path
from .views import ProvinceModelViewSet, CityModelViewSet, AreaModelViewSet, StationModelViewSet

urlpatterns = [
    path('provinces/', ProvinceModelViewSet.as_view({'get': 'list'})),
    path('citys/', CityModelViewSet.as_view({'get': 'list'})),
    path('areas/', AreaModelViewSet.as_view({'get': 'list'})),
    path('stations/', StationModelViewSet.as_view({'get': 'list'})),
]
