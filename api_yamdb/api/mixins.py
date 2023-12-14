from rest_framework import viewsets, mixins


class CreateListDestroyMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Кастомный миксин для Create, List, Delete операций"""
    pass
