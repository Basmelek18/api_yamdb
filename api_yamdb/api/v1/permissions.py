from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Administrator access rights."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Access rights administrator, moderator, author."""
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
    """Change access rights are admin."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )
