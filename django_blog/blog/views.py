from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Post
"""
Views for Django Blog authentication
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm
from .models import Post, Profile

def home_view(request):
    """
    Home page view showing recent posts
    """
    posts = Post.objects.all().order_by('-published_date')[:5]
    return render(request, 'blog/home.html', {'posts': posts})

def posts_view(request):
    """
    View all blog posts
    """
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/posts.html', {'posts': posts})

def register_view(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, 
                f'Account created for {username}! You can now log in.'
            )
            return redirect('login')
        else:
            messages.error(
                request, 
                'Please correct the errors below.'
            )
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    """
    User login view
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')

@login_required
def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile_view(request):
    """
    User profile view
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'registration/profile.html', {'form': form})
