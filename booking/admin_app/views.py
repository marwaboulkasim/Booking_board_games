from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

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
