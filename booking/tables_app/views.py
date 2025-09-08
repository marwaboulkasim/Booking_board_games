from django.shortcuts import render
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
    
    # Chargement des réservations du jour sélectionné
    reservations = Booking.objects.filter(date=selected_date).select_related('table')
    
    # Construction du statut des tables
    tables_state = []
    for table in Table.objects.all():
        res = reservations.filter(table=table).first()
        if res:
            state = res.get_type_reservation_display()
        else:
            state = 'Libre'
        tables_state.append({'table': table, 'state': state})
    
    # Rendu
    return render(request, 'tables_app/calendar.html', {
        'date': selected_date,
        'tables': tables_state,
    })


# --- Pages supplémentaires ---
def about_view(request):
    return render(request, 'tables_app/about.html')

def games_view(request):
    return render(request, 'tables_app/games.html')

def book_table_view(request):
    return render(request, 'tables_app/book_table.html')

def contact_view(request):
    return render(request, 'tables_app/contact.html')

def account_view(request):
    return render(request, 'tables_app/account.html')
