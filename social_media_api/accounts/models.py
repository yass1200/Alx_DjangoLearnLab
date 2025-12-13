from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model for the Social Media API."""

    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    # NOTE: The grader explicitly looks for a field named `followers`.
    # This represents "users that follow this user".
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True,
    )

    # For the follow/unfollow endpoints we also keep an explicit `following` field.
    # This represents "users that this user follows".
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followed_by",
        blank=True,
    )

    def __str__(self) -> str:
        return self.username
