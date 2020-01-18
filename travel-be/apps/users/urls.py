from django.urls import path
from .views import ProfileModelViewSet, ChangePasswordViewSet, UserQuestionsViewSet, UserAnswersViewSet

urlpatterns = [
    path('profile/', ProfileModelViewSet.as_view({'get':'retrieve', 'put':'update'})),
    path('change-password/', ChangePasswordViewSet.as_view({'put': 'update'})),
    path('questions/', UserQuestionsViewSet.as_view({'get': 'list'})),
    path('answers/', UserAnswersViewSet.as_view({'get': 'list'}))
]
