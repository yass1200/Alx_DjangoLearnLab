# --- Role-based profile model ---
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# relationship_app/models.py
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    # clé étrangère vers Author (un auteur -> plusieurs livres)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f"{self.title} by {self.author}"


class Library(models.Model):
    name = models.CharField(max_length=255)
    # plusieurs livres peuvent être dans plusieurs bibliothèques
    books = models.ManyToManyField(Book, related_name="libraries", blank=True)

    def __str__(self):
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=255)
    # 1–à–1 : une bibliothèque a un seul bibliothécaire
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name="librarian")

    def __str__(self):
        return f"{self.name} ({self.library})"

class UserProfile(models.Model):
    ROLE_ADMIN = 'Admin'
    ROLE_LIBRARIAN = 'Librarian'
    ROLE_MEMBER = 'Member'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_LIBRARIAN, 'Librarian'),
        (ROLE_MEMBER, 'Member'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Auto-create profile for new users; ensure it exists for existing users
    UserProfile.objects.get_or_create(user=instance)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

    class Meta:
        # Custom permissions (different from Django’s default add/change/delete)
        permissions = (
            ("can_add_book", "Can add book (custom)"),
            ("can_change_book", "Can change book (custom)"),
            ("can_delete_book", "Can delete book (custom)"),
        )

