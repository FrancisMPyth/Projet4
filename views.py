# views.py

import os
import json
from datetime import datetime
from controllers import PlayerController, TournamentController

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
TOURNOIS_DIR = os.path.join(DATA_DIR, "tournois")
JOUEURS_DIR = os.path.join(DATA_DIR, "joueurs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TOURNOIS_DIR, exist_ok=True)
os.makedirs(JOUEURS_DIR, exist_ok=True)


class PlayerListView:
    def display_player_list(self, player_controller):
        players = player_controller.get_players()
        print("Liste des Joueurs :")
        for player in players:
            print(f"Nom: {player.first_name} {player.last_name}")
            print(f"Date de naissance: {player.date_of_birth.strftime('%d/%m/%Y')}")
            print(f"Identifiant: {player.chess_id}")
            print()


class TournamentCreationView:
    def create_tournament(self, tournament_controller):
        print("Enregistrer un tournoi :")
        name = input("Nom du tournoi : ")
        location = input("Lieu du tournoi : ")
        start_date = datetime.strptime(input("Date de début (jj/mm/aaaa) : "), "%d/%m/%Y")
        end_date = datetime.strptime(input("Date de fin (jj/mm/aaaa) : "), "%d/%m/%Y")

        tournament = tournament_controller.create_tournament(name, location, start_date, end_date)
        print(f"Le tournoi '{tournament.name}' a été enregistré avec succès.")


class TournamentListView:
    def display_tournaments(self, tournament_controller):
        tournaments = tournament_controller.get_tournaments()
        print("Liste des Tournois :")
        for tournament in tournaments:
            print(f"Identifiant: {tournament.tournament_id}")
            print(f"Nom: {tournament.name}")
            print(f"Lieu: {tournament.location}")
            print(f"Date de début: {tournament.start_date.strftime('%d/%m/%Y')}")
            print(f"Date de fin: {tournament.end_date.strftime('%d/%m/%Y')}")
            print(f"Nombre de tours: {tournament.number_of_rounds}")
            print()

    def display_players(self, tournament):
        print(f"Liste des joueurs pour le tournoi '{tournament.name}' :")
        players = tournament.players
        for player in players:
            print(f"Nom: {player.first_name} {player.last_name}")
            print(f"Date de naissance: {player.date_of_birth.strftime('%d/%m/%Y')}")
            print(f"Identifiant: {player.chess_id}")
            print()

    def save_tournament_to_file(self, tournament):
        filepath = os.path.join(TOURNOIS_DIR, f"{tournament.name}.json")
        with open(filepath, "w") as file:
            tournament_data = {
                "tournament_id": tournament.tournament_id,
                "name": tournament.name,
                "location": tournament.location,
                "start_date": tournament.start_date.strftime("%d/%m/%Y"),
                "end_date": tournament.end_date.strftime("%d/%m/%Y"),
                "number_of_rounds": tournament.number_of_rounds,
                "players": [
                    {
                        "first_name": player.first_name,
                        "last_name": player.last_name,
                        "date_of_birth": player.date_of_birth.strftime("%d/%m/%Y"),
                        "chess_id": player.chess_id
                    }
                    for player in tournament.players
                ]
            }
            json.dump(tournament_data, file, indent=4)


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
