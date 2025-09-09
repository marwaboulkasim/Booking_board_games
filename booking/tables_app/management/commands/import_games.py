# Pour envoyer la donnée CSV dans la BDD (en passant en json) :
# python manage.py import_games
# Penser à bien se mettre dans /booking-board-game/booking
# Le CSV est donc modifiable manuellement, et actualisable avec les commandes.

# Si besoin de supprimer l'ensemble des données dans la BDD (puis repartir sur un manage.py import_games) :
# 1 = python manage.py shell
# 2 = from tables_app.models import Game
# Game.objects.all().delete()


# import os
# import csv
# from django.core.management.base import BaseCommand
# from tables_app.models import Game

# class Command(BaseCommand):
#     help = 'Importe les jeux depuis le CSV dans la base de données'

#     def handle(self, *args, **kwargs):
#         # Chemin relatif depuis le dossier courant où l'on lance python manage.py
#         csv_path = os.path.join(os.path.dirname(os.getcwd()), 'data', 'games.csv')

#         # Vérification de l'existence du fichier CSV
#         if not os.path.exists(csv_path):
#             self.stderr.write(f"❌ Fichier CSV introuvable : {csv_path}")
#             return

#         print(f"📄 Fichier CSV trouvé : {csv_path}")  # Pour confirmer

#         with open(csv_path, newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             count_added = 0
#             for row in reader:
#                 game, created = Game.objects.get_or_create(
#                     name_game=row["name_game"],
#                     defaults={
#                         "category_game": row["category_game"],
#                         "nb_player_min_game": int(row["nb_player_min_game"]),
#                         "nb_player_max_game": int(row["nb_player_max_game"]),
#                         "stock_game": int(row["stock_game"]),
#                         "availability_game": row["availability_game"].lower() in ["true", "1", "yes"]
#                     }
#                 )
#                 if created:
#                     count_added += 1
#                     self.stdout.write(f"✅ Jeu ajouté : {game.name_game}")
#                 else:
#                     self.stdout.write(f"⚠️ Jeu déjà existant : {game.name_game}")

#             self.stdout.write(self.style.SUCCESS(f"Import terminé ! {count_added} nouveaux jeux ajoutés."))




import os
import csv
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from tables_app.models import Game

class Command(BaseCommand):
    help = 'Importe les jeux depuis le CSV et met à jour les images'

    def handle(self, *args, **kwargs):
        # Chemin vers le CSV depuis la racine du projet
        csv_path = os.path.join(os.path.dirname(os.getcwd()), 'data', 'games.csv')

        if not os.path.exists(csv_path):
            self.stderr.write(f"❌ Fichier CSV introuvable : {csv_path}")
            return

        print(f"📄 Fichier CSV trouvé : {csv_path}")

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count_added = 0
            count_updated = 0

            for row in reader:
                # Récupérer ou créer le jeu
                game, created = Game.objects.get_or_create(name_game=row["name_game"])

                # Mettre à jour les informations
                game.category_game = row["category_game"]
                game.duration_game = row.get("duration_game", "")
                game.presentation = row.get("presentation", "")
                game.nb_player_min_game = int(row["nb_player_min_game"])
                game.nb_player_max_game = int(row["nb_player_max_game"])
                game.stock_game = int(row["stock_game"])
                game.availability_game = row["availability_game"].lower() in ["true", "1", "yes"]
                
                # Champ image_url ou ImageField
                image_url = row.get("image_url")
                if image_url:
                    # Si c'est un ImageField et que le jeu n'a pas encore d'image
                    if hasattr(game, 'image') and not game.image:
                        try:
                            response = requests.get(image_url)
                            if response.status_code == 200:
                                game.image.save(
                                    os.path.basename(image_url),
                                    ContentFile(response.content),
                                    save=False  # On sauvegarde après avoir mis tous les champs
                                )
                        except Exception as e:
                            self.stderr.write(f"❌ Impossible de télécharger l'image pour {game.name_game}: {e}")
                    else:
                        # Sinon on peut juste stocker l'URL si tu utilises image_url
                        game.image_url = image_url

                game.save()

                if created:
                    count_added += 1
                    self.stdout.write(f"✅ Jeu ajouté : {game.name_game}")
                else:
                    count_updated += 1
                    self.stdout.write(f"🔄 Jeu mis à jour : {game.name_game}")

            self.stdout.write(self.style.SUCCESS(
                f"Import terminé ! {count_added} nouveaux jeux ajoutés, {count_updated} jeux mis à jour."
            ))


