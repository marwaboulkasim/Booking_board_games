from django.contrib import admin
from .models import Game, Customer, Table, Booking

admin.site.register(Game)
admin.site.register(Customer)
admin.site.register(Table)
admin.site.register(Booking)