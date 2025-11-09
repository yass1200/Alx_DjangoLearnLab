"""
Sample ORM queries for relationship_app.

You can run this file directly:
    (djenv) ...\django-models\LibraryProject> python relationship_app\query_samples.py

Or via Django shell:
    python manage.py shell -c "from relationship_app.query_samples import demo; demo()"
"""

import os
import sys
import django

# Ensure Django can find settings when running this file directly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)  # ...\LibraryProject
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def get_books_by_author(author_name: str):
    """Query all books by a specific author."""
    return Book.objects.filter(author__name=author_name).values_list("title", flat=True)


def list_books_in_library(library_name: str):
    """List all books in a given library."""
    try:
        lib = Library.objects.prefetch_related("books__author").get(name=library_name)
    except Library.DoesNotExist:
        return []
    return [f"{b.title} (by {b.author.name})" for b in lib.books.all()]


def get_librarian_for_library(library_name: str):
    """Retrieve the librarian for a library (OneToOne)."""
    try:
        lib = Library.objects.select_related("librarian").get(name=library_name)
    except Library.DoesNotExist:
        return None
    return getattr(lib, "librarian", None)


def seed_demo_data():
    """Create a tiny dataset if empty, so queries have something to show."""
    if Author.objects.exists():
        return

    a1 = Author.objects.create(name="George Orwell")
    a2 = Author.objects.create(name="Jane Austen")

    b1 = Book.objects.create(title="1984", author=a1)
    b2 = Book.objects.create(title="Animal Farm", author=a1)
    b3 = Book.objects.create(title="Pride and Prejudice", author=a2)

    l1 = Library.objects.create(name="Central Library")
    l2 = Library.objects.create(name="Community Library")

    l1.books.add(b1, b3)
    l2.books.add(b2)

    Librarian.objects.create(name="Mr. Smith", library=l1)
    Librarian.objects.create(name="Ms. Johnson", library=l2)


def demo():
    seed_demo_data()

    print("Books by George Orwell:")
    print(list(get_books_by_author("George Orwell")))
    print()

    print("Books in Central Library:")
    print(list(list_books_in_library("Central Library")))
    print()

    print("Librarian for Community Library:")
    lib = get_librarian_for_library("Community Library")
    print(lib.name if lib else None)


if __name__ == "__main__":
    demo()
