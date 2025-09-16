from django.db import models
from django.utils import timezone
from django.conf import settings
import random
import string


# Enum pour l'état des tables
class TableEtat(models.TextChoices):
    LIBRE = 'libre', 'Libre'
    PRIVEE = 'privée', 'Privée'
    PUBLIQUE = 'publique', 'Publique'

# Enum pour le type de réservation
class BookingType(models.TextChoices):
    PRIVEE = 'privée', 'Privée'
    PUBLIQUE = 'publique', 'Publique'

# Game
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
    capacity_table = models.IntegerField(default=12)
    state_table = models.CharField(max_length=10, choices=TableEtat.choices, default=TableEtat.LIBRE)
    game_table = models.ForeignKey("Game", null=True, blank=True, on_delete=models.SET_NULL)
    code_table = models.CharField(max_length=20, null=True, blank=True)
    customer_table = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            blank=True,
                                            related_name='joined_tables')

    def __str__(self):
        return f"Table {self.number_table} - {self.state_table}"


class Booking(models.Model):
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    duration = models.DurationField(help_text="Durée (HH:MM:SS)")
    booking_type = models.CharField(max_length=10, choices=BookingType.choices)
    table = models.ForeignKey("Table", on_delete=models.CASCADE)
    main_customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    code = models.CharField(max_length=10, blank=True, null=True)  # ajout du code

    # Partie sélection jeu
    game = models.ForeignKey("tables_app.Game", on_delete=models.SET_NULL, null=True, blank=True)
    max_players = models.PositiveBigIntegerField(null=True, blank=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_bookings', blank=True)
    # Option jeu utilisateur
    custom_game = models.CharField(max_length=100, blank=True, null=True)
    

    def save(self, *args, **kwargs):
        # Générer un code uniquement si réservation privée et pas déjà présent
        if self.booking_type == BookingType.PRIVEE and not self.code:
            self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)
        
        # Si publique et pas de max_players fourni -> prendre le max_player du jeu
        if self.game and getattr(self.game, "nb_player_max_game", None):
            self.max_players = self.game.nb_player_max_game
        
        # Empêche le max_players > capacity de la table
        if self.max_players and getattr(self.table, "capacity_table", None):
            if self.max_players > self.table.capacity_table:
                self.max_players = self.table.capacity_table
        super().save(*args, **kwargs)
    
    @property
    def seats_taken(self):
        # 1 pour le créateur + participants
        return 1 + self.participants.count()

    @property
    def remaining_places(self):
        if self.booking_type != 'publique' or not self.max_players:
            return 0
        return max(0, self.max_players - self.seats_taken)

    @property
    def is_full(self):
        return self.booking_type == 'publique' and self.max_players is not None and self.seats_taken >= self.max_players

    def __str__(self):
        return f"{self.main_customer.pseudo} - Table {self.table.number_table} le {self.date}"
    

    
