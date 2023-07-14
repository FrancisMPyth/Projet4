# controllers.py

import os
import json
from datetime import datetime
from views import *
from models import Tournament, Player

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
JOUEURS_DIR = os.path.join(DATA_DIR, "joueurs")
TOURNOIS_DIR = os.path.join(DATA_DIR, "tournois")

# Créer les répertoires s'ils n'existent pas
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(JOUEURS_DIR, exist_ok=True)


class TournamentController:

    tournament_index = 0

    def __init__(self):
        self.tournaments = []
        self.players = []
        self.load_players_from_file()
        self.load_tournaments_from_file()

    def create_tournament(self, name, location, start_date, end_date):
        self.tournament_index += 1
        tournament_index_str = f"T{self.tournament_index:03d}"
        tournament = Tournament(tournament_index_str, name, location, start_date, end_date)
        self.tournaments.append(tournament)
        self.save_tournaments_to_file()
        return tournament


    def save_tournaments_to_file(self):
        tournaments = [tournament.__dict__ for tournament in self.tournaments]
        filepath = os.path.join(TOURNOIS_DIR, "tournois.json")

        with open(filepath, "w") as file:
            json.dump(tournaments, file, indent=4)

    def display_tournaments(self):
        tournois = self.get_tournaments()
        self._lazy_import_views()
        self.tournament_list_view.display_tournaments(tournois)

    def add_player(self, first_name, last_name, date_of_birth, chess_id):
        player = Player(first_name, last_name, date_of_birth, chess_id)
        self.players.append(player)
        self.save_players_to_file()
        return player

    def add_player_to_tournament(self, tournament_index, player_index):
        tournament = self.tournaments[tournament_index]
        player = self.players[player_index]
        tournament.players.append(player)

    def generate_rounds(self, tournament_index, nombre_tours=4):
        # Logique de génération des rounds pour le tournoi spécifié
        tournament = self.tournaments[tournament_index]
        # Code pour générer les rounds en fonction des joueurs inscrits au tournoi

    def record_match_result(self, match, result):
        # Logique pour enregistrer le résultat d'un match
        match.result = result

    def get_players(self):
        return self.players

    def get_tournaments(self):
        return self.tournaments

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

    def load_tournaments_from_file(self):
        filepath = os.path.join(TOURNOIS_DIR, "tournois.json")
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                tournaments_data = json.load(file)
                for tournament_data in tournaments_data:
                    index = tournament_data["index"]
                    name = tournament_data["name"]
                    location = tournament_data["location"]
                    start_date = datetime.strptime(tournament_data["start_date"], "%d-%m-%Y")
                    end_date = datetime.strptime(tournament_data["end_date"], "%d-%m-%Y")
                    rounds = tournament_data["rounds"]
                    players = tournament_data["players"]

                    tournament = Tournament(index, name, location, start_date, end_date, rounds, players)

                    self.tournaments.append(tournament)
