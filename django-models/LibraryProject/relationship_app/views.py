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
# relationship_app/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def _has_role(user, role_name: str) -> bool:
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == role_name

# ---- Role-based views ----
@login_required
@user_passes_test(lambda u: _has_role(u, 'Admin'))
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(lambda u: _has_role(u, 'Librarian'))
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(lambda u: _has_role(u, 'Member'))
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
