from django.urls import path
from .views import CategoryModelViewSet

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
    path('', CategoryModelViewSet.as_view(snippet_list)),
    path('<int:pk>/', CategoryModelViewSet.as_view(snippet_detail)),
]
