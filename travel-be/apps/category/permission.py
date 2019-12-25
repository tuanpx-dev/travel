from rest_framework.permissions import BasePermission


class CategoryPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        if not request.token.is_valid():
            return False

        return request.token.user.is_superuser