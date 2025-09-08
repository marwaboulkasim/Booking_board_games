from django.urls import path
from . import views

app_name = 'tables_app'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('about/', views.about_view, name='about'),
]
