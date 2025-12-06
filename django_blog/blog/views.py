from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Post

def home_view(request):
    return render(request, 'blog/home.html')

def posts_view(request):
    posts = Post.objects.all()
    return render(request, 'blog/posts.html', {'posts': posts})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'registration/profile.html')
