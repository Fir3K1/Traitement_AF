from functions import *

def main():
    automate = None
    
    while True:
        print("\n" + "="*40)
        print("          MENU PRINCIPAL")
        print("="*40)
        print("1. Charger un autre automate (ou lancer pour la 1ère fois)")
        print("2. Standardisation")
        print("3. Déterminisation")
        print("4. Minimisation")
        print("5. Reconnaissance de mots")
        print("6. Créer l'automate complémentaire")
        print("0. Quitter le programme")
        
        choix = input("\nChoisissez une option : ")

        if choix == "0":
            print("Fin du programme. Au revoir !")
            break
            
        elif choix == "1" or automate is None:
            if automate is None and choix != "1":
                print("-> Veuillez d'abord charger un automate (Option 1).")
            
            while True:
                try:
                    num_AF = int(input("\nSaisissez le numéro de l'automate (1 à 44) : "))
                    if 1 <= num_AF <= 44:
                        break
                    print("Valeur incorrecte. Veuillez taper un nombre entre 1 et 44.")
                except ValueError:
                    print("Valeur incorrecte. Veuillez entrer un entier.")
            
            chemin = f"AF/AF{num_AF}.txt"
            automate = lecture_automate(chemin)
            print(f"\n[+] Automate n°{num_AF} chargé avec succès !")
            print(Affichage(automate.alphabet, automate.etats, automate.initial, automate.final, automate.transitions))

        elif automate is not None:
            if choix == "2":
                print("\n--- 2. Standardisation ---")
                if not automate.est_standard():
                    choix_std = input("Voulez-vous standardiser cet automate ? (o/n) : ")
                    if choix_std.lower() == 'o':
                        automate = automate.standardiser()
                        print("\nAutomate standardisé :")
                        print(Affichage(automate.alphabet, automate.etats, automate.initial, automate.final, automate.transitions))
                else:
                    print("L'automate est déjà standard.")
                    
            elif choix == "3":
                print("\n--- 5. Déterminisation ---")
                automate = automate.determiniser()
                print("\n[+] L'automate a été déterminisé avec succès et mis à jour en mémoire.")
                print(Affichage(automate.alphabet, automate.etats, automate.initial, automate.final, automate.transitions))

            elif choix == "4":
                print("\n--- 6. Minimisation ---")
                automate = automate.Minimisation()
                print("\n[+] L'automate a été minimisé avec succès et mis à jour en mémoire.")
                print(Affichage(automate.alphabet, automate.etats, automate.initial, automate.final, automate.transitions))
                    
            elif choix == "5":
                print("\n--- 7. Reconnaissance de mots ---")
                
                if not automate.est_deterministe():
                    print("Action impossible : L'automate n'est pas déterministe.")
                    print("Veuillez d'abord exécuter la déterminisation ")
                else:
                    print("Tapez 'fin' pour arrêter et revenir au menu principal.")
                    while True:
                        mot = input("\nSaisissez un mot à vérifier : ")
                        
                        if mot.strip().lower() == "fin":
                            print("Retour au menu principal...")
                            break
                            
                        if automate.recognizes_string(mot.strip()):
                            print(f" ==> Le mot est RECONNU par l'automate !")
                        else:
                            print(f" ==> Le mot n'est PAS RECONNU par l'automate !")

            elif choix == "6":
                print("\n--- 8. Construire l'Automate Complémentaire ---")
                
                if not automate.est_deterministe() or not automate.est_complet():
                    print("Action impossible : L'automate est actuellement non AFDC (Déterministe ET Complet).")
                    print("Veuillez d'abord exécuter la déterminisation et la complétion.")
                else:
                    automate_complementaire = automate.get_complementary()
                    
                    if automate_complementaire:
                        print("\n[+] Automate complémentaire généré avec succès !")
                        print(Affichage(automate_complementaire.alphabet, 
                                        automate_complementaire.etats, 
                                        automate_complementaire.initial, 
                                        automate_complementaire.final, 
                                        automate_complementaire.transitions))
                        
                        remplacer = input("\nVoulez-vous écraser l'automate temporaire en mémoire par celui-ci ? (o/n) : ")
                        if remplacer.lower() == 'o':
                            automate = automate_complementaire
                            print("L'automate courant a été mis à jour dans la mémoire.")
            else:
                print("Option invalide.")

if __name__ == "__main__":
    main()