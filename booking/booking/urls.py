from django.contrib import admin
from django.urls import path, include  # <- include est nécessaire

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tables_app.urls')),  # <- inclut les urls de ton app
]
