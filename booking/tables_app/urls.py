# tables_app/urls.py
from django.urls import path
from . import views

app_name = "tables_app"

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', views.calendar_view, name='calendar'),
#     path('api/calendar/', views.api_calendar, name='api_calendar'),
#     path('create/', views.calendar_reservation_view, name='create_reservation'),
#     path('join/', views.join_reservation, name='join_reservation'),
#     path('leave/', views.leave_reservation, name='leave_reservation')
]
