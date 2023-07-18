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
        print("5. Gestion des Tournois")
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
            while True:
                print("\nGestion des Tournois:")
                print("1. Choix du Tournoi")
                print("2. Afficher les détails d'un tournoi")
                print("3. Enregistrer un tournoi dans un fichier")
                print("4. Retour au menu principal")

                sous_choix = input("Entrez votre choix : ")

                if sous_choix == "1":
                    tournament_list_view.display_tournaments(tournament_controller)
                    tournament_id = input("Spécifiez l'identifiant du tournoi ('q' pour quitter) : ")
                    if tournament_id.lower() == "q":
                        break
                    tournament = tournament_controller.select_tournament(tournament_id)
                    if tournament is not None:
                        tournament_list_view.display_players(tournament)
                elif sous_choix == "2":
                    tournament_list_view.display_tournaments(tournament_controller)
                    tournament_id = input("Spécifiez l'identifiant du tournoi ('q' pour quitter) : ")
                    if tournament_id.lower() == "q":
                        break
                    tournament = tournament_controller.select_tournament(tournament_id)
                    if tournament is not None:
                        tournament_list_view.display_tournament_details(tournament)
                elif sous_choix == "3":
                    tournament_list_view.display_tournaments(tournament_controller)
                    tournament_id = input("Spécifiez l'identifiant du tournoi ('q' pour quitter) : ")
                    if tournament_id.lower() == "q":
                        break
                    tournament = tournament_controller.select_tournament(tournament_id)
                    if tournament is not None:
                        tournament_list_view.save_tournament_to_file(tournament)
                        print(f"Le tournoi '{tournament.name}' a été enregistré dans un fichier.")
                elif sous_choix == "4":
                    break
                else:
                    print("Choix invalide. Veuillez réessayer.")
        elif choix.lower() == "q":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main()
