# tables_app/views.py
from django.shortcuts import render

def home_view(request):
    return render(request, 'tables_app/home.html')

