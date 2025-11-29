import django_filters
from .models import Book


import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    Custom filter for Book model to enable filtering by title, author, and publication_year.
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    publication_year = django_filters.NumberFilter()

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
