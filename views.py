# views.py

import re
import json
import os
from datetime import datetime

class PlayerListView:
    def create_player_list(self, player_controller):
        print("Création de la Liste de Joueurs")
        while True:
            print("Entrez les informations du joueur ('q' pour quitter) :")
            nom_joueur = input("Nom du joueur : ")
            if nom_joueur.lower() == "q":
                break
            prenom_joueur = input("Prénom du joueur : ")
            date_naissance_joueur = input("Date de Naissance du joueur (JJ-MM-AAAA) : ")
            identifiant_echec = input("Identifiant Echec du joueur (2 lettres majuscules + 5 chiffres) : ")

            if not re.match(r"^[A-Z]{2}\d{5}$", identifiant_echec):
                print("L'identifiant Echec doit contenir 2 lettres majuscules suivies de 5 chiffres.")
                continue

            try:
                date_naissance = datetime.strptime(date_naissance_joueur, "%d-%m-%Y")
            except ValueError:
                print("Format de date invalide. Veuillez utiliser le format JJ-MM-AAAA.")
                continue

            player_controller.add_player(nom_joueur, prenom_joueur, date_naissance, identifiant_echec)
            print("Joueur ajouté à la liste.")

    def display_player_list(self, player_controller):
        players = player_controller.get_players()
        print("Liste des Joueurs :")
        for player in players:
            print(f"Nom: {player.first_name} {player.last_name}")
            print(f"Date de naissance: {player.date_of_birth.strftime('%d-%m-%Y')}")
            print(f"ID Échecs: {player.chess_id}")
            print()


class TournamentCreationView:
    def create_tournament(self, tournament_controller):
        print("Enregistrement d'un tournoi")
        nom = input("Entrez le nom du tournoi : ")
        ville = input("Entrez la ville du tournoi : ")
        date_debut_str = input("Entrez la date de début du tournoi (JJ/MM/AAAA) : ")
        date_fin_str = input("Entrez la date de fin du tournoi (JJ/MM/AAAA) : ")

        try:
            date_debut = datetime.strptime(date_debut_str, "%d/%m/%Y")
            date_fin = datetime.strptime(date_fin_str, "%d/%m/%Y")
        except ValueError:
            print("Format de date invalide. Veuillez utiliser le format JJ/MM/AAAA.")
            return

        tournament_controller.create_tournament(nom, ville, date_debut, date_fin)
        print(f"Tournoi enregistré avec succès !")


class TournamentListView:
    def display_tournaments(self, tournament_controller):
        tournaments = tournament_controller.get_tournaments()
        if not tournaments:
            print("Aucun tournoi enregistré.")
        else:
            print("Liste des Tournois :")
            for tournament in tournaments:
                print(f"Identifiant: {tournament.tournament_id}")
                print(f"Nom: {tournament.name}")
                print(f"Lieu: {tournament.location}")
                print(f"Date de début: {tournament.start_date.strftime('%d-%m-%Y')}")
                print(f"Date de fin: {tournament.end_date.strftime('%d-%m-%Y')}")
                print(f"Nombre de tours: {tournament.number_of_rounds}")
                print()

    def select_tournament(self, tournament_controller):
        tournament_id = input("Spécifiez l'identifiant du tournoi ('q' pour quitter) : ")
        if tournament_id.lower() == "q":
            return None
        tournament = tournament_controller.get_tournament_by_id(tournament_id)
        if tournament is None:
            print("Aucun tournoi trouvé avec cet identifiant.")
        return tournament


    def display_players(self, tournament):
        print(f"Liste des joueurs pour le tournoi '{tournament.name}' :")
        players = tournament.get_players()
        for player in players:
            print(f"Nom: {player['first_name']} {player['last_name']}")
            print(f"Date de naissance: {player['date_of_birth']}")
            print(f"ID Échecs: {player['chess_id']}")
            print()

    def manage_tournament(self, tournament_controller):
        tournament_id = input("Spécifiez l'identifiant du tournoi : ")
        tournament = tournament_controller.get_tournament_by_id(tournament_id)
        if tournament is None:
            print("Aucun tournoi trouvé avec cet identifiant.")
            return
        self.display_players(tournament)

    def create_player_list(self, player_controller):
        print("Création de la Liste de Joueurs")
        while True:
            print("Entrez les informations du joueur ('q' pour quitter) :")
            nom_joueur = input("Nom du joueur : ")
            if nom_joueur.lower() == "q":
                break
            prenom_joueur = input("Prénom du joueur : ")
            date_naissance_joueur = input("Date de Naissance du joueur (JJ-MM-AAAA) : ")
            identifiant_echec = input("Identifiant Echec du joueur (2 lettres majuscules + 5 chiffres) : ")

            if not re.match(r"^[A-Z]{2}\d{5}$", identifiant_echec):
                print("L'identifiant Echec doit contenir 2 lettres majuscules suivies de 5 chiffres.")
                continue

            try:
                date_naissance = datetime.strptime(date_naissance_joueur, "%d-%m-%Y")
            except ValueError:
                print("Format de date invalide. Veuillez utiliser le format JJ-MM-AAAA.")
                continue

            player_controller.add_player(nom_joueur, prenom_joueur, date_naissance, identifiant_echec)
            print("Joueur ajouté à la liste.")

    def display_player_list(self, player_controller):
        players = player_controller.get_players()
        print("Liste des Joueurs :")
        for player in players:
            print(f"Nom: {player.first_name} {player.last_name}")
            print(f"Date de naissance: {player.date_of_birth.strftime('%d-%m-%Y')}")
            print(f"ID Échecs: {player.chess_id}")
            print()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
JOUEURS_DIR = os.path.join(DATA_DIR, "joueurs")
os.makedirs(JOUEURS_DIR, exist_ok=True)
