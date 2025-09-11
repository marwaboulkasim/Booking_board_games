
# Début Thibaud

from django.db import models
from django.utils import timezone
from django.conf import settings

# Enum pour l'état des tables
class TableEtat(models.TextChoices):
    LIBRE = 'libre', 'Libre'
    PRIVEE = 'privée', 'Privée'
    PUBLIQUE = 'publique', 'Publique'

# Enum pour le type de réservation
class BookingType(models.TextChoices):
    PRIVEE = 'privée', 'Privée'
    PUBLIQUE = 'publique', 'Publique'


# Games
class Game(models.Model):
    name_game = models.CharField(max_length=100)
    category_game = models.CharField(max_length=50)
    duration_game = models.CharField(max_length=50, null=True, blank=True)
    nb_player_min_game = models.IntegerField(null=True, blank=True)
    nb_player_max_game = models.IntegerField(null=True, blank=True)
    stock_game = models.IntegerField(default=0)
    availability_game = models.BooleanField(default=True)
    presentation = models.TextField(null=True, blank=True) 
    image_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name_game



# Tables
class Table(models.Model):
    number_table = models.IntegerField(unique=True)
    capacity_table = models.IntegerField()
    state_table = models.CharField(max_length=10, choices=TableEtat.choices, default=TableEtat.LIBRE)
    game_table = models.ForeignKey("Game", null=True, blank=True, on_delete=models.SET_NULL)
    code_table = models.CharField(max_length=20, null=True, blank=True)
    customer_table = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            blank=True,
                                            related_name='joined_tables')

    def __str__(self):
        return f"Table {self.number_table} - {self.state_table}"


# Booking / Réservation
class Booking(models.Model):
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    duration = models.DurationField(help_text="Durée (HH:MM:SS)")
    booking_type = models.CharField(max_length=10, choices=BookingType.choices)
    table = models.ForeignKey("Table", on_delete=models.CASCADE)
    main_customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    
    class Meta:
        ordering = ['-date', 'start_time']
        
    def __str__(self):
        return f"{self.main_customer.pseudo} - Table {self.table.number_table} le {self.date}"



# Fin Thibaud