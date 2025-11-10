3. Implement Role-Based Access Control in Django
mandatory
Objective: Implement role-based access control within a Django application to manage different user roles and permissions effectively. You will extend the User model and create views that restrict access based on user roles.

Task Description:
In your Django project, you will extend the Django User model to include user roles and develop views that restrict access based on these roles. Your task is to set up this system by creating a new model for user profiles, defining views with access restrictions, and configuring URL patterns.

Step 1: Extend the User Model with a UserProfile
Create a UserProfile model that includes a role field with predefined roles. This model should be linked to Django’s built-in User model with a one-to-one relationship.

Fields Required:
user: OneToOneField linked to Django’s User.
role: CharField with choices for ‘Admin’, ‘Librarian’, and ‘Member’.
Automatic Creation: Use Django signals to automatically create a UserProfile when a new user is registered.
Step 2: Set Up Role-Based Views
Create three separate views to manage content access based on user roles:

Views to Implement:

An ‘Admin’ view that only users with the ‘Admin’ role can access, the name of the file should be admin_view
A ‘Librarian’ view accessible only to users identified as ‘Librarians’. The file should be named librarian_view
A ‘Member’ view for users with the ‘Member’ role, the name of the file should be member_view
Access Control:

Utilize the @user_passes_test decorator to check the user’s role before granting access to each view.
Step 3: Configure URL Patterns
Define URL patterns that will route to the newly created role-specific views. Ensure that each URL is correctly linked to its respective view and that the URLs are named for easy reference.

URLs to Define:
A URL for the ‘Admin’ view.
A URL for the ‘Librarian’ view.
A URL for the ‘Member’ view.
Step 4: Create Role-Based HTML Templates
For each role, create an HTML template to display relevant content when users access their respective views.

Templates to Create:

admin_view.html for Admin users.
librarian_view.html for Librarians.
member_view.html for Members.
Repo:

GitHub repository: Alx_DjangoLearnLab
Directory: django-models
File: models.py, views.py, urls.py