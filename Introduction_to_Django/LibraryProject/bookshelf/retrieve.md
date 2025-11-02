\# RETRIEVE



```python

from bookshelf.models import Book

\# Adapte l'ID si nécessaire

b = Book.objects.get(id=2)

b.title, b.author, b.publication\_year



