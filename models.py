# models.py

class Player:
    def __init__(self, first_name, last_name, date_of_birth, chess_id):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.chess_id = chess_id

class Tournament:
    def __init__(self, tournament_id, name, location, start_date, end_date, number_of_rounds=4):
        self.tournament_id = tournament_id
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.players = []

    def add_player(self, player):
        self.players.append(player)



