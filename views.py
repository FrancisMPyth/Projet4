# views.py
import os
from datetime import datetime
import re
import json
from controllers import PlayerController, TournamentController

TOURNOIS_DIR = "tournois"

class PlayerListView:
    def generate_chess_id(self, players):
        existing_ids = [player.chess_id for player in players]
        max_id = max(existing_ids, default="J0")
        match = re.match(r"J(\d+)", max_id)
        if match:
            next_id = int(match.group(1)) + 1
        else:
            next_id = 1
        return f"J{next_id:03d}"

    def create_player(self, player_controller):
        print("\nEnregistrement des Joueurs :")
        first_name = input("Prénom : ")
        last_name = input("Nom : ")
        date_of_birth_str = input("Date de naissance (jj/mm/aaaa) : ")
        try:
            date_of_birth = datetime.strptime(date_of_birth_str, "%d/%m/%Y")
        except ValueError:
            print("Format de date incorrect. Assurez-vous de saisir la date au format jj/mm/aaaa.")
            return

        chess_id = self.generate_chess_id(player_controller.get_players())
        national_chess_id = input("Identifiant national d'échecs : ")
        player_controller.add_player(first_name, last_name, date_of_birth, chess_id, national_chess_id)
        print("Joueur enregistré avec succès!")

    def display_player_list(self, player_controller):
        players = player_controller.get_players()
        print("\nListe des Joueurs :")
        for player in players:
            print(f"Nom: {player.last_name}")
            print(f"Prénom: {player.first_name}")
            print(f"Date de naissance: {player.date_of_birth.strftime('%d/%m/%Y')}")
            print(f"Identifiant: {player.chess_id}")
            print(f"Identifiant national d'échecs: {player.national_chess_id}\n")

class TournamentCreationView:
    def __init__(self, tournament_controller, player_controller):
        self.tournament_controller = tournament_controller
        self.player_controller = player_controller

    def generate_chess_id(self, players):
        existing_ids = [player.chess_id for player in players]
        max_id = max(existing_ids, default="J0")
        match = re.match(r"J(\d+)", max_id)
        if match:
            next_id = int(match.group(1)) + 1
        else:
            next_id = 1
        return f"J{next_id:03d}"

    def get_players_selection(self):
        players = self.player_controller.get_players()

        print("Liste des joueurs disponibles :")
        for i, player in enumerate(players, 1):
            print(f"{i}. {player.first_name} {player.last_name} (ID: {player.chess_id})")

        selected_players = []
        while True:
            player_id_input = input("Sélectionnez l'ID du joueur à ajouter au tournoi (ou appuyez sur Entrée pour terminer) : ")
            if not player_id_input:
                break

            selected_player = self.player_controller.select_player(player_id_input)
            if selected_player:
                selected_players.append(selected_player)
            else:
                print("ID de joueur invalide. Veuillez réessayer.")

        return selected_players

    def create_tournament(self):
        print("Enregistrer un tournoi :")
        name = input("Nom du tournoi : ")
        location = input("Lieu du tournoi : ")
        start_date_str = input("Date de début (jj/mm/aaaa) : ")
        end_date_str = input("Date de fin (jj/mm/aaaa) : ")

        try:
            number_of_rounds = int(input("Nombre de rounds (par défaut 4) : ") or 4)

            selected_players = self.get_players_selection()

            self.tournament_controller.create_tournament(name, location, start_date_str, end_date_str, number_of_rounds, selected_players)
            print("Tournoi enregistré avec succès!\n")
        except ValueError:
            print("Format de date ou nombre de rounds incorrect. Assurez-vous de saisir les informations correctement.")

class TournamentListView:
    def display_tournaments(self, tournament_controller):
        tournaments = tournament_controller.get_tournaments()

        if not tournaments:
            print("Aucun tournoi enregistré.")
            return

        print("Liste des tournois :")
        for tournament in tournaments:
            print(f"Identifiant : {tournament.tournament_id}")
            print(f"Nom : {tournament.name}")
            print(f"Lieu : {tournament.location}")
            print(f"Début : {tournament.start_date.strftime('%d/%m/%Y')}")
            print(f"Fin : {tournament.end_date.strftime('%d/%m/%Y')}")
            print(f"Nombre de rounds : {tournament.number_of_rounds}")
            print("Joueurs inscrits :")
            for player_id in tournament.players:
                player = tournament_controller.player_controller.select_player(player_id)
                if player:
                    print(f" - {player.first_name} {player.last_name} (ID: {player.chess_id})")
            print("=" * 40)

    def display_tournament_details(self, tournament):  
        print(f"Détails du tournoi '{tournament.name}' :")

    def display_players(self, tournament_controller, tournament):
        print(f"Joueurs inscrits au tournoi '{tournament.name}' :")
        for player_id in tournament.players:
            player = tournament_controller.player_controller.select_player(player_id)
            if player:
                print(f"  - {player.first_name} {player.last_name}")
        print()

    def save_tournament_to_file(self, tournament):
        filepath = os.path.join(TOURNOIS_DIR, f"{tournament.tournament_id}.json")
        with open(filepath, "w") as file:
            tournament_data = {
                "tournament_id": tournament.tournament_id,
                "name": tournament.name,
                "location": tournament.location,
                "start_date": tournament.start_date.strftime('%d/%m/%Y'),
                "end_date": tournament.end_date.strftime('%d/%m/%Y'),
                "number_of_rounds": tournament.number_of_rounds,
                "players": [
                    {
                        "first_name": player.first_name,
                        "last_name": player.last_name,
                        "date_of_birth": player.date_of_birth.strftime('%d/%m/%Y'),
                        "chess_id": player.chess_id,
                        "national_chess_id": player.national_chess_id
                    } for player in tournament.players
                ]
            }
            json.dump(tournament_data, file, indent=4)

