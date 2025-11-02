\# CREATE



```python

from bookshelf.models import Book

b = Book.objects.create(title="1984", author="George Orwell", publication\_year=1949)

b.id



