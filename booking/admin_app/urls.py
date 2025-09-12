from django.urls import path
from . import views

app_name = "admin_app"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("reservations/", views.manage_reservations, name="manage_reservations"),
    path("users/", views.manage_users, name="manage_users"),
    path("games/", views.manage_games, name="manage_games"),

]
