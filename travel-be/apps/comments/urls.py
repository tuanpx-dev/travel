from django.urls import path
from .views import CommentModelViewSet

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
    path('', CommentModelViewSet.as_view(snippet_list)),
    path('<int:pk>/', CommentModelViewSet.as_view(snippet_detail)),
]
