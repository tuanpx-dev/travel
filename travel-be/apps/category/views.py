from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from .models import Category, InterestCategory
from .serializers import CategorySerializer, CreateInterestCategorySerializer, InterestCategorySerializer
from .permission import CategoryPermission
from travel.errors.common import ErrorResponse
from travel.auth.core import JwtAuthentication
from travel.permissions.core import IsOwnerOrReadOnly


# Create your views here.
class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [JwtAuthentication, ]
    permission_classes = [CategoryPermission, ]

    def get_authenticators(self):
        if self.request.method == 'GET':
            self.authentication_classes = []
        return [auth() for auth in self.authentication_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        category = Category.objects.create(user=request.token.user, **validated_data)
        return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)


class InterestCategoryViewSet(ModelViewSet):
    queryset = InterestCategory.objects.all()
    serializer_class = CreateInterestCategorySerializer
    authentication_classes = [JwtAuthentication, ]
    permission_classes = [IsOwnerOrReadOnly, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        category_id = validated_data.pop('category_id')
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return ErrorResponse(message="Category does not exist")

        interest = InterestCategory.objects.create(user=request.token.user, category=category)
        return Response(InterestCategorySerializer(interest).data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        user = request.token.user
        categories = user.interest_categories.all()
        return Response(InterestCategorySerializer(categories, many=True).data, status=status.HTTP_200_OK)
