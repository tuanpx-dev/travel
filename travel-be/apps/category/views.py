from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
from .permission import CategoryPermission
from travel.auth.core import JwtAuthentication

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
