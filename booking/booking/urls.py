from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tables_app.urls')),     # accueil
    path('users/', include('users_app.urls')) # auth
]
