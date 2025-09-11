from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ProfileForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from tables_app.models import Table, Booking
from users_app.forms import EditBookingForm
import datetime
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import random
import string




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
        if "update_profile" in request.POST:  # bouton infos perso
            form = ProfileForm(request.POST, instance=user)
            password_form = PasswordChangeForm(user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profil mis à jour avec succès ✅")
                return redirect('users_app:profile')

        elif "update_password" in request.POST:  # bouton mot de passe
            form = ProfileForm(instance=user)
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # évite la déconnexion
                messages.success(request, "Mot de passe changé avec succès 🔑")
                return redirect('users_app:profile')

    else:
        form = ProfileForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'users_app/profile.html', {
        'form': form,
        'password_form': password_form
    })

import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from tables_app.models import Table, Booking
import datetime

# Créneaux disponibles
TIME_SLOTS = {
    "14h-18h": (datetime.time(14, 0), datetime.time(18, 0)),
    "18h-20h": (datetime.time(18, 0), datetime.time(20, 0)),
    "20h-00h": (datetime.time(20, 0), datetime.time(0, 0)),  # minuit
}

@login_required
def create_booking(request, table_id):
    table = get_object_or_404(Table, id=table_id)

    if request.method == "POST":
        date_str = request.POST.get("date")
        slot_label = request.POST.get("slot_label")
        booking_type = request.POST.get("booking_type")

        if not date_str or not slot_label or slot_label not in TIME_SLOTS:
            return redirect("tables_app:calendar")

        # Convertir la date
        try:
            selected_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.localdate()

        start_time, end_time = TIME_SLOTS[slot_label]

        # Durée
        if end_time == datetime.time(0, 0):
            end_dt = datetime.datetime.combine(selected_date + datetime.timedelta(days=1), end_time)
        else:
            end_dt = datetime.datetime.combine(selected_date, end_time)
        start_dt = datetime.datetime.combine(selected_date, start_time)
        duration = end_dt - start_dt

        # Vérification du chevauchement
        overlapping = Booking.objects.filter(
            table=table,
            date=selected_date,
            start_time__lt=end_dt.time(),
        ).exclude(
            start_time__gte=end_dt.time()
        )

        if overlapping.exists():
            return render(request, "users_app/booking_error.html", {
                "message": f"Le créneau {slot_label} est déjà réservé pour cette table."
            })

        # Génération du code uniquement si réservation privée
        booking_code = None
        if booking_type == "privée":
            booking_code = str(uuid.uuid4())[:8]  # Exemple : code unique court

        # Création de la réservation
        booking = Booking.objects.create(
            table=table,
            main_customer=request.user,
            date=selected_date,
            start_time=start_time,
            duration=duration,
            booking_type=booking_type,
            code=booking_code,  # ← ajouté
        )

        return redirect("tables_app:booking_confirmation", booking_id=booking.id)

    return redirect("tables_app:calendar")



# --- BOOKING CONFIRMATION ---
@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "tables_app/booking_confirmation.html", {"booking": booking})

# --- Page gestion des réservations (User) --- #

@login_required
def my_booking_view(request):
    bookings = Booking.objects.filter(main_customer=request.user).select_related('table')
    return render(request, 'users_app/my_bookings.html', {'bookings': bookings})

# --- Modification de réservation --- #
@login_required
def edit_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, main_customer=request.user)

    if request.method == "POST":
        form = EditBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Réservation mise à jour avec succès !")
            return redirect("users_app:my_bookings")
    else:
        form = EditBookingForm(instance=booking)

    return render(request, "users_app/edit_booking.html", {"form": form, "booking": booking})

# --- Suppression de réservation --- #

@login_required
def delete_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, main_customer=request.user)
    if request.method == "POST":
        booking.delete()
        messages.success(request, "Réservation supprimée !")
        return redirect("users_app:my_bookings")
    return render(request, "users_app/delete_booking_confirm.html", {"booking": booking})
