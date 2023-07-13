# views.py

from models import Player, Tournament, Round, Match
import os


class PlayerListView:
    def display_players(self, players):
        print("Liste des Joueurs :")
        for player in players:
           print(f"- {player.first_name} - {player.last_name} - {player.date_of_birth.strftime('%Y-%m-%d')} - ({player.chess_id})")

        print()  



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


class MenuView:
    def __init__(self, tournament_controller):
        self.tournament_controller = tournament_controller
        self.player_list_view = PlayerListView()
        self.tournament_list_view = TournamentListView()
        self.tournament_detail_view = TournamentDetailView()

    def run(self):
        while True:
            print("Menu Principal:")
            print("1. Créer une Liste de Joueurs")
            print("2. Afficher la Liste des Joueurs")
            print("3. Créer un Tournoi")
            print("4. Ajouter un Joueur au Tournoi")
            print("5. Générer les Rounds d'un Tournoi")
            print("6. Enregistrer le Résultat d'un Match")
            print("7. Afficher la Liste des Tournois")
            print("8. Afficher les Détails d'un Tournoi")
            print("q. Quitter")

            choix = input("Entrez votre choix : ")

            if choix == "1":
                self.create_player_list()
            elif choix == "2":
                self.display_player_list()
            elif choix == "3":
                self.create_tournament()
            elif choix == "4":
                self.add_player_to_tournament()
            elif choix == "5":
                self.generate_rounds()
            elif choix == "6":
                self.record_match_result()
            elif choix == "7":
                self.display_tournaments()
            elif choix == "8":
                self.display_tournament_details()
            elif choix.lower() == "q":
                break
            else:
                print("Entrée invalide. Veuillez réessayer.")

    def create_player_list(self):
        print("Création de la Liste de Joueurs")
        while True:
            print("Entrez les informations du joueur ('q' pour quitter) :")
            nom_joueur = input("Nom du joueur : ")
            if nom_joueur.lower() == "q":
                break
            prenom_joueur = input("Prénom du joueur : ")
            date_naissance_joueur = input("Date de Naissance du joueur (JJ-MM-AAAA) : ")
            identifiant_echec = input("Identifiant Echec du joueur (2 lettres majuscules + 5 chiffres) : ")

            # Vérification des informations du joueur
            if not re.match(r"^[A-Z]{2}\d{5}$", identifiant_echec):
                print("L'identifiant Echec doit contenir 2 lettres majuscules suivies de 5 chiffres.")
                continue

            try:
                date_naissance = datetime.strptime(date_naissance_joueur, "%d-%m-%Y")
            except ValueError:
                print("Format de date invalide. Veuillez utiliser le format JJ-MM-AAAA.")
                continue

            joueur = self.tournament_controller.add_player(nom_joueur, prenom_joueur, date_naissance, identifiant_echec)
            print(
                f"Joueur '{joueur.first_name} - {joueur.last_name} - {joueur.date_of_birth} - ({joueur.chess_id})' ajouté à la liste.")

    def display_player_list(self):
        joueurs = self.tournament_controller.get_players()
        self.player_list_view.display_players(joueurs)

    def create_tournament(self):
        nom = input("Entrez le nom du tournoi : ")
        lieu = input("Entrez le lieu du tournoi : ")
        date_debut = input("Entrez la date de début du tournoi : ")
        date_fin = input("Entrez la date de fin du tournoi : ")
        tournoi = self.tournament_controller.create_tournament(nom, lieu, date_debut, date_fin)
        print(f"Tournoi '{tournoi.name}' créé !")

    def add_player_to_tournament(self):
        tournois = self.tournament_controller.get_tournaments()
        self.tournament_list_view.display_tournaments(tournois)
        index_tournoi = int(input("Entrez l'index du tournoi auquel ajouter un joueur : "))
        prenom_joueur = input("Entrez le prénom du joueur : ")
        nom_joueur = input("Entrez le nom du joueur : ")
        joueur = self.tournament_controller.add_player_to_tournament(index_tournoi, prenom_joueur, nom_joueur)
        print(f"Joueur '{joueur.first_name} {joueur.last_name}' ajouté au tournoi.")

    def generate_rounds(self):
        tournois = self.tournament_controller.get_tournaments()
        self.tournament_list_view.display_tournaments(tournois)
        index_tournoi = int(input("Entrez l'index du tournoi pour générer les rounds : "))
        self.tournament_controller.generate_rounds(index_tournoi)
        print("Rounds générés pour le tournoi.")

    def record_match_result(self):
        # Logique pour enregistrer le résultat d'un match
        pass

    def display_tournaments(self):
        tournois = self.tournament_controller.get_tournaments()
        self.tournament_list_view.display_tournaments(tournois)

    def display_tournament_details(self):
        tournois = self.tournament_controller.get_tournaments()
        self.tournament_list_view.display_tournaments(tournois)
        index_tournoi = int(input("Entrez l'index du tournoi pour afficher les détails : "))
        tournoi = tournois[index_tournoi]
        self.tournament_detail_view.display_rounds(tournoi.rounds)
        self.tournament_detail_view.display_matches(tournoi.rounds[-1].matches)  # Afficher les matchs du dernier round
