from django.urls import path
from . import views

app_name = 'tables_app'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('about/', views.about_view, name='about'),
    path("games/", views.games, name="games"),
    path("games/<int:game_id>/", views.game_detail, name="game_detail"),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    


    
]


