from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import CustomUserCreationForm
from tables_app.models import Customer, Table, Booking
import datetime
import random
import string

# --- Accueil ---
def home(request):
    return render(request, "home.html")

# --- Enregistrement ---
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tables_app:calendar')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# --- Connexion ---
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

# --- Déconnexion ---
def logout_view(request):
    logout(request)
    return redirect('tables_app:home')

# --- Création d'une réservation (privée uniquement) ---
@login_required
def create_booking(request, table_id):
    table = get_object_or_404(Table, id=table_id)

    # Récupérer ou créer le Customer correspondant au User connecté
    customer, _ = Customer.objects.get_or_create(
        email=request.user.email,
        defaults={
            'pseudo': request.user.username,
            'first_name': getattr(request.user, 'first_name', ''),
            'last_name': getattr(request.user, 'last_name', ''),
            'password': ''
        }
    )

    if request.method == "POST":
        date_str = request.POST.get("date")
        start_time_str = request.POST.get("start_time")
        duration_str = request.POST.get("duration")
        booking_type = request.POST.get("booking_type")

        # Conversion des chaînes en objets Python
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
        h, m, s = map(int, duration_str.split(":"))
        duration = datetime.timedelta(hours=h, minutes=m, seconds=s)

        # Création de la réservation
        booking = Booking.objects.create(
            table=table,
            main_customer=customer,
            date=date,
            start_time=start_time,
            duration=duration,
            booking_type=booking_type
        )

        # Si réservation privée, générer un code unique
        if booking.booking_type == "privée":
            booking.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            booking.save()

        # Redirection vers page de confirmation
        return redirect(reverse("users_app:booking_confirmation", args=[booking.id]))

    return redirect('tables_app:calendar')

# --- Page de confirmation ---
@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "tables_app/booking_confirmation.html", {"booking": booking})
