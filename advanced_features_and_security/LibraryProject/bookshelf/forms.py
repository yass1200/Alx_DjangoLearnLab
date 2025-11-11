# bookshelf/forms.py
from django import forms
from .models import Book

class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        max_length=100,
        strip=True,
        label="Search",
        help_text="Search by title or author",
    )

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]
