from django.contrib.auth.models import User
from .models import Author, Book

def create_test_data():
    """
    Create test data for unit tests
    """
    # Create test users
    user1 = User.objects.create_user(
        username='testuser', 
        password='testpass123',
        email='test@example.com'
    )
    user2 = User.objects.create_user(
        username='adminuser', 
        password='adminpass123',
        email='admin@example.com',
        is_staff=True
    )
    
    # Create test authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="J.R.R. Tolkien")
    author3 = Author.objects.create(name="George Orwell")
    
    # Create test books
    book1 = Book.objects.create(
        title="Harry Potter and the Philosopher's Stone",
        publication_year=1997,
        author=author1
    )
    book2 = Book.objects.create(
        title="Harry Potter and the Chamber of Secrets", 
        publication_year=1998,
        author=author1
    )
    book3 = Book.objects.create(
        title="The Hobbit",
        publication_year=1937,
        author=author2
    )
    book4 = Book.objects.create(
        title="1984",
        publication_year=1949,
        author=author3
    )
    
    return {
        'users': {'regular': user1, 'admin': user2},
        'authors': [author1, author2, author3],
        'books': [book1, book2, book3, book4]
    }
