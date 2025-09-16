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
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("my-bookings/<int:booking_id>/edit/", views.edit_booking, name="edit_booking"),
    path('my-bookings/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
    path('join-public-booking/<int:booking_id>/', views.join_public_booking, name='join_public_booking'),
    path('leave-public-booking/<int:booking_id>/', views.leave_public_booking, name='leave_public_booking'),

]


