from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from apps.questions.models import Question
from .models import Answer
from .serializers import AnswerSerializer
from travel.auth.core import JwtAuthentication
from travel.permissions.core import IsOwnerOrReadOnly
from travel.errors.common import ErrorResponse


# Create your views here.
class AnswerModelViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
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
        question_id = validated_data.pop('question_id')
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return ErrorResponse(message="Question does not exist")
        answer = Answer.objects.create(user=request.token.user, question=question, **validated_data)
        return Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED)
