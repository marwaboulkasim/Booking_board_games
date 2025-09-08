from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from tables_app.models import Table, Booking
import datetime

# --- Enregistrement ---
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


# --- Création d'une réservation privée ou publique ---
@login_required
def create_private_booking_user(request, table_id):
    table = get_object_or_404(Table, id=table_id)

    if request.method == "POST":
        booking_type = request.POST.get("booking_type")
        date_str = request.POST.get("date")
        start_time_str = request.POST.get("start_time")
        duration_str = request.POST.get("duration")

        # Conversion des chaînes en objets Python
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
        h, m, s = map(int, duration_str.split(":"))
        duration = datetime.timedelta(hours=h, minutes=m, seconds=s)

        # Création de la réservation
        Booking.objects.create(
            date=date,
            start_time=start_time,
            duration=duration,
            booking_type=booking_type,
            table=table,
            main_customer=request.user.customer  # Assure-toi que User a une relation OneToOne vers Customer
        )

    return redirect('tables_app:calendar')  # Retour au calendrier après réservation
