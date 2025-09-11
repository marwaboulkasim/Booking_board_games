from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import CustomUserCreationForm
from tables_app.models import Table, Booking
import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from tables_app.models import Customer, Table, Booking


def home(request):
    return render(request, "home.html")

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
    return render(request, 'users_app/register.html', {'form': form})

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
    return render(request, 'users_app/login.html', {'form': form})

# --- Déconnexion ---
def logout_view(request):
    logout(request)
    return redirect('tables_app:home')

# --- Création d'une réservation (privée ou publique) ---@login_required

@login_required
def create_booking(request, table_id):
    table = get_object_or_404(Table, id=table_id)

    # Récupérer le Customer correspondant au User connecté
    try:
        customer = Customer.objects.get(email=request.user.email)
    except Customer.DoesNotExist:
        # Crée un Customer minimal si aucun trouvé
        customer = Customer.objects.create(
            pseudo=request.user.username,
            email=request.user.email,
            first_name=getattr(request.user, 'first_name', ''),
            last_name=getattr(request.user, 'last_name', ''),
            password=''  # Placeholder, pas utilisé
        )

    if request.method == "POST":
        date_str = request.POST.get("date")
        start_time_str = request.POST.get("start_time")
        duration_str = request.POST.get("duration")
        booking_type = request.POST.get("booking_type")

        # --- Conversion de la date ---
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            try:
                date = datetime.datetime.strptime(date_str, "%b. %d, %Y").date()
            except ValueError:
                messages.error(request, "Format de date invalide.")
                return redirect("tables_app:calendar")

        # --- Conversion de l'heure de début ---
        start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()

        # --- Conversion de la durée ---
        h, m, s = map(int, duration_str.split(":"))
        duration = datetime.timedelta(hours=h, minutes=m, seconds=s)

        # Création de la réservation
        booking = Booking.objects.create(
            table=table,
            main_customer=customer,
            date=date,
            start_time=start_time,
            duration=duration,
            booking_type=booking_type,
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
