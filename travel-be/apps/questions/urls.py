from django.urls import path
from .views import QuestionModelViewSet, FetchAnswersViewSet, LikeQuestionViewSet, UserQuestionsViewSet, \
    FetchUserAnswersViewSet, SearchQuestionViewSet, UserSearchQuestionViewSet

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
    path('likes/', LikeQuestionViewSet.as_view({'post': 'create'})),
    path('auth-required-questions/', UserQuestionsViewSet.as_view({'get': 'list'})),
    path('auth-required-questions/<int:pk>/', UserQuestionsViewSet.as_view({'get': 'retrieve'})),
    path('auth-required-questions/<int:question_id>/answers/', FetchUserAnswersViewSet.as_view({'get': 'list'})),
    path('search/', SearchQuestionViewSet.as_view({'post': 'create'})),
    path('auth-required-search/', UserSearchQuestionViewSet.as_view({'post': 'create'})),
]
