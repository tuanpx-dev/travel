from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from .models import Question, QuestionLikes
from apps.answers.models import Answer
from apps.category.models import Category
from .serializers import QuestionSerializer, LikeQuestionSerializer
from .dto import UserQuestion, UserQuestions
from apps.answers.serializers import AnswerSerializer
from travel.auth.core import JwtAuthentication
from travel.permissions.core import IsOwnerOrReadOnly
from travel.errors.common import ErrorResponse
from travel.pagination.core import DEFAULT_LIMIT, DEFAULT_OFFSET, Paginator


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

    def list(self, request, *args, **kwargs):
        try:
            limit = int(request.GET.get("limit", DEFAULT_LIMIT))
            offset = int(request.GET.get("offset", DEFAULT_OFFSET))
        except ValueError:
            return ErrorResponse(message="Parameters invalid")

        total_length = self.queryset.count()
        self.queryset = self.queryset.order_by('-created_at')[offset:offset+limit]
        serializers = QuestionSerializer(self.queryset, many=True)
        page = Paginator(content=serializers.data, limit=limit, offset=offset, total_length=total_length)
        return Response(page.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        category_id = validated_data.pop('category_id', None)
        try:
            category = Category.objects.get(id=category_id)
        except:
            question = Question.objects.create(user=request.token.user, **validated_data)
            return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)

        question = Question.objects.create(user=request.token.user, category=category, **validated_data)
        return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)


class FetchAnswersViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def list(self, request, *args, **kwargs):
        question_id = kwargs.get("question_id")
        try:
            limit = int(request.GET.get("limit", DEFAULT_LIMIT))
            offset = int(request.GET.get("offset", DEFAULT_OFFSET))
        except ValueError:
            return ErrorResponse(message="Parameters invalid")
        self.queryset = self.queryset.filter(question__id=question_id)
        total_length = self.queryset.count()
        self.queryset = self.queryset.order_by('-created_at')[offset:offset + limit]
        serializers = AnswerSerializer(self.queryset, many=True)
        page = Paginator(content=serializers.data, limit=limit, offset=offset, total_length=total_length)
        return Response(page.data, status=status.HTTP_200_OK)


class LikeQuestionViewSet(ModelViewSet):
    queryset = QuestionLikes.objects.all()
    serializer_class = LikeQuestionSerializer
    authentication_classes = [JwtAuthentication, ]
    permission_classes = [IsOwnerOrReadOnly, ]

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

        try:
            # if like this question then dislike
            like_question = QuestionLikes.objects.get(user=request.token.user, question=question)
            like_question.delete()
            question.total_likes -= 1
            question.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except QuestionLikes.DoesNotExist:
            # if not like this question then like
            QuestionLikes.objects.create(user=request.token.user, question=question)
            question.total_likes += 1
            question.save()
            return Response(status=status.HTTP_201_CREATED)


class UserQuestionsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Question.objects.all()
    authentication_classes = [JwtAuthentication, ]

    def retrieve(self, request, *args, **kwargs):
        question = self.get_object()
        user_question = UserQuestion(request.token.user, question)
        return Response(user_question.data(), status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        try:
            limit = int(request.GET.get("limit", DEFAULT_LIMIT))
            offset = int(request.GET.get("offset", DEFAULT_OFFSET))
        except ValueError:
            return ErrorResponse(message="Parameters invalid")

        total_length = self.queryset.count()
        self.queryset = self.queryset.order_by('-created_at')[offset:offset+limit]
        data = UserQuestions(request.token.user, list(self.queryset)).data()

        page = Paginator(content=data, limit=limit, offset=offset, total_length=total_length)
        return Response(page.data, status=status.HTTP_200_OK)
