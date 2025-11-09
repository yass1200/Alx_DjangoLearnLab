from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView

# --- Registration (function-based) ---
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally log the user in right after registering:
            login(request, user)
            return redirect('list_books')   # or any page you want
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# --- Login / Logout (class-based, built-ins) ---
class AppLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class AppLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'
