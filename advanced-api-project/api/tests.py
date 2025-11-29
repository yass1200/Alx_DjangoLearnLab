from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Author, Book
from .test_data import create_test_data

class BookAPITestCase(APITestCase):
    """
    Test case for Book API endpoints including CRUD operations,
    filtering, searching, ordering, and authentication.
    """
    
    def setUp(self):
        """
        Set up test data before each test method
        """
        self.client = APIClient()
        self.test_data = create_test_data()
        
        # URLs
        self.book_list_url = reverse('book-list')
        self.book_create_url = reverse('book-create')
        
    def test_get_book_list_unauthenticated(self):
        """
        Test that unauthenticated users can access book list
        """
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # Should return all 4 test books
    
    def test_get_book_detail_unauthenticated(self):
        """
        Test that unauthenticated users can access book details
        """
        book = self.test_data['books'][0]
        url = reverse('book-detail', kwargs={'pk': book.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], book.title)
        self.assertEqual(response.data['publication_year'], book.publication_year)
    
    def test_create_book_authenticated(self):
        """
        Test that authenticated users can create books
        """
        user = self.test_data['users']['regular']
        self.client.force_authenticate(user=user)
        
        author = self.test_data['authors'][0]
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': author.id
        }
        
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 5)  # Original 4 + new book
        self.assertEqual(response.data['title'], 'New Test Book')
    
    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books
        """
        author = self.test_data['authors'][0]
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': author.id
        }
        
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_authenticated(self):
        """
        Test that authenticated users can update books
        """
        user = self.test_data['users']['regular']
        self.client.force_authenticate(user=user)
        
        book = self.test_data['books'][0]
        url = reverse('book-update', kwargs={'pk': book.id})
        data = {
            'title': 'Updated Book Title',
            'publication_year': book.publication_year,
            'author': book.author.id
        }
        
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, 'Updated Book Title')
    
    def test_delete_book_authenticated(self):
        """
        Test that authenticated users can delete books
        """
        user = self.test_data['users']['regular']
        self.client.force_authenticate(user=user)
        
        book = self.test_data['books'][0]
        url = reverse('book-delete', kwargs={'pk': book.id})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 3)  # Original 4 - 1 deleted
    
    def test_book_validation_future_publication_year(self):
        """
        Test that books with future publication years are rejected
        """
        user = self.test_data['users']['regular']
        self.client.force_authenticate(user=user)
        
        author = self.test_data['authors'][0]
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': author.id
        }
        
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)

class FilterSearchOrderTest(APITestCase):
    """
    Test filtering, searching, and ordering functionality
    """
    
    def setUp(self):
        self.client = APIClient()
        self.test_data = create_test_data()
        self.book_list_url = reverse('book-list')
    
    def test_filter_by_author(self):
        """
        Test filtering books by author name
        """
        response = self.client.get(self.book_list_url, {'author__name': 'Rowling'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 Harry Potter books
    
    def test_filter_by_publication_year(self):
        """
        Test filtering books by publication year
        """
        response = self.client.get(self.book_list_url, {'publication_year': 1997})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 1997)
    
    def test_search_functionality(self):
        """
        Test search across title and author fields
        """
        # Search in title
        response = self.client.get(self.book_list_url, {'search': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Search in author name
        response = self.client.get(self.book_list_url, {'search': 'Tolkien'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_ordering_by_title(self):
        """
        Test ordering books by title
        """
        response = self.client.get(self.book_list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))  # Should be in alphabetical order
    
    def test_ordering_by_publication_year_descending(self):
        """
        Test ordering books by publication year descending
        """
        response = self.client.get(self.book_list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))  # Should be in descending order

class AuthorAPITestCase(APITestCase):
    """
    Test case for Author API endpoints
    """
    
    def setUp(self):
        self.client = APIClient()
        self.test_data = create_test_data()
        self.author_list_url = reverse('author-list')
    
    def test_get_author_list(self):
        """
        Test retrieving author list
        """
        response = self.client.get(self.author_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Should return all 3 authors
    
    def test_get_author_detail(self):
        """
        Test retrieving specific author details
        """
        author = self.test_data['authors'][0]
        url = reverse('author-detail', kwargs={'pk': author.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], author.name)
        self.assertEqual(len(response.data['books']), 2)  # J.K. Rowling has 2 books

class ErrorHandlingTest(APITestCase):
    """
    Test error handling and edge cases
    """
    
    def setUp(self):
        self.client = APIClient()
        self.test_data = create_test_data()
    
    def test_get_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist
        """
        url = reverse('book-detail', kwargs={'pk': 9999})  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_nonexistent_book(self):
        """
        Test updating a book that doesn't exist
        """
        user = self.test_data['users']['regular']
        self.client.force_authenticate(user=user)
        
        url = reverse('book-update', kwargs={'pk': 9999})
        data = {'title': 'Updated Title', 'publication_year': 2023, 'author': 1}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_invalid_data_creation(self):
        """
        Test creating book with invalid data
        """
        user = self.test_data['users']['regular']
        self.client.force_authenticate(user=user)
        
        data = {
            'title': '',  # Empty title
            'publication_year': 'invalid_year',  # Invalid year
            'author': 9999  # Non-existent author
        }
        
        response = self.client.post(reverse('book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
