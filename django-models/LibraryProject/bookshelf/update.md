\# UPDATE



```python

from bookshelf.models import Book

b = Book.objects.get(id=2)  # adapte l'ID si besoin

b.title = "Nineteen Eighty-Four"

b.save()

b.title



