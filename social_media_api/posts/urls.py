from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CommentViewSet,
    FeedView,
    LikePostAPIView,
    PostViewSet,
    UnlikePostAPIView,
)

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("feed/", FeedView.as_view(), name="feed"),
    path("posts/<int:pk>/like/", LikePostAPIView.as_view(), name="like-post"),
    path("posts/<int:pk>/unlike/", UnlikePostAPIView.as_view(), name="unlike-post"),
]
