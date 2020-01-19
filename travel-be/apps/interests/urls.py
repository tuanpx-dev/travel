from django.urls import path
from .views import InterestsModelViewSet

urlpatterns = [
    path('', InterestsModelViewSet.as_view({'post':'create', 'get': 'list'})),
]
