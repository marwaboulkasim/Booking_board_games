# 🎲 Booking Board Games

Plateforme web de **réservation de tables de jeux de société** développée avec [Django](https://www.djangoproject.com/).  
Ce projet a été réalisé dans le cadre de notre formation en développement web collaboratif.

---

##  Fonctionnalités

-  **Calendrier interactif** : choisir une date et voir l’état des tables disponibles
-  **Réservation de tables** : créer, modifier ou annuler une réservation
-  **Gestion des utilisateurs** : inscription, connexion, profil personnalisé
-  **Ludothèque** : choix de jeux proposés (ou ajout du vôtre)
-  **Pages d’information** : Accueil, À propos, FAQ

---

##  Technologies utilisées

- **Backend** : Django (Python 3.12)
- **Base de données** : SQLite (par défaut) → peut évoluer vers PostgreSQL
- **Frontend** : HTML, CSS (templates Django)
- **Gestion de version** : Git + GitHub
- **Outils de travail collaboratif** : Figma (maquettes), Git branches

---

##  Structure du projet

Booking_board_games/
│── booking/ # Configuration principale Django
│── tables_app/ # Application pour la gestion des tables
│── users_app/ # Application pour l'authentification
│── static/ # Fichiers CSS, JS, images
│── templates/ # Templates globaux (base.html, etc.)
│── README.md # Ce fichier
│── requirements.txt # Dépendances du projet

---

##  Installation & lancement

1. **Cloner le projet** :
   ```bash
   git https://github.com/marwaboulkasim/Booking_board_games.git
   cd Booking_board_games
2. **Créer un environnement virtuel** :
   ```python -m venv .venv
source .venv/bin/activate   # sous Linux / Mac
.venv\Scripts\activate      # sous Windows
3. **Installer les dépendances** :
pip install -r requirements.txt

4. **Lancer les migrations** :
python manage.py migrate

5. **Démarrer le serveur** :
python manage.py runserver

6. **Accéder à l'application en local** :
http://127.0.0.1:8000

## Équipe de développement

Marwa – Authentification & gestion des utilisateurs

Thibaut – Base de données & gestion des tables

Gaëtan – Réservations & interface calendrier
