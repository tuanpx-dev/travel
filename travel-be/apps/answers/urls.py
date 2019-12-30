from django.urls import path
from .views import AnswerModelViewSet, FetchCommentsViewSet, LikeAnswerViewSet, UserAnswersViewSet

snippet_list = {
    'get': 'list',
    'post': 'create'
}

snippet_detail = {
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
}

urlpatterns = [
    path('', AnswerModelViewSet.as_view(snippet_list)),
    path('<int:pk>/', AnswerModelViewSet.as_view(snippet_detail)),
    path('<int:answer_id>/comments/', FetchCommentsViewSet.as_view({'get': 'list'})),
    path('likes/', LikeAnswerViewSet.as_view({'post': 'create'})),
    path('auth-required-answers/', UserAnswersViewSet.as_view({'get': 'list'})),
    path('auth-required-answers/<int:pk>/', UserAnswersViewSet.as_view({'get': 'retrieve'})),
]
