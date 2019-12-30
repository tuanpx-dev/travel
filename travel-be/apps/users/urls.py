from django.urls import path
from .views import ProfileModelViewSet, ChangePasswordViewSet

urlpatterns = [
    path('profile/', ProfileModelViewSet.as_view({'get':'retrieve', 'put':'update'})),
    path('change-password/', ChangePasswordViewSet.as_view({'put': 'update'}))
]
