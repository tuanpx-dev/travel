from django.urls import path
from .views import ProvinceModelViewSet, CityModelViewSet, AreaModelViewSet, StationModelViewSet, InterestAreaViewSet

urlpatterns = [
    path('provinces/', ProvinceModelViewSet.as_view({'get': 'list'})),
    path('citys/', CityModelViewSet.as_view({'get': 'list'})),
    path('areas/', AreaModelViewSet.as_view({'get': 'list'})),
    path('stations/', StationModelViewSet.as_view({'get': 'list'})),
    path('interest/', InterestAreaViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('interest/<int:pk>/', InterestAreaViewSet.as_view({'delete': 'destroy'})),
]
