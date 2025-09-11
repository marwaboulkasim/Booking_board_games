from django.shortcuts import render, get_object_or_404
from .models import Table, Booking, BookingType
import datetime

# --- Accueil ---
def home_view(request):
    return render(request, 'tables_app/home.html')

# --- Calendrier ---
def calendar_view(request):
    # Lecture de la date depuis l'URL (?date=YYYY-MM-DD)
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = datetime.date.today()
    else:
        selected_date = datetime.date.today()
    
    # Récupérer toutes les réservations pour le jour sélectionné
    reservations = Booking.objects.filter(date=selected_date).select_related('table')
    
    # Construction de l'état des tables
    tables_state = []
    for table in Table.objects.all():
        # Vérifie si une réservation existe pour cette table
        res = reservations.filter(table=table).first()
        if res:
            state = res.booking_type  # "privée" ou "publique"
        else:
            state = 'Libre'
        tables_state.append({'table': table, 'state': state})

    # Debug : affiche la liste des tables avec leur état
    print(tables_state)

    # Rendu du template
    return render(request, 'tables_app/calendar.html', {
        'date': selected_date,
        'tables': tables_state,
    })
# --- Confirmation de réservation ---#
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "tables_app/booking_confirmation.html", {
        "booking": booking
    })

# --- Nos jeux disponibles ---
from django.shortcuts import render, get_object_or_404
from tables_app.models import Game

def games(request):
    # Récupérer les filtres GET
    category = request.GET.get("category")
    players = request.GET.get("players")
    max_players = request.GET.get("max_players")
    duration = request.GET.get("duration")

    # Base queryset
    games = Game.objects.all()

    # Appliquer les filtres existants
    if category:
        games = games.filter(category_game=category)
    if players:
        games = games.filter(nb_player_min_game__lte=int(players))
    
    # Nouveaux filtres
    if max_players:
        games = games.filter(nb_player_max_game__gte=int(max_players))
    if duration:
        games = games.filter(duration_game__icontains=duration)

    # Options dynamiques pour le formulaire
    categories = Game.objects.values_list("category_game", flat=True).distinct()
    player_options = sorted(Game.objects.values_list("nb_player_min_game", flat=True).distinct())
    max_player_options = sorted(Game.objects.values_list("nb_player_max_game", flat=True).distinct())
    duration_options = Game.objects.values_list("duration_game", flat=True).distinct()

    context = {
        "games": games,
        "categories": categories,
        "player_options": player_options,
        "max_player_options": max_player_options,
        "duration_options": duration_options,
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
