from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from tables_app.models import Table, Booking
import datetime


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
            return redirect('tables_app:calendar')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# --- Déconnexion ---
def logout_view(request):
    logout(request)
    return redirect('tables_app:calendar')

# --- Création d'une réservation (privée ou publique) ---
@login_required
def create_booking(request, table_id):
    table = get_object_or_404(Table, id=table_id)

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
        Booking.objects.create(
            table=table,
            main_customer=request.user.customer,  # Assurez-vous que User a un OneToOne vers Customer
            date=date,
            start_time=start_time,
            duration=duration,
            booking_type=booking_type
        )

    # Retour au calendrier après réservation
    return redirect('tables_app:calendar')
