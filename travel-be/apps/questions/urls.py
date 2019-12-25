from django.urls import path
from .views import QuestionModelViewSet, FetchAnswersViewSet

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
    path('', QuestionModelViewSet.as_view(snippet_list)),
    path('<int:pk>/', QuestionModelViewSet.as_view(snippet_detail)),
    path('<int:question_id>/answers/', FetchAnswersViewSet.as_view({'get': 'list'})),
]
