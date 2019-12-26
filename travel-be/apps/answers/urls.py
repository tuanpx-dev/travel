from django.urls import path
from .views import AnswerModelViewSet, FetchCommentsViewSet, LikeAnswerViewSet

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
    path('likes/', LikeAnswerViewSet.as_view({'post': 'create'}))
]
