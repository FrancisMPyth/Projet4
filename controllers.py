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

class TournamentController:
    def __init__(self):
        self.players = []
        self.tournaments = []
        self.load_players_from_file()
        self.load_tournaments_from_file()

    def create_tournament(self, name, location, date_debut, date_fin, number_of_rounds=4):
        tournament_id = self.generate_tournament_id()
        start_date = date_debut
        end_date = date_fin
        tournament = Tournament(tournament_id, name, location, start_date, end_date, number_of_rounds)
        self.tournaments.append(tournament)
        self.save_tournaments_to_file()
        return tournament

    def generate_tournament_id(self):
        tournament_count = len(self.tournaments)
        tournament_id = f"T{tournament_count + 1}"
        return tournament_id

    def save_tournaments_to_file(self):
        tournaments = [tournament.__dict__ for tournament in self.tournaments]
        filepath = os.path.join(TOURNOIS_DIR, "tournois.json")

        with open(filepath, "w") as file:
            json.dump(tournaments, file, indent=4)

    def load_tournaments_from_file(self):
        filepath = os.path.join(TOURNOIS_DIR, "tournois.json")
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                tournaments_data = json.load(file)
                for tournament_data in tournaments_data:
                    tournament_id = tournament_data["tournament_id"]
                    name = tournament_data["name"]
                    location = tournament_data["location"]
                    start_date = datetime.strptime(tournament_data["start_date"], "%d/%m/%Y")
                    end_date = datetime.strptime(tournament_data["end_date"], "%d/%m/%Y")
                    number_of_rounds = tournament_data.get("number_of_rounds", 4)
                    tournament = Tournament(tournament_id, name, location, start_date, end_date, number_of_rounds)
                    self.tournaments.append(tournament)

    def get_tournaments(self):
        return self.tournaments

    def add_player(self, first_name, last_name, date_of_birth, chess_id):
        player = Player(first_name, last_name, date_of_birth, chess_id)
        self.players.append(player)
        self.save_players_to_file()
        return player

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
                    "date_of_birth": player.date_of_birth.strftime("%d-%m-%Y"),
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
                    date_of_birth = datetime.strptime(player_data["date_of_birth"], "%d-%m-%Y")
                    chess_id = player_data["chess_id"]
                    player = Player(first_name, last_name, date_of_birth, chess_id)
                    self.players.append(player)
