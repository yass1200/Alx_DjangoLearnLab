
from django.urls import path
from . import views

app_name = "blog"

from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # === AUTHENTICATION URLS (Task 1 expects these) ===
    path('login/', views.BlogLoginView.as_view(), name='login'),
    path('logout/', views.BlogLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # === POST CRUD (Task 2) ===
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('', views.PostListView.as_view(), name='post-list'),

    # === COMMENTS CRUD (Task 3 – note pk in URL) ===
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

    # === TAG FILTERING (Task 4 – exact string required) ===
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts-by-tag'),

    # === SEARCH (Task 4) ===
    path('search/', views.SearchResultsView.as_view(), name='search'),
]
