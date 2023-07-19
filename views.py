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
    
    def create_tournament(self, name, location, start_date, end_date, number_of_rounds=4):
        tournament_id = self.generate_tournament_id()
        start_date = datetime.strptime(start_date, "%d/%m/%Y")  # Convertir en objet datetime
        end_date = datetime.strptime(end_date, "%d/%m/%Y")  # Convertir en objet datetime

        tournament = Tournament(tournament_id, name, location, start_date, end_date, number_of_rounds)

        player_ids = input("Entrez les identifiants des joueurs séparés par des virgules : ").split(",")
        for player_id in player_ids:
            player = self.player_controller.select_player(player_id.strip())
            if player:
                tournament.add_player(player)  # Ajouter le joueur au tournoi
            else:
                print(f"Le joueur avec l'identifiant '{player_id}' n'a pas été trouvé. Veuillez vérifier l'identifiant.")

        self.tournaments.append(tournament)
        self.save_tournaments_to_file()
        return tournament

class TournamentListView:
    def display_tournaments(self, tournament_controller):
        tournaments = tournament_controller.get_tournaments()
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

    def display_players(self, tournament_controller, tournament):
        print(f"Joueurs inscrits au tournoi '{tournament.name}' :")
        for player_id in tournament.players:
            player = tournament_controller.player_controller.select_player(player_id)
            if player:
                print(f"  - {player.first_name} {player.last_name}")
        print()

    def display_tournament_details(self, tournament):
        print(f"Détails du tournoi '{tournament.name}' :")
        print(f"Identifiant : {tournament.tournament_id}")
        print(f"Lieu : {tournament.location}")
        print(f"Début : {tournament.start_date.strftime('%d/%m/%Y')}")
        print(f"Fin : {tournament.end_date.strftime('%d/%m/%Y')}")
        print(f"Nombre de rounds : {tournament.number_of_rounds}")
        print(f"Joueurs inscrits ({len(tournament.players)} sur {tournament.number_of_players}) :")
        for player in tournament.players:
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
