from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

"""
URL configuration for blog app
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and posts
    path('', views.home_view, name='home'),
    path('posts/', views.posts_view, name='posts'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
