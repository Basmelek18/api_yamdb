from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter

from .permissions import (IsAdminOrReadOnly,)


class CreateListDestroyMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Кастомный миксин для Create, List, Delete операций"""
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
