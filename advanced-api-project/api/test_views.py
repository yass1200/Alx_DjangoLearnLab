from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Author, Book

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
        
        # Create test users
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="J.R.R. Tolkien")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="The Hobbit",
            publication_year=1937,
            author=self.author2
        )
        
        # URLs
        self.book_list_url = reverse('book-list')
        self.book_create_url = reverse('book-create')
    
    def test_get_book_list_unauthenticated(self):
        """
        Test that unauthenticated users can access book list - should return 200
        """
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data content
        self.assertIn('response.data', str(response.data))  # Check data exists
        self.assertTrue(len(response.data) > 0)  # Check data is not empty
    
    def test_get_book_detail_unauthenticated(self):
        """
        Test that unauthenticated users can access book details - should return 200
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data content
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author'], self.book1.author.id)
    
    def test_create_book_authenticated(self):
        """
        Test that authenticated users can create books - should return 201
        """
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check response data content
        self.assertEqual(response.data['title'], 'New Test Book')
        self.assertEqual(response.data['publication_year'], 2023)
        self.assertEqual(response.data['author'], self.author1.id)
    
    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books - should return 403
        """
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Check response data contains error detail
        self.assertIn('response.data', str(response.data))
        self.assertIn('detail', response.data)
    
    def test_update_book_authenticated(self):
        """
        Test that authenticated users can update books - should return 200
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Book Title',
            'publication_year': self.book1.publication_year,
            'author': self.book1.author.id
        }
        
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data content
        self.assertEqual(response.data['title'], 'Updated Book Title')
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
    
    def test_delete_book_authenticated(self):
        """
        Test that authenticated users can delete books - should return 204
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        initial_count = Book.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check that book was actually deleted
        self.assertEqual(Book.objects.count(), initial_count - 1)
    
    def test_book_validation_future_publication_year(self):
        """
        Test that books with future publication years are rejected - should return 400
        """
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check response data contains validation error
        self.assertIn('publication_year', response.data)
        self.assertIn('response.data', str(response.data))

class FilterSearchOrderTest(APITestCase):
    """
    Test filtering, searching, and ordering functionality
    """
    
    def setUp(self):
        self.client = APIClient()
        
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="J.R.R. Tolkien")
        
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="The Hobbit",
            publication_year=1937,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            publication_year=1998,
            author=self.author1
        )
        
        self.book_list_url = reverse('book-list')
    
    def test_filter_by_author(self):
        """
        Test filtering books by author name - should return 200
        """
        response = self.client.get(self.book_list_url, {'author__name': 'Rowling'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data contains filtered results
        self.assertTrue(len(response.data) > 0)
        for book in response.data:
            self.assertEqual(book['author'], self.author1.id)
    
    def test_filter_by_publication_year(self):
        """
        Test filtering books by publication year - should return 200
        """
        response = self.client.get(self.book_list_url, {'publication_year': 1997})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data contains correct year
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 1997)
    
    def test_search_functionality_title(self):
        """
        Test search across title fields - should return 200
        """
        response = self.client.get(self.book_list_url, {'search': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data contains search results
        self.assertTrue(len(response.data) > 0)
        for book in response.data:
            self.assertIn('Harry', book['title'])
    
    def test_search_functionality_author(self):
        """
        Test search across author fields - should return 200
        """
        response = self.client.get(self.book_list_url, {'search': 'Tolkien'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data contains author search results
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author2.id)
    
    def test_ordering_by_title_ascending(self):
        """
        Test ordering books by title ascending - should return 200
        """
        response = self.client.get(self.book_list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data is properly ordered
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_by_publication_year_descending(self):
        """
        Test ordering books by publication year descending - should return 200
        """
        response = self.client.get(self.book_list_url, {'ordering': '-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data is properly ordered
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

class ErrorHandlingTest(APITestCase):
    """
    Test error handling and edge cases
    """
    
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
    
    def test_get_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist - should return 404
        """
        url = reverse('book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Check response data contains error detail
        self.assertIn('response.data', str(response.data))
        self.assertIn('detail', response.data)
    
    def test_update_nonexistent_book(self):
        """
        Test updating a book that doesn't exist - should return 404
        """
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        
        url = reverse('book-update', kwargs={'pk': 9999})
        data = {'title': 'Updated Title', 'publication_year': 2023, 'author': self.author.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Check response data contains error detail
        self.assertIn('response.data', str(response.data))
    
    def test_invalid_data_creation(self):
        """
        Test creating book with invalid data - should return 400
        """
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        
        data = {
            'title': '',  # Empty title
            'publication_year': 'invalid_year',  # Invalid year
            'author': 9999  # Non-existent author
        }
        
        response = self.client.post(reverse('book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check response data contains validation errors
        self.assertIn('response.data', str(response.data))
        self.assertIn('title', response.data)
        self.assertIn('publication_year', response.data)
        self.assertIn('author', response.data)
