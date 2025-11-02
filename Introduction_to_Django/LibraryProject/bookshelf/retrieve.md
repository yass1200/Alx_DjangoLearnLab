# RETRIEVE

```python
from bookshelf.models import Book
b = Book.objects.get(id=2)
b.title, b.author, b.publication_year
