# controllers



from models import Tournament, Player

class TournamentController:
    def __init__(self):
        self.tournaments = []
        self.players = []

    def create_tournament(self, name, location, start_date, end_date):
        tournament = Tournament(name, location, start_date, end_date)
        self.tournaments.append(tournament)
        return tournament

    def add_player_to_tournament(self, tournament_index, first_name, last_name):
        player = Player(first_name, last_name)
        self.tournaments[tournament_index].players.append(player)
        self.players.append(player)
        return player

    def generate_rounds(self, tournament_index):
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
