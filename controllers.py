# controllers.py

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

    def add_player(self, first_name, last_name, date_of_birth, chess_id, national_chess_id):
        player = Player(first_name, last_name, date_of_birth, chess_id, national_chess_id)
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
                    "chess_id": player.chess_id,
                    "national_chess_id": player.national_chess_id
                }
                players_data.append(player_data)
            json.dump(players_data, file)

    def load_players_from_file(self):
        filepath = os.path.join(JOUEURS_DIR, "joueurs.json")
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                try:
                    players_data = json.load(file)
                    for player_data in players_data:
                        first_name = player_data["first_name"]
                        last_name = player_data["last_name"]
                        date_of_birth = datetime.strptime(player_data["date_of_birth"], "%d/%m/%Y")
                        chess_id = player_data["chess_id"]
                        national_chess_id = player_data["national_chess_id"]
                        player = Player(first_name, last_name, date_of_birth, chess_id, national_chess_id)
                        self.players.append(player)
                except json.JSONDecodeError:
                    print("Erreur lors du chargement des données des joueurs. Le fichier peut être vide.")
        else:
            print("Le fichier des joueurs n'existe pas. Une nouvelle liste de joueurs sera créée.")

class TournamentController:
        def __init__(self, player_controller):
            self.player_controller = player_controller
            self.load_tournaments_from_file()

        def create_tournament(self, name, location, start_date_str, end_date_str, number_of_rounds):
            try:
                start_date = datetime.strptime(start_date_str, "%d/%m/%Y")  
                end_date = datetime.strptime(end_date_str, "%d/%m/%Y")  
            except ValueError:
                print("Format de date incorrect. Assurez-vous de saisir la date au format jj/mm/aaaa.")
                return

            tournament_id = self.generate_tournament_id()
            tournament = Tournament(tournament_id, name, location, start_date, end_date, number_of_rounds)
            self.tournaments.append(tournament)
            self.save_tournaments_to_file()

            return tournament
            
        def get_tournaments(self):
            return self.tournaments
        
        def save_tournaments_to_file(self):
            tournaments = [self.serialize_tournament(tournament) for tournament in self.tournaments]
            filepath = os.path.join(TOURNOIS_DIR, "tournois.json")

            with open(filepath, "w") as file:
                json.dump(tournaments, file, indent=4, default=datetime_to_string)

        def load_tournaments_from_file(self):
            filepath = os.path.join(TOURNOIS_DIR, "tournois.json")
            if os.path.isfile(filepath):
                with open(filepath, "r") as file:
                    try:
                        tournaments_data = json.load(file)

                        tournaments = []
                        for tournament_data in tournaments_data:
                            tournament = self.deserialize_tournament(tournament_data)
                            tournaments.append(tournament)

                        self.tournaments = tournaments
                    except json.JSONDecodeError:
                        print("Erreur lors du chargement des données des tournois. Le fichier peut être vide.")
            else:
                print("Le fichier des tournois n'existe pas. Aucun tournoi enregistré.")

        def generate_tournament_id(self):
                tournament_count = len(self.tournaments)
                tournament_id = f"T{tournament_count + 1}"
                return tournament_id

        def serialize_tournament(self, tournament):
                if isinstance(tournament, Tournament):
                    return {
                        "tournament_id": tournament.tournament_id,
                        "name": tournament.name,
                        "location": tournament.location,
                        "start_date": tournament.start_date.strftime("%d/%m/%Y"),
                        "end_date": tournament.end_date.strftime("%d/%m/%Y"),
                        "number_of_rounds": tournament.number_of_rounds,
                        "players": [player.chess_id for player in tournament.players]
                    }
                raise TypeError(f"Object of type {tournament.__class__.__name__} is not JSON serializable")

        def deserialize_tournament(self, tournament_data):
                return Tournament(
                    tournament_data["tournament_id"],
                    tournament_data["name"],
                    tournament_data["location"],
                    datetime.strptime(tournament_data["start_date"], "%d/%m/%Y"),
                    datetime.strptime(tournament_data["end_date"], "%d/%m/%Y"),
                    tournament_data.get("number_of_rounds", 4)
                )

def datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%d/%m/%Y")
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")