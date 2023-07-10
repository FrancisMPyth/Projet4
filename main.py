
# main.py


from controllers import TournamentController
from views import PlayerListView, TournamentListView, TournamentDetailView


def main():
    tournament_controller = TournamentController()
    player_list_view = PlayerListView()
    tournament_list_view = TournamentListView()
    tournament_detail_view = TournamentDetailView()

    while True:
        print("Menu Principal:")
        print("1. Créer un Tournoi")
        print("2. Ajouter un Joueur au Tournoi")
        print("3. Générer les Rounds")
        print("4. Enregistrer le Résultat d'un Match")
        print("5. Afficher la Liste des Joueurs")
        print("6. Afficher la Liste des Tournois")
        print("7. Afficher les Détails d'un Tournoi")
        print("q. Quitter")

        choix = input("Entrez votre choix : ")

        if choix == "1":
            nom = input("Entrez le nom du tournoi : ")
            lieu = input("Entrez le lieu du tournoi : ")
            date_debut = input("Entrez la date de début du tournoi : ")
            date_fin = input("Entrez la date de fin du tournoi : ")
            tournoi = tournament_controller.create_tournament(nom, lieu, date_debut, date_fin)
            print(f"Tournoi '{tournoi.nom}' créé !")
        elif choix == "2":
            tournament_list_view.display_tournaments(tournament_controller.get_tournaments())
            index_tournoi = int(input("Entrez l'index du tournoi auquel ajouter un joueur : "))
            prenom_joueur = input("Entrez le prénom du joueur : ")
            nom_joueur = input("Entrez le nom du joueur : ")
            joueur = tournament_controller.add_player_to_tournament(index_tournoi, prenom_joueur, nom_joueur)
            print(f"Joueur '{joueur.prenom} {joueur.nom}' ajouté au tournoi.")
        elif choix == "3":
            tournament_list_view.display_tournaments(tournament_controller.get_tournaments())
            index_tournoi = int(input("Entrez l'index du tournoi pour générer les rounds : "))
            tournament_controller.generate_rounds(index_tournoi)
            print("Rounds générés pour le tournoi.")
        elif choix == "4":
            # Logique pour enregistrer le résultat d'un match
            pass
        elif choix == "5":
            joueurs = tournament_controller.get_players()
            player_list_view.display_players(joueurs)
        elif choix == "6":
            tournois = tournament_controller.get_tournaments()
            tournament_list_view.display_tournaments(tournois)
        elif choix == "7":
            tournois = tournament_controller.get_tournaments()
            tournament_list_view.display_tournaments(tournois)
            index_tournoi = int(input("Entrez l'index du tournoi pour afficher les détails : "))
            tournoi = tournois[index_tournoi]
            tournament_detail_view.display_rounds(tournoi.rounds)
            tournament_detail_view.display_matches(tournoi.rounds[-1].matches)  # Afficher les matchs du dernier round
        elif choix.lower() == "q":
            break
        else:
            print("Entrée invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
