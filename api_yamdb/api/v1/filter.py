import django_filters

from reviews.models import Title


class TitleFilters(django_filters.FilterSet):
    """Filtration of works."""
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact',
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='iexact',
    )
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='iexact',
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
