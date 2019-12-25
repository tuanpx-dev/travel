from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from .models import Question
from apps.answers.models import Answer
from apps.category.models import Category
from .serializers import QuestionSerializer
from apps.answers.serializers import AnswerSerializer
from travel.auth.core import JwtAuthentication
from travel.permissions.core import IsOwnerOrReadOnly
from travel.errors.common import ErrorResponse


# Create your views here.
class QuestionModelViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [JwtAuthentication, ]
    permission_classes = [IsOwnerOrReadOnly, ]

    def get_authenticators(self):
        if self.request.method == 'GET':
            self.authentication_classes = []
        return [auth() for auth in self.authentication_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        category_id = validated_data.pop('category_id')
        try:
            category = Category.objects.get(id=category_id)
        except:
            return ErrorResponse(message="Category does not exist")
        question = Question.objects.create(user=request.token.user, category=category, **validated_data)
        return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)


class FetchAnswersViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def list(self, request, *args, **kwargs):
        question_id = kwargs.get("question_id")
        print(question_id)
        limit = int(request.GET.get("limit", 20))
        offset = int(request.GET.get("offset", 0))
        self.queryset = self.queryset.filter(question__id=question_id).order_by('-created_at')[offset:offset + limit]
        return Response(AnswerSerializer(self.queryset, many=True).data, status=status.HTTP_200_OK)
