from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ProfileForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
#marwa
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tables_app:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tables_app:home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('tables_app:home')
#fin marwa

@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            return redirect('users_app:profile')
    else:
        form = ProfileForm(instance=user)
        password_form = PasswordChangeForm(user)
    return render(request, 'users_app/profile.html', {
        'form': form,
        'password_form': password_form
    })