# Pour envoyer la donnée CSV dans la BDD (en passant en json) :
# python manage.py import_games
# Penser à bien se mettre dans /booking-board-game/booking
# Le CSV est donc modifiable manuellement, et actualisable avec les commandes.


import os
import csv
from django.core.management.base import BaseCommand
from tables_app.models import Table, Game, TableEtat

class Command(BaseCommand):
    help = "Importe les tables depuis le CSV dans la base de données"

    def handle(self, *args, **kwargs):
        # Remonter à la racine du projet (booking-board-game)
        csv_path = os.path.join(os.path.dirname(os.getcwd()), 'data', 'tables.csv')

        if not os.path.exists(csv_path):
            self.stderr.write(f"❌ Fichier CSV introuvable : {csv_path}")
            return

        print(f"📄 Fichier CSV trouvé : {csv_path}")

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count_added = 0
            for row in reader:
                # Chercher le jeu correspondant si renseigné
                game = None
                if row["game_table"]:
                    game = Game.objects.filter(name_game=row["game_table"]).first()
                    if not game:
                        self.stderr.write(f"⚠️ Jeu '{row['game_table']}' introuvable, ignoré pour la table {row['number_table']}")

                table, created = Table.objects.get_or_create(
                    number_table=int(row["number_table"]),
                    defaults={
                        "capacity_table": int(row["capacity_table"]),
                        "state_table": row["state_table"],
                        "game_table": game,
                        "code_table": row["code_table"] or None,
                    }
                )

                if created:
                    count_added += 1
                    self.stdout.write(f"✅ Table ajoutée : {table}")
                else:
                    self.stdout.write(f"⚠️ Table déjà existante : {table}")

            self.stdout.write(self.style.SUCCESS(f"Import terminé ! {count_added} nouvelles tables ajoutées."))
