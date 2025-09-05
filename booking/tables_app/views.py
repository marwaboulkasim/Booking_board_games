# tables_app/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import Table
import datetime

def home(request):
    return render(request, 'tables_app/home.html')



# page calendrier
@login_required
def calendar_view(request):
    # Récupération du paramètre GET ?date=YYYY-MM-DD
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponseBadRequest('Format de date invalide : Utiliser YYYY-MM-DD.')
    else:
        selected_date = datetime.date.today() # par défaut = aujourd'hui
    
    # Chargement de l'état des tables
    tables = Table.objects.all()
    
    #  Template
    return render(request, 'tables_app/calendar.html', {
        'date': selected_date,
        'tables': tables
    })
