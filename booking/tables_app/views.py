from django.shortcuts import render, get_object_or_404
from .models import Table, Booking, BookingType, Game
from datetime import datetime, date, time


# --- Accueil ---
def home_view(request):
    return render(request, 'tables_app/home.html')


# --- Calendrier ---
def calendar_view(request):
    # Lecture de la date depuis l'URL (?date=YYYY-MM-DD)
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    # Définition des créneaux horaires
    slots = [
        {"label": "14h-18h", "start": time(14, 0), "end": time(18, 0)},
        {"label": "18h-20h", "start": time(18, 0), "end": time(20, 0)},
        {"label": "20h-00h", "start": time(20, 0), "end": time(23, 59)},
    ]

    tables_data = []

    for table in Table.objects.all():
        table_slots = []
        for slot in slots:
            # Vérifier si une réservation existe pour ce créneau
            conflicts = Booking.objects.filter(
                table=table,
                date=selected_date,
            ).filter(
                start_time__lt=slot["end"],
                start_time__gte=slot["start"]
            )

            if conflicts.exists():
                state = conflicts.first().booking_type
                available = False
            else:
                state = 'Libre'
                available = True

            table_slots.append({
                "slot_label": slot["label"],
                "state": state,
                "available": available,
            })

        tables_data.append({
            "table": table,
            "slots": table_slots
        })

    # Récupérer les réservations de l’utilisateur connecté
    user_reservations = None
    if request.user.is_authenticated:
        user_reservations = Booking.objects.filter(
            main_customer=request.user
        ).order_by('-date', 'start_time')

    context = {
        "date": selected_date,
        "tables": tables_data,
        "user_reservations": user_reservations,
    }
    return render(request, "tables_app/calendar.html", context)


# --- Confirmation de réservation ---
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "tables_app/booking_confirmation.html", {
        "booking": booking
    })


# --- Nos jeux disponibles ---
def games(request):
    # Récupérer les filtres GET
    category = request.GET.get("category")
    players = request.GET.get("players")
    max_players = request.GET.get("max_players")
    duration = request.GET.get("duration")

    games_qs = Game.objects.all()

    if category:
        games_qs = games_qs.filter(category_game=category)
    if players:
        games_qs = games_qs.filter(nb_player_min_game__lte=int(players))
    if max_players:
        games_qs = games_qs.filter(nb_player_max_game__gte=int(max_players))
    if duration:
        games_qs = games_qs.filter(duration_game__icontains=duration)

    context = {
        "games": games_qs,
        "categories": Game.objects.values_list("category_game", flat=True).distinct(),
        "player_options": sorted(Game.objects.values_list("nb_player_min_game", flat=True).distinct()),
        "max_player_options": sorted(Game.objects.values_list("nb_player_max_game", flat=True).distinct()),
        "duration_options": Game.objects.values_list("duration_game", flat=True).distinct(),
    }

    return render(request, "tables_app/game.html", context)


def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, "tables_app/game_detail.html", {"game": game})


# --- Pages supplémentaires ---
def about_view(request):
    return render(request, 'tables_app/about.html')

def games_view(request):
    return render(request, 'tables_app/games.html')

def book_table_view(request):
    return render(request, 'tables_app/book_table.html')

def contact_view(request):
    return render(request, 'tables_app:contact.html')

def account_view(request):
    return render(request, 'tables_app/account.html')
