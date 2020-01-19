import logging
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from .models import Question, QuestionLikes, QuestionAreas, QuestionCategories, LIKE_QUESTION_TYPE
from apps.answers.models import Answer
from apps.category.models import Category
from apps.area.models import Province, City, Area, Station
from .serializers import QuestionSerializer, LikeQuestionSerializer, CreateQuestionSerializer, SearchQuestionSerializer
from .dto import UserQuestion, UserQuestions
from .services import search_questions
from apps.answers.dto import UserAnswers
from apps.answers.serializers import AnswerSerializer
from travel.auth.core import JwtAuthentication
from travel.permissions.core import IsOwnerOrReadOnly
from travel.errors.common import ErrorResponse
from travel.pagination.core import DEFAULT_LIMIT, DEFAULT_OFFSET, Paginator

# Create your views here
_logger = logging.getLogger(__name__)


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
            search = request.GET.get("search", None)
            type = request.GET.get("type", settings.SEARCH_NEW_TYPE)
        except ValueError:
            return ErrorResponse(message="Parameters invalid")

        self.queryset, total_length = search_questions(self.queryset, limit, offset, search, None, type)

        serializers = QuestionSerializer(self.queryset, many=True)
        page = Paginator(content=serializers.data, limit=limit, offset=offset, total_length=total_length)
        return Response(page.data, status=status.HTTP_200_OK)

    def _create_question_categories(self, question, category_ids=[]):
        for category_id in category_ids:
            category = Category.objects.get(id=category_id)
            QuestionCategories.objects.create(question=question, category=category)

    def _create_question_areas(self, question, areas=[]):
        for area_dto in areas:
            province_id = area_dto.get('province_id', None)
            province = None
            if province_id:
                province = Province.objects.get(id=province_id)

            city_id = area_dto.get('city_id', None)
            city = None
            if city_id:
                city = City.objects.get(id=city_id)

            area_id = area_dto.get('area_id', None)
            area = None
            if area_id:
                area = Area.objects.get(id=area_id)

            station_id = area_dto.get('station_id', None)
            station = None
            if station_id:
                station = Station.objects.get(id=station_id)

            if province or city or area or station:
                QuestionAreas.objects.create(question=question, province=province, city=city, area=area,
                                             station=station)

    def create(self, request, *args, **kwargs):
        serializer = CreateQuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        title = validated_data.get('title', None)
        body = validated_data.get('body', None)
        categories = validated_data.get('categories', [])
        areas = validated_data.get('areas', [])

        try:
            with transaction.atomic():
                question = Question.objects.create(user=request.token.user, title=title, body=body)
                self._create_question_categories(question, category_ids=categories)
                self._create_question_areas(question, areas=areas)
                return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            _logger.info(e)
            return ErrorResponse(message="Parameters invalid")


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


class FetchUserAnswersViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    authentication_classes = [JwtAuthentication, ]

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
        data = UserAnswers(request.token.user, list(self.queryset)).data()
        page = Paginator(content=data, limit=limit, offset=offset, total_length=total_length)
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
            question.subtract_point(LIKE_QUESTION_TYPE)
            question.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except QuestionLikes.DoesNotExist:
            # if not like this question then like
            QuestionLikes.objects.create(user=request.token.user, question=question)
            question.total_likes += 1
            question.add_point(LIKE_QUESTION_TYPE)
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
            search = request.GET.get("search", None)
            sort_type = request.GET.get("type", settings.SEARCH_NEW_TYPE)
        except ValueError:
            return ErrorResponse(message="Parameters invalid")

        self.queryset, total_length = search_questions(self.queryset, limit, offset, search, None, sort_type)
        data = UserQuestions(request.token.user, list(self.queryset)).data()
        page = Paginator(content=data, limit=limit, offset=offset, total_length=total_length)
        return Response(page.data, status=status.HTTP_200_OK)


class SearchQuestionViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = SearchQuestionSerializer
    authentication_classes = []

    def _search_by_categories(self, categories):
        self.queryset = self.queryset.filter(categories__category__id__in=categories)

    def _search_by_areas(self, areas):
        queries = []
        for area in areas:
            province_id = area.get('province_id', None)
            city_id = area.get('city_id', None)
            area_id = area.get('area_id', None)
            station_id = area.get('station_id', None)

            conditions = []
            if province_id:
                conditions.append(Q(areas__province__id=province_id))

            if city_id:
                conditions.append(Q(areas__city__id=city_id))

            if area_id:
                conditions.append(Q(areas__area__id=area_id))

            if station_id:
                conditions.append(Q(areas__station__id=station_id))

            query = conditions.pop()
            for condition in conditions:
                query &= condition

            queries.append(query)

        query = queries.pop()
        for condition in queries:
            query |= condition

        self.queryset = self.queryset.filter(query)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        limit = validated_data.get('limit')
        offset = validated_data.get('offset')
        search = validated_data.get('search', None)
        categories = validated_data.get('categories', [])
        areas = validated_data.get('areas', [])
        type = validated_data.get('type')

        self.queryset, total_length = search_questions(self.queryset, limit, offset, search,
                                         {'categories': categories, 'areas': areas}, type, distinct=True)

        serializers = QuestionSerializer(self.queryset, many=True)
        page = Paginator(content=serializers.data, limit=limit, offset=offset, total_length=total_length)
        return Response(page.data, status=status.HTTP_200_OK)


class UserSearchQuestionViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = SearchQuestionSerializer
    authentication_classes = [JwtAuthentication, ]

    def _search_by_categories(self, categories):
        self.queryset = self.queryset.filter(categories__category__id__in=categories)

    def _search_by_areas(self, areas):
        queries = []
        for area in areas:
            province_id = area.get('province_id', None)
            city_id = area.get('city_id', None)
            area_id = area.get('area_id', None)
            station_id = area.get('station_id', None)

            conditions = []
            if province_id:
                conditions.append(Q(areas__province__id=province_id))

            if city_id:
                conditions.append(Q(areas__city__id=city_id))

            if area_id:
                conditions.append(Q(areas__area__id=area_id))

            if station_id:
                conditions.append(Q(areas__station__id=station_id))

            query = conditions.pop()
            for condition in conditions:
                query &= condition

            queries.append(query)

        query = queries.pop()
        for condition in queries:
            query |= condition

        self.queryset = self.queryset.filter(query)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        limit = validated_data.get('limit')
        offset = validated_data.get('offset')
        search = validated_data.get('search', None)
        categories = validated_data.get('categories', [])
        areas = validated_data.get('areas', [])
        type = validated_data.get('type')

        self.queryset, total_length = search_questions(self.queryset, limit, offset, search,
                                                       {'categories': categories, 'areas': areas}, type, distinct=True)

        data = UserQuestions(request.token.user, list(self.queryset)).data()
        page = Paginator(content=data, limit=limit, offset=offset, total_length=total_length)
        return Response(page.data, status=status.HTTP_200_OK)
