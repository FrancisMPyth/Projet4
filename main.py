# main.py

import os
import json
from datetime import datetime
from controllers import TournamentController
from views import PlayerListView
from views import PlayerListView, TournamentListView, TournamentCreationView

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "tournois"), exist_ok=True)


def datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%d-%m-%Y")
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def main():
    tournament_controller = TournamentController()
    player_list_view = PlayerListView()
    tournament_list_view = TournamentListView()
    tournament_creation_view = TournamentCreationView()

    while True:
        print("Menu Principal:")
        print("1. Enregistrement des Joueurs")
        print("2. Afficher la liste des joueurs")
        print("3. Enregistrer un tournoi")
        print("4. Afficher la liste des tournois")
        print("5. Lancer un Tournoi")
        print("q. Quitter")

        choix = input("Entrez votre choix : ")

        if choix == "1":
            player_list_view.create_player_list(tournament_controller)
        elif choix == "2":
            player_list_view.display_player_list(tournament_controller)
        elif choix == "3":
            tournament_creation_view.create_tournament(tournament_controller)
        elif choix == "4":
            tournament_list_view.display_tournaments(tournament_controller)
        elif choix.lower() == "q":
            break
        else:
            print("Entrée invalide. Veuillez réessayer.")

    tournament_controller.save_players_to_file()
    tournament_controller.save_tournaments_to_file()

if __name__ == "__main__":
    main()

