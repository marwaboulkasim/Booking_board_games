from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ProfileForm, PasswordChangeForm, EditBookingForm
from django.contrib.auth import update_session_auth_hash
from tables_app.models import Table, Booking, Game
from users_app.forms import EditBookingForm
from datetime import datetime, time, timedelta
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model
import random
import string
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponseForbidden



# --- HOME ---
def home(request):
    return render(request, "home.html")

# --- REGISTER ---
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tables_app:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users_app/register.html', {'form': form})

# --- LOGIN ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tables_app:home')
    else:
        form = AuthenticationForm()
    return render(request, 'users_app/login.html', {'form': form})

# --- LOGOUT ---
def logout_view(request):
    logout(request)
    return redirect('tables_app:home')


# --- Gestion profil user ---#
# --- PROFILE ---
@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        if "update_profile" in request.POST:
            form = ProfileForm(request.POST, instance=user)
            password_form = PasswordChangeForm(user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profil mis à jour avec succès ✅")
                return redirect('users_app:profile')

        elif "update_password" in request.POST:
            form = ProfileForm(instance=user)
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Mot de passe changé avec succès 🔑")
                return redirect('users_app:profile')

    else:
        form = ProfileForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'users_app/profile.html', {
        'form': form,
        'password_form': password_form
    })

# --- Créneaux disponibles ---
TIME_SLOTS = {
    "14h-18h": (time(14, 0), time(18, 0)),
    "18h-20h": (time(18, 0), time(20, 0)),
    "20h-00h": (time(20, 0), time(0, 0)),

}

# ####### CREER UNE RESA ######

@login_required
def create_booking(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    customer = request.user

    if request.method == "POST":
        date_str = request.POST.get("date")
        slot_label = request.POST.get("slot_label")
        booking_type = request.POST.get("booking_type")

        # --- Nouveaux champs pour le choix de jeu ---
        booking_choice = request.POST.get("booking_choice")  # "our_game" / "custom"
        game_id = request.POST.get("game_id") or request.POST.get("game")
        custom_game = request.POST.get("custom_game")
        max_players_input = request.POST.get("max_players")

        # --- Conversion de la date ---
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Format de date invalide.")
            return redirect("tables_app:calendar")

        # --- Définition des créneaux horaires ---
        slots = {
            "14h-18h": (time(14, 0), time(18, 0)),
            "18h-20h": (time(18, 0), time(20, 0)),
            "20h-00h": (time(20, 0), time(0, 0)),
        }

        if slot_label not in slots:
            messages.error(request, "Créneau invalide.")
            return redirect("tables_app:calendar")

        start_time, end_time = slots[slot_label]
        start_dt = datetime.combine(selected_date, start_time)
        end_dt = datetime.combine(selected_date, end_time)

        # --- Vérification des conflits ---
        existing = Booking.objects.filter(table=table, date=selected_date)
        for b in existing:
            b_start = datetime.combine(b.date, b.start_time)
            b_end = b_start + b.duration
            if not (b_end <= start_dt or b_start >= end_dt):  # chevauchement
                messages.error(request, f"Le créneau {slot_label} est déjà réservé pour cette table.")
                return redirect("tables_app:calendar")

        # --- Gestion jeu ---
        game = None
        if booking_type == "publique":
            # Obligatoire : un jeu choisi
            if not (game_id or custom_game):
                messages.error(request, "Sélectionnez un jeu pour une table publique.")
                return redirect("tables_app:calendar")

            # Jeu de la base
            if booking_choice == "our_game" and game_id:
                game = get_object_or_404(Game, id=game_id)

        # --- Définition des places max pour table publique ---
        mp = None
        if booking_type == "publique":
            try:
                mp = int(max_players_input) if max_players_input else None
            except ValueError:
                mp = None

            # fallback sur jeu si utilisateur n’a rien rempli
            if mp is None and game and hasattr(game, "nb_player_max_game"):
                mp = game.nb_player_max_game

            # limiter à la capacité de la table si nécessaire
            if getattr(table, "capacity_table", None) and mp:
                mp = min(mp, table.capacity_table)

        # --- Création de la réservation ---
        booking = Booking(
            table=table,
            main_customer=customer,
            date=selected_date,
            start_time=start_time,
            duration=end_dt - start_dt,
            booking_type=booking_type,
            game=game if booking_type == "publique" else None,
            custom_game=custom_game if booking_type == "publique" else None,
            max_players=mp if booking_type == "publique" else None,
        )

        # --- Code pour réservation privée ---
        if booking_type == "privée" and not booking.code:
            booking.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # --- Sauvegarde finale ---
        booking.save()

        return redirect(reverse("users_app:booking_confirmation", args=[booking.id]))

    return redirect("tables_app:calendar")




##### Rejoindre / Quitter une table publique ####
@require_POST
@login_required
def join_public_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, booking_type='publique')

    # Vérifier qu’il reste de la place
    if booking.participants.count() + 1 >= booking.max_players:
        return JsonResponse({"error": "Table complète"}, status=400)

    # Ajouter le joueur
    booking.participants.add(request.user)
    return JsonResponse({"success": True})


@login_required
def leave_public_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, booking_type='publique')
    if booking.participants.filter(id=request.user.id).exists():
        booking.participants.remove(request.user)
        messages.success(request, "Vous avez quitté la table.")
    else:
        messages.info(request, "Vous n'étiez pas inscrit sur cette table.")
    return redirect('users_app:my_bookings')

#################

# --- BOOKING CONFIRMATION ---
@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # Déterminer le jeu réservé
    if booking.game:  # Jeu du catalogue
        game_name = booking.game.name_game
    elif booking.custom_game:  # Jeu apporté par l'utilisateur
        game_name = booking.custom_game
    else:
        game_name = "Aucun"

    return render(request, "tables_app/booking_confirmation.html", {
        "booking": booking,
        "game_name": game_name
    })



# --- MES RESERVATIONS ---
# @login_required
# def my_bookings(request):
#     bookings = Booking.objects.filter(main_customer=request.user).select_related('table')
#     return render(request, "users_app/my_bookings.html", {"bookings": bookings})

@login_required
def my_bookings(request):
    # Récupérer toutes les réservations où l'utilisateur est créateur ou participant
    bookings = Booking.objects.filter(
        Q(main_customer=request.user) | Q(participants=request.user)
    ).select_related('table').order_by('-date', 'start_time')

    return render(request, "users_app/my_bookings.html", {"bookings": bookings})

# --- MODIFICATION DES RESERVATIONS --- 
@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, main_customer=request.user)

    if request.method == "POST":
        form = EditBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Réservation mise à jour ✅")
            return redirect("users_app:my_bookings")
    else:
        form = EditBookingForm(instance=booking)

    return render(request, "users_app/edit_booking.html", {"form": form, "booking": booking})

# --- ANNULATION DES RESERVATIONS --- 

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Vérifie que l'utilisateur est bien le propriétaire
    if booking.main_customer != request.user:
        return HttpResponseForbidden("Vous n'avez pas le droit de supprimer cette réservation.")

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Réservation supprimée avec succès.")
        return redirect('users_app:my_bookings')

    return render(request, "users_app/confirm_delete.html", {"booking": booking})


