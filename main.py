# main.py

import os
import json
from datetime import datetime
from controllers import PlayerController, TournamentController
from views import PlayerListView, TournamentCreationView, TournamentListView

def main():
    player_controller = PlayerController()
    tournament_controller = TournamentController()
    player_list_view = PlayerListView()
    tournament_creation_view = TournamentCreationView()
    tournament_list_view = TournamentListView()

    while True:
        print("Menu Principal:")
        print("1. Enregistrement des Joueurs")
        print("2. Afficher la liste des joueurs")
        print("3. Enregistrer un tournoi")
        print("4. Afficher la liste des tournois")
        print("5. Gestion de Tournoi")
        print("q. Quitter")

        choix = input("Entrez votre choix : ")

        if choix == "1":
            player_list_view.create_player_list(player_controller)
        elif choix == "2":
            player_list_view.display_player_list(player_controller)
        elif choix == "3":
            tournament_creation_view.create_tournament(tournament_controller)
        elif choix == "4":
            tournament_list_view.display_tournaments(tournament_controller)
        elif choix == "5":
            tournament_list_view.display_tournaments(tournament_controller)
            tournament_id = input("Spécifiez l'identifiant du tournoi ('q' pour quitter) : ")
            if tournament_id.lower() == "q":
                continue
            tournament = tournament_controller.select_tournament(tournament_id)
            if tournament is not None:
                tournament_list_view.display_players(tournament)
        elif choix.lower() == "q":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
