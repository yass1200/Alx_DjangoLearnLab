# RETRIEVE

```python
from bookshelf.models import Book
b = Book.objects.get(title="1984")
b.title, b.author, b.publication_year
