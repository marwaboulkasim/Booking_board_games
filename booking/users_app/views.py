from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ProfileForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from tables_app.models import Table, Booking, Game
from django.urls import reverse
import datetime
import random
import string
from django.contrib.auth import get_user_model
from django.contrib import messages

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
    "14h-18h": (datetime.time(14, 0), datetime.time(18, 0)),
    "18h-20h": (datetime.time(18, 0), datetime.time(20, 0)),
    "20h-00h": (datetime.time(20, 0), datetime.time(0, 0)),  # minuit
}

#################### Créer une réservation ####################
@login_required
def create_booking(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    customer = request.user

    if request.method == "POST":
        date_str = request.POST.get("date")
        slot_label = request.POST.get("slot_label")
        booking_type = request.POST.get("booking_type")

        # --- Nouveaux champs pour le choix de jeu ---
        booking_choice = request.POST.get("booking_choice")  # "our_game" / "custom" / None
        game_id = request.POST.get("game_id")
        custom_game = request.POST.get("custom_game")

        # --- Conversion de la date ---
        try:
            selected_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Format de date invalide.")
            return redirect("tables_app:calendar")

        # --- Définition des créneaux horaires ---
        slots = {
            "14h-18h": (datetime.time(14, 0), datetime.time(18, 0)),
            "18h-20h": (datetime.time(18, 0), datetime.time(20, 0)),
            "20h-00h": (datetime.time(20, 0), datetime.time(23, 59)),
        }

        if slot_label not in slots:
            messages.error(request, "Créneau invalide.")
            return redirect("tables_app:calendar")

        start_time, end_time = slots[slot_label]

        # --- Vérification des conflits ---
        conflicts = Booking.objects.filter(
            table=table,
            date=selected_date,
            start_time__lt=end_time,
            start_time__gte=start_time
        )
        if conflicts.exists():
            messages.error(request, f"Le créneau {slot_label} est déjà réservé pour cette table.")
            return redirect("tables_app:calendar")

        # --- Création de la réservation ---
        booking = Booking(
            table=table,
            main_customer=customer,
            date=selected_date,
            start_time=start_time,
            duration=datetime.timedelta(
                hours=(end_time.hour - start_time.hour),
                minutes=(end_time.minute - start_time.minute)
            ),
            booking_type=booking_type
        )

        # 🎲 Gérer le choix du jeu
        if booking_choice == "our_game" and game_id:
            booking.game_id = int(game_id)  # conversion en int pour ForeignKey
        elif booking_choice == "custom" and custom_game:
            booking.custom_game = custom_game

        # --- Sauvegarde de la réservation ---
        booking.save()

        # Si réservation privée → générer un code
        if booking.booking_type == "privée" and not booking.code:
            booking.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            booking.save()

        return redirect(reverse("users_app:booking_confirmation", args=[booking.id]))

    return redirect("tables_app:calendar")

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

