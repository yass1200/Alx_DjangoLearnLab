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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Profile", {"fields": ("date_of_birth", "profile_photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )
    list_display = ("username", "email", "date_of_birth", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")

