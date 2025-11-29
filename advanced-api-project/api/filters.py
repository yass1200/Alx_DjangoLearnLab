import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    Custom filter for Book model to enable advanced filtering capabilities.
    Supports filtering by title, author name, and publication year ranges.
    """
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title contains')
    author__name = django_filters.CharFilter(lookup_expr='icontains', label='Author name contains')
    publication_year = django_filters.NumberFilter(label='Exact publication year')
    publication_year__gte = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gte',
        label='Publication year greater than or equal to'
    )
    publication_year__lte = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lte',
        label='Publication year less than or equal to'
    )

    class Meta:
        model = Book
        fields = ['title', 'author__name', 'publication_year']
