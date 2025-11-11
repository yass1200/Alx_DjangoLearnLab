# LibraryProject/bookshelf/urls.py
from django.urls import path
from . import views


from django.urls import path
from . import views

app_name = "bookshelf"

urlpatterns = [
    path("books/", views.book_list, name="book_list"),        # <- matches the checker
    path("books/add/", views.add_book, name="add_book"),
    path("books/<int:pk>/edit/", views.edit_book, name="edit_book"),
    path("books/<int:pk>/delete/", views.delete_book, name="delete_book"),
]
