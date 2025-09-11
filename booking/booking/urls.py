from django.contrib import admin
from django.urls import path, include
from tables_app import views as table_views



urlpatterns = [
    path('admin/', admin.site.urls),

    # accueil + calendrier (gérés par tables_app/urls.py)
    path('', include('tables_app.urls')),

    # authentification
    path('users/', include('users_app.urls')),



]
