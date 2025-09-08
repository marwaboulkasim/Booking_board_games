from django.contrib import admin
from django.urls import path, include
from tables_app import views as table_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tables_app.urls')),     # accueil
    path('users/', include('users_app.urls')), # auth
    path('calendar/', include('tables_app.urls')) # calendar

    # accueil + calendrier (gérés par tables_app/urls.py)
    path('', include('tables_app.urls')),

    # authentification
    path('users/', include('users_app.urls')),

    # Pages supplémentaires
    path('about/', table_views.about_view, name='about'),
    path('games/', table_views.games_view, name='games'),
    path('book-table/', table_views.book_table_view, name='book_table'),
    path('contact/', table_views.contact_view, name='contact'),
    path('account/', table_views.account_view, name='account'),
]
