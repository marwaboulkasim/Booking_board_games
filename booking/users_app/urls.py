from django.urls import path
from . import views
# from .views import register_view

app_name = 'users_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    #path('create-booking/<int:table_id>/', views.create_booking, name='create_private_booking_user'),#marwa
    path('create-booking/<int:table_id>/', views.create_booking, name='create_booking'),
    path("confirmation/<int:booking_id>/", views.booking_confirmation, name="booking_confirmation"),
    path('my_bookings/', views.my_booking_view, name='my_bookings'),
    path('booking/edit/<int:booking_id>/', views.edit_booking_view, name='edit_booking'),
    path('booking/delete/<int:booking_id>/', views.delete_booking_view, name='delete_booking'),
]


