from django.contrib import admin
from django.urls import path, include
from tables_app import views as table_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tables_app.urls')),     # accueil
    path('users/', include('users_app.urls')), # auth
    path('calendar/', include('tables_app.urls')), # calendar
    path('about/', include('tables_app.urls')) # à propos

]
