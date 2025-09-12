from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


@staff_member_required
def dashboard(request):
    return render(request, "admin_app/dashboard.html")

@staff_member_required
def manage_reservations(request):
    # logique pour gérer les réservations
    return render(request, "admin_app/manage_reservations.html")

@staff_member_required
def manage_users(request):
    # logique pour gérer les utilisateurs
    return render(request, "admin_app/manage_users.html")

@staff_member_required
def manage_games(request):
    # logique pour gérer les jeux
    return render(request, "admin_app/manage_games.html")





def add_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if username and email and password:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Utilisateur ajouté avec succès !")
            return redirect("admin_app:manage_users")
        else:
            messages.error(request, "Tous les champs sont requis.")
    return render(request, "admin_app/add_user.html")
