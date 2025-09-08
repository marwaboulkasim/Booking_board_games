from django.urls import path
from . import views

app_name = "tables_app" #get

urlpatterns = [
    path('', views.home_view, name='home'),
    path('calendar/', views.calendar_view, name='calendar') #get

]




