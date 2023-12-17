from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Права доступа администратор."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_superuser)
        )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Права доступа администратор, модератор, автор."""
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or request.user == obj.author
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права доступа на изменения администратор."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_superuser)
        )

