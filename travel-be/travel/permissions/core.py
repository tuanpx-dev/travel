from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.token.is_valid():
            return False
        return request.token.user.is_superuser

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        if not request.token.is_valid():
            return False

        if request.method == 'POST':
            return request.token.is_valid()

        if request.method in ['PUT', 'DELETE']:
            return obj.user == request.token.user

        return request.token.user.is_superuser
