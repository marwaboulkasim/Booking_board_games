from django.urls import path
from . import views
# from .views import register_view

app_name = 'users_app'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-booking/<int:table_id>/', views.create_private_booking_user, name='create_private_booking_user'),#marwa

    #path('register/', views.logout_view, name='logout'),
]



