from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library

# ---------- Function-based view ----------
def list_books(request):
    """
    List all books with their authors.
    If templates are configured, renders list_books.html.
    Otherwise returns a simple text response.
    """
    books = Book.objects.select_related("author").all()

    # Optional template render (recommended)
    if request.GET.get("html", "1") == "1":  # keep plain text fallback possible
        return render(request, "relationship_app/list_books.html", {"books": books})

    # Plain-text fallback
    lines = [f"{b.title} by {b.author.name}" for b in books]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# ---------- Class-based view ----------
class LibraryDetailView(DetailView):
    """
    Show details for a specific library and list its books.
    URL expects pk (library id).
    """
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    # Not strictly required, but handy if you want to prefetch related books
    def get_queryset(self):
        return Library.objects.prefetch_related("books__author")
