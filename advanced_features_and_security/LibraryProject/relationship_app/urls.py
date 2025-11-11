# relationship_app/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import list_books


from django.urls import path
from . import views


urlpatterns = [
    # Auth
    path('login/',  LoginView.as_view(template_name='relationship_app/login.html'),  name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # Views from previous task (keep these if you already added them)
    path('books/', views.list_books, name='list_books'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('role/admin/', views.admin_view, name='admin_view'),
    path('role/librarian/', views.librarian_view, name='librarian_view'),
    path('role/member/', views.member_view, name='member_view'),
    path('books/add/', views.add_book_view, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book_view, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book_view, name='delete_book'),
    path("books/add/", views.add_book_view, name="add_book"),
    path("books/<int:pk>/edit/", views.edit_book_view, name="edit_book"),
    path("books/<int:pk>/delete/", views.delete_book_view, name="delete_book"),
    path("add_book/", views.add_book_view, name="add_book"),
    path("edit_book/<int:pk>/", views.edit_book_view, name="edit_book"),
    path("delete_book/<int:pk>/", views.delete_book_view, name="delete_book"),
       # Exercise 1 paths (names can be anything, but these are common)
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
        path("books/", views.list_books, name="list_books"),
    path("books/add/", views.add_book_view, name="add_book"),
    path("books/<int:pk>/edit/", views.edit_book_view, name="edit_book"),
    path("books/<int:pk>/delete/", views.delete_book_view, name="delete_book"),
]

