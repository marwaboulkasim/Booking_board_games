from django.contrib import admin
from django.urls import path, include
from tables_app import views as table_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tables_app.urls')),       # tables_app gère home, calendar, about
    path('users/', include('users_app.urls')),  # users_app gère auth + profil
    path('contact/', include('contact_app.urls')) # contact
]


