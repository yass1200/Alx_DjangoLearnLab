# Permissions & Groups (bookshelf)

Custom permissions on `bookshelf.models.Book`:
- `can_view`
- `can_create`
- `can_edit`
- `can_delete`

Views (decorated with `@permission_required`):
- `book_list`      -> `bookshelf.can_view`
- `add_book`       -> `bookshelf.can_create`
- `edit_book`      -> `bookshelf.can_edit`
- `delete_book`    -> `bookshelf.can_delete`

Suggested groups:
- **Viewers**: `can_view`
- **Editors**: `can_view`, `can_create`, `can_edit`
- **Admins** : `can_view`, `can_create`, `can_edit`, `can_delete`
