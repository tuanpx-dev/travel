from django.urls import path
from .views import CategoryModelViewSet, InterestCategoryViewSet

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
    path('interest/', InterestCategoryViewSet.as_view(snippet_list)),
    path('interest/<int:pk>/', InterestCategoryViewSet.as_view({'delete': 'destroy'})),
]
