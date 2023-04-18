from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (user.is_authenticated
                and user.is_admin or user.is_superuser)


class IsAuthorAdminModeratorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == user
            or user.is_admin
            or user.is_moderator
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return request.method in permissions.SAFE_METHODS or (
            user.is_authenticated
            and (user.is_superuser
                 or user.is_admin)
        )
