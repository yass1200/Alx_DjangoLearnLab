from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Colonnes visibles dans la liste
    list_display = ('title', 'author', 'publication_year')

    # Filtres latéraux
    list_filter = ('author', 'publication_year')

    # Barre de recherche
    search_fields = ('title', 'author')
