# API Views Documentation

## Book Views

### BookListView
- **URL:** `/api/books/`
- **Method:** GET
- **Permissions:** AllowAny (Public access)
- **Description:** Retrieves all books with optional author filtering
- **Filtering:** Use `?author=1` to filter by author ID

### BookDetailView
- **URL:** `/api/books/<id>/`
- **Method:** GET
- **Permissions:** AllowAny (Public access)
- **Description:** Retrieves a single book by ID

### BookCreateView
- **URL:** `/api/books/create/`
- **Method:** POST
- **Permissions:** IsAuthenticated
- **Description:** Creates a new book (requires authentication)

### BookUpdateView
- **URL:** `/api/books/<id>/update/`
- **Method:** PUT, PATCH
- **Permissions:** IsAuthenticated
- **Description:** Updates an existing book (requires authentication)

### BookDeleteView
- **URL:** `/api/books/<id>/delete/`
- **Method:** DELETE
- **Permissions:** IsAuthenticated
- **Description:** Deletes a book (requires authentication)

## Custom Features
- **Validation:** Publication year cannot be in the future
- **Filtering:** Books can be filtered by author
- **Permissions:** Read-only for public, write operations require authentication
