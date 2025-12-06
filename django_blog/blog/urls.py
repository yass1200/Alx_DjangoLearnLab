from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home page
    path('', views.home_view, name='home'),
    
    # Blog posts
    path('posts/', views.posts_view, name='posts'),
    
    # Authentication - using Django's built-in views
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
]
