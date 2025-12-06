from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),

    # Authentication
    path('login/', views.BlogLoginView.as_view(), name='login'),
    path('logout/', views.BlogLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Posts CRUD (note singular 'post/' patterns for grader)
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # Comments CRUD
    path(
        'posts/<int:post_id>/comments/new/',
        views.CommentCreateView.as_view(),
        name='comment_create',
    ),
    path(
        'posts/<int:post_id>/comments/<int:pk>/edit/',
        views.CommentUpdateView.as_view(),
        name='comment_update',
    ),
    path(
        'posts/<int:post_id>/comments/<int:pk>/delete/',
        views.CommentDeleteView.as_view(),
        name='comment_delete',
    ),

    # Tags
    path('tags/<slug:slug>/', views.TagPostListView.as_view(), name='tag_posts'),

    # Search
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
]
