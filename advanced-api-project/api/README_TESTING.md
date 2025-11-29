# Unit Testing Documentation

## Testing Strategy

This test suite comprehensively tests the Book API endpoints, covering:

### 1. CRUD Operations
- **Create**: Authenticated users can create books with valid data
- **Read**: All users can read book lists and details
- **Update**: Authenticated users can update existing books
- **Delete**: Authenticated users can delete books

### 2. Authentication & Permissions
- Unauthenticated users can only read data
- Authenticated users can perform all CRUD operations
- Proper error handling for unauthorized access

### 3. Filtering, Searching & Ordering
- **Filtering**: By author name, publication year
- **Searching**: Across title and author fields
- **Ordering**: By title, publication year (ascending/descending)

### 4. Error Handling
- Invalid data validation
- Non-existent resource access
- Future publication year prevention

## Running Tests

### Run All Tests
```bash
python manage.py test api
