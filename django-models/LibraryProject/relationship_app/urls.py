from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    register,
    AppLoginView,
    AppLogoutView,
)

urlpatterns = [
    # existing views
    path('books/', list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # auth
    path('login/', AppLoginView.as_view(), name='login'),
    path('logout/', AppLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]
