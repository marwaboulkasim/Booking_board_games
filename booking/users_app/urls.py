from django.urls import path
from . import views
# from .views import register_view

app_name = 'users_app'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    #path('create-booking/<int:table_id>/', views.create_booking, name='create_private_booking_user'),#marwa
    path('create-booking/<int:table_id>/', views.create_booking, name='create_booking'),

    #path('register/', views.logout_view, name='logout'),
]


