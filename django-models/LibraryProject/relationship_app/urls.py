from django.urls import path
from .views import list_books, LibraryDetailView

app_name = "relationship_app"

urlpatterns = [
    path("books/", list_books, name="list_books"),  # function-based view
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),  # class-based view
]
