
# main.py

import os
from controllers import TournamentController
from views import MenuView

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
JOUEURS_DIR = os.path.join(DATA_DIR, "joueurs")
TOURNOIS_DIR = os.path.join(DATA_DIR, "tournois")


# Créer les répertoires si ils n'existent pas
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(JOUEURS_DIR, exist_ok=True)
os.makedirs(TOURNOIS_DIR, exist_ok=True)

def main():
    tournament_controller = TournamentController()
    menu_view = MenuView(tournament_controller)
    menu_view.run()

if __name__ == "__main__":
    main()
