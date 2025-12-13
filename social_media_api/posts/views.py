from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.utils import create_notification


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def feed(self, request):
        following_ids = request.user.following.values_list("id", flat=True)
        qs = Post.objects.filter(author_id__in=following_ids).select_related("author").order_by("-created_at")
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(PostSerializer(page, many=True).data)
        return Response(PostSerializer(qs, many=True).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if created and post.author_id != request.user.id:
            create_notification(recipient=post.author, actor=request.user, verb="liked your post", target=post)
        return Response({"detail": "ok"})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        Like.objects.filter(post=post, user=request.user).delete()
        return Response({"detail": "ok"})


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "post").all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    search_fields = ["content"]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        if comment.post.author_id != self.request.user.id:
            create_notification(recipient=comment.post.author, actor=self.request.user, verb="commented on your post", target=comment.post)
