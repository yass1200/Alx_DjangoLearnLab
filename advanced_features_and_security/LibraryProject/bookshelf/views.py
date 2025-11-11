# LibraryProject/bookshelf/views.py
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
def list_books(request):
    books = Book.objects.all()
    return render(request, "bookshelf/list_books.html", {"books": books})


@login_required
@permission_required("bookshelf.can_create", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("bookshelf:list_books")
    else:
        form = BookForm()
    return render(request, "bookshelf/book_form.html", {"form": form, "action": "Add"})


@login_required
@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("bookshelf:list_books")
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/book_form.html", {"form": form, "action": "Edit"})


@login_required
@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("bookshelf:list_books")
    return render(request, "bookshelf/book_confirm_delete.html", {"book": book})
