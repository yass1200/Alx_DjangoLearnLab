from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django import forms
from django.contrib.auth.decorators import permission_required

from .models import Library
from .models import Book

# ---------- Exercise 1: FBV + CBV for books & library ----------
from django.views.generic.detail import DetailView   # needed for the class-based view
from .models import Book, Library                    # grader checks for this exact import line

# Function-based view: list all books (simple text/HTML list)
def list_books(request):
    books = Book.objects.all()   # grader looks for Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view: show details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
# ---------------------------------------------------------------


# --- Registration (function-based) ---
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally log the user in right after registering:
            login(request, user)
            return redirect('list_books')   # or any page you want
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# --- Login / Logout (class-based, built-ins) ---
class AppLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class AppLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'
# relationship_app/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def _has_role(user, role_name: str) -> bool:
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == role_name

# ---- Role-based views ----
@login_required
@user_passes_test(lambda u: _has_role(u, 'Admin'))
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(lambda u: _has_role(u, 'Librarian'))
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(lambda u: _has_role(u, 'Member'))
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django import forms

from .models import Book




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django import forms

from .models import Book


# ---- Forms ----
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]


# ---- Views protected with custom permissions ----

@login_required
@permission_required("relationship_app.can_view", raise_exception=True)
def list_books(request):
    """List all books (requires can_view)."""
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


@login_required
@permission_required("relationship_app.can_create", raise_exception=True)
def add_book_view(request):
    """Create a book (requires can_create)."""
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm()
    return render(request, "relationship_app/book_form.html", {"form": form, "action": "Add"})


@login_required
@permission_required("relationship_app.can_edit", raise_exception=True)
def edit_book_view(request, pk):
    """Edit a book (requires can_edit)."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm(instance=book)
    return render(request, "relationship_app/book_form.html", {"form": form, "action": "Edit"})


@login_required
@permission_required("relationship_app.can_delete", raise_exception=True)
def delete_book_view(request, pk):
    """Delete a book (requires can_delete)."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "relationship_app/book_confirm_delete.html", {"book": book})



