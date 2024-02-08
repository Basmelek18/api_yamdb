from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter

from api.v1.permissions import (IsAdminOrReadOnly,)


class CreateListDestroyMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Custom mixin for Create, List, Delete operations"""
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
