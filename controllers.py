# Controllers.py

import os
import json
from datetime import datetime
from models import Player, Tournament

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
TOURNOIS_DIR = os.path.join(DATA_DIR, "tournois")
JOUEURS_DIR = os.path.join(DATA_DIR, "joueurs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TOURNOIS_DIR, exist_ok=True)
os.makedirs(JOUEURS_DIR, exist_ok=True)


class PlayerController:
    def __init__(self):
        self.players = []
        self.load_players_from_file()

    def add_player(self, first_name, last_name, date_of_birth, chess_id):
        player = Player(first_name, last_name, date_of_birth, chess_id)
        self.players.append(player)
        self.save_players_to_file()
        return player

    def select_player(self, player_id):
        for player in self.players:
            if player.chess_id == player_id:
                return player
        return None

    def get_players(self):
        return self.players

    def save_players_to_file(self):
        filepath = os.path.join(JOUEURS_DIR, "joueurs.json")
        with open(filepath, "w") as file:
            players_data = []
            for player in self.players:
                player_data = {
                    "first_name": player.first_name,
                    "last_name": player.last_name,
                    "date_of_birth": player.date_of_birth.strftime("%d/%m/%Y"),
                    "chess_id": player.chess_id
                }
                players_data.append(player_data)
            json.dump(players_data, file)

    def load_players_from_file(self):
        filepath = os.path.join(JOUEURS_DIR, "joueurs.json")
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                players_data = json.load(file)
                for player_data in players_data:
                    first_name = player_data["first_name"]
                    last_name = player_data["last_name"]
                    date_of_birth = datetime.strptime(player_data["date_of_birth"], "%d/%m/%Y")
                    chess_id = player_data["chess_id"]
                    player = Player(first_name, last_name, date_of_birth, chess_id)
                    self.players.append(player)


class TournamentController:
    def __init__(self):
        self.tournaments = []
        self.load_tournaments_from_file()
        self.player_controller = PlayerController()

    def create_tournament(self, name, location, start_date, end_date, number_of_rounds=4):
        tournament_id = self.generate_tournament_id()
        tournament = Tournament(tournament_id, name, location, start_date, end_date, number_of_rounds)
        
        player_ids = input("Entrez les identifiants des joueurs séparés par des virgules : ").split(",")
        for player_id in player_ids:
            player = self.player_controller.select_player(player_id.strip())
            if player:
                tournament.add_player(player)

        self.tournaments.append(tournament)
        self.save_tournaments_to_file()
        return tournament

    def get_tournaments(self):
        return self.tournaments

    def select_tournament(self, tournament_id):
        for tournament in self.tournaments:
            if tournament.tournament_id == tournament_id:
                return tournament
        return None

    def save_tournaments_to_file(self):
        tournaments = [tournament.__dict__ for tournament in self.tournaments]
        filepath = os.path.join(TOURNOIS_DIR, "tournois.json")

        with open(filepath, "w") as file:
            json.dump(tournaments, file, indent=4, default=datetime_to_string)

    def load_tournaments_from_file(self):
        filepath = os.path.join(TOURNOIS_DIR, "tournois.json")
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                tournaments_data = json.load(file)
                for tournament_data in tournaments_data:
                    tournament = Tournament(
                        tournament_data["tournament_id"],
                        tournament_data["name"],
                        tournament_data["location"],
                        datetime.strptime(tournament_data["start_date"], "%d/%m/%Y"),
                        datetime.strptime(tournament_data["end_date"], "%d/%m/%Y"),
                        tournament_data.get("number_of_rounds", 4)
                    )
                    self.tournaments.append(tournament)

    def generate_tournament_id(self):
        tournament_count = len(self.tournaments)
        tournament_id = f"T{tournament_count + 1}"
        return tournament_id


def datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%d/%m/%Y")
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


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
