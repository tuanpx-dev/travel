from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from apps.questions.models import Question
from .models import Answer, AnswerLikes
from apps.comments.models import Comment
from .serializers import AnswerSerializer, LikeAnswerSerializer
from .dto import UserAnswer, UserAnswers
from apps.comments.serializers import CommentSerializer
from travel.auth.core import JwtAuthentication
from travel.permissions.core import IsOwnerOrReadOnly
from travel.errors.common import ErrorResponse
from travel.pagination.core import DEFAULT_LIMIT, DEFAULT_OFFSET, Paginator


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

    def list(self, request, *args, **kwargs):
        try:
            limit = int(request.GET.get("limit", DEFAULT_LIMIT))
            offset = int(request.GET.get("offset", DEFAULT_OFFSET))
        except ValueError:
            return ErrorResponse(message="Parameters invalid")

        total_length = self.queryset.count()
        self.queryset = self.queryset.order_by('-created_at')[offset:offset+limit]
        serializers = AnswerSerializer(self.queryset, many=True)
        page = Paginator(content=serializers.data, limit=limit, offset=offset, total_length=total_length)
        return Response(page.data, status=status.HTTP_200_OK)

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


class FetchCommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        answer_id = kwargs.get("answer_id")
        try:
            limit = int(request.GET.get("limit", DEFAULT_LIMIT))
            offset = int(request.GET.get("offset", DEFAULT_OFFSET))
        except ValueError:
            return ErrorResponse(message="Parameters invalid")
        self.queryset = self.queryset.filter(answer__id=answer_id)
        total_length = self.queryset.count()
        self.queryset = self.queryset.order_by('created_at')[offset:offset + limit]
        serializers = CommentSerializer(self.queryset, many=True)
        page = Paginator(content=serializers.data, limit=limit, offset=offset, total_length=total_length)
        return Response(page.data, status=status.HTTP_200_OK)


class LikeAnswerViewSet(ModelViewSet):
    queryset = AnswerLikes.objects.all()
    serializer_class = LikeAnswerSerializer
    authentication_classes = [JwtAuthentication, ]
    permission_classes = [IsOwnerOrReadOnly, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        answer_id = validated_data.pop('answer_id')
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return ErrorResponse(message="Answer does not exist")

        try:
            # if like this answer then dislike
            like_answer = AnswerLikes.objects.get(user=request.token.user, answer=answer)
            like_answer.delete()
            answer.total_likes -= 1
            answer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AnswerLikes.DoesNotExist:
            # if not like this answer then like
            AnswerLikes.objects.create(user=request.token.user, answer=answer)
            answer.total_likes += 1
            answer.save()
            return Response(status=status.HTTP_201_CREATED)


class UserAnswersViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Answer.objects.all()
    authentication_classes = [JwtAuthentication, ]

    def retrieve(self, request, *args, **kwargs):
        answer = self.get_object()
        user_answer = UserAnswer(request.token.user, answer)
        return Response(user_answer.data(), status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        try:
            limit = int(request.GET.get("limit", DEFAULT_LIMIT))
            offset = int(request.GET.get("offset", DEFAULT_OFFSET))
        except ValueError:
            return ErrorResponse(message="Parameters invalid")

        total_length = self.queryset.count()
        self.queryset = self.queryset.order_by('-created_at')[offset:offset+limit]
        data = UserAnswers(request.token.user, list(self.queryset)).data()

        page = Paginator(content=data, limit=limit, offset=offset, total_length=total_length)
        return Response(page.data, status=status.HTTP_200_OK)
