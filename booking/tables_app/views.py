# tables_app/views.py
from django.shortcuts import render
from .models import Table, Booking, BookingType
import datetime

def home_view(request):
    return render(request, 'tables_app/home.html')

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
