from django.contrib import admin
from .models import Game, Table, Booking
from users_app.models import User
admin.site.register(Game)
admin.site.register(User)
admin.site.register(Table)
admin.site.register(Booking)