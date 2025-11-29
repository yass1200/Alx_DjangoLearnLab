# Filtering, Searching, and Ordering Documentation

## Book API Advanced Query Capabilities

### Filtering
Filter books using various criteria:

**Basic Filters:**
- `?title=harry` - Books with "harry" in title
- `?author__name=rowling` - Books by authors with "rowling" in name
- `?publication_year=1997` - Books published exactly in 1997

**Range Filters:**
- `?publication_year__gte=1990` - Books published in or after 1990
- `?publication_year__lte=2000` - Books published in or before 2000
- `?publication_year__gte=1990&publication_year__lte=2000` - Books between 1990-2000

### Searching
Search across multiple fields:
- `?search=potter` - Search in title and author name fields

### Ordering
Sort results by any field:
- `?ordering=title` - Sort by title (A-Z)
- `?ordering=-title` - Sort by title descending (Z-A)
- `?ordering=publication_year` - Sort by publication year (oldest first)
- `?ordering=-publication_year` - Sort by publication year (newest first)

### Combined Examples:
- `?search=magic&publication_year__gte=1990&ordering=-publication_year`
- `?author__name=tolkien&ordering=title`

## API Endpoints Summary

### Books:
- `GET /api/books/` - List all books with filtering, searching, ordering
- `GET /api/books/<id>/` - Get specific book
- `POST /api/books/create/` - Create new book (authenticated)
- `PUT /api/books/update/<id>/` - Update book (authenticated)
- `DELETE /api/books/delete/<id>/` - Delete book (authenticated)

### Authors:
- `GET /api/authors/` - List all authors
- `GET /api/authors/<id>/` - Get specific author
