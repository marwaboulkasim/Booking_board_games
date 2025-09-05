from django.db import models

# Tables
class Table(models.Model):
    number_table = models.IntegerField(unique=True)
    capacity_table = models.IntegerField()
    state_table = models.CharField(max_length=10, choices=TableEtat.choices, default=TableEtat.LIBRE)
    game_table = models.ForeignKey(Game, null=True, blank=True, on_delete=models.SET_NULL)
    code_table = models.CharField(max_length=20, null=True, blank=True)
    customer_table = models.ManyToManyField(Customer, blank=True, related_name='tables')

    def __str__(self):
        return f"Table {self.number_table} - {self.state_table}"