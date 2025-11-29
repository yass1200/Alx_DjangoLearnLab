from rest_framework import generics, permissions
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books.
    Allows any user to view all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    Allows any user to view individual book details.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book with custom validation.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom method to handle book creation.
        Can be extended to add additional logic like logging, notifications, etc.
        """
        serializer.save()
        # Additional custom logic can be added here
        # Example: send notification, update user activity, etc.

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book with custom behavior.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom method to handle book updates.
        """
        serializer.save()
        # Additional custom logic for updates

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books with filtering capabilities.
    Allows any user to view all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Custom queryset to enable basic filtering.
        Example: /api/books/?author=1
        """
        queryset = Book.objects.all()
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        return queryset
