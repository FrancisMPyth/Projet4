# views

class PlayerListView:
    def display_players(self, players):
        print("Liste des Joueurs :")
        for player in players:
            print(f"- {player.first_name} {player.last_name}")


class TournamentListView:
    def display_tournaments(self, tournaments):
        print("Liste des Tournois :")
        for index, tournament in enumerate(tournaments):
            print(f"{index}. {tournament.name}")

class TournamentDetailView:
    def display_rounds(self, rounds):
        print("Liste des Rounds :")
        for round in rounds:
            print(f"- {round.name}")

    def display_matches(self, matches):
        print("Liste des Matchs :")
        for match in matches:
            print(f"- {match.player1.first_name} vs {match.player2.first_name} ({match.result})")
