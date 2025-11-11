# LibraryProject/bookshelf/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django import forms

from .models import Book

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]


@login_required
@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    """
    Safe search using Django ORM and validated input.
    No raw SQL; no string concatenation into queries.
    """
    form = SearchForm(request.GET or None)
    qs = Book.objects.select_related("author").all()

    if form.is_valid():
        q = form.cleaned_data.get("q") or ""
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(author__name__icontains=q)
            )

    return render(request, "bookshelf/book_list.html", {"books": qs, "form": form})

@login_required
@permission_required("bookshelf.can_create", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("bookshelf:book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/form_example.html", {"form": form, "action": "Add"})

@login_required
@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("bookshelf:book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/form_example.html", {"form": form, "action": "Edit"})

@login_required
@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("bookshelf:book_list")
    # Reuse form_example for a simple confirm, or keep your dedicated template
    return render(request, "bookshelf/form_example.html", {"form": None, "action": "Confirm delete", "book": book})

# LibraryProject/bookshelf/views.py
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .forms import ExampleForm


@csrf_protect
def example_form_view(request):
    """
    Demonstrates secure form handling (CSRF token, input validation).
    """
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Handle sanitized data securely (no direct SQL!)
            cleaned = form.cleaned_data
            # You could save or log it; we just show success message
            return render(request, "bookshelf/form_example.html", {"form": form, "success": True})
    else:
        form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})
