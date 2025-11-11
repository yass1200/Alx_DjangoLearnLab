from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('', include('relationship_app.urls')),
    path('admin/', admin.site.urls),
    path("", include("bookshelf.urls")),
]

