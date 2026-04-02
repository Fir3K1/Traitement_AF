from functions import *


def afficher_menu():
    print("\n\nMENU PRINCIPAL\n\n")
    print("  1. Afficher l'automate ")
    print("  2. Tests (standard / deterministe / complet)")
    print("  3. Standardiser")
    print("  4. Déterminiser et compléter -> AFDC")
    print("  5. Minimiser -> AFDCM")
    print("  6. Reconnaître des mots")
    print("  7. Automate complémentaire")
    print("  8. Changer d'automate")
    print("  0. Quitter\n")



def main():

    print("\n\n   TRAITEMENT D'AUTOMATES FINIS - EFREI P2 2025/2026\n")

    trace = input("\nVoulez-vous générer les traces d'éxecution des automates ? (o/n) : ").strip().lower()
    if trace == 'o':
        print("\nGénération des traces d'éxecution de tous les automates.")
        # Génération des 44 fichiers de trace
        for i in range(1, 45):
            print(i)
            Ecriture_trace(f"AF/AF{i}.txt", f"traces/trace_AF{i}.txt")

    
    print("\nLancement du programme de traitement d'automates.")


    while True:

        af = None   # Automate original ou standardise
        afdc = None   # Automate déterministe complet
        afdcm = None   # Automate déterministe complet minimal

        try:
            num = int(input("Numéro de l'automate à charger (1-44), ou 0 pour quitter : "))
        except ValueError:
            print("--> Erreur : entier attendu.")
            continue

        if num == 0:
            return None  # signal de sortie
        if not (1 <= num <= 44):
            print("--> Erreur : numéro entre 1 et 44.")
            continue

        chemin = f"AF/AF{num}.txt"
        try:
            af = lecture_automate(chemin)
            print(f"\nAutomate n°{num} chargé avec succès.")
            print(af.Affichage())
        except FileNotFoundError:
            print(f"--> Erreur : fichier '{chemin}' introuvable.")


        if af is None:
            print("\nFin du programme. Au revoir !")
            return

        while True:
            afficher_menu()

            try:
                choix = int(input("\nVotre choix : "))
            except ValueError:
                print("--> Erreur : entier attendu.")
                continue

            if choix == 0:
                print("\nFin du programme. Au revoir !")
                return

            elif choix == 1:
                print("\n--- Automate courant ---")
                print(af.Affichage())

            elif choix == 2:
                print("\n--- Test : standard ---")
                af.est_standard()

                print("\n--- Test : déterministe ---")
                det = af.est_deterministe()

                print("\n--- Test : complet ---")
                if det:
                    af.Completion()
                    print(af.Affichage())
                    af.est_complet()
                    

                else:
                    print("L'automate n'est pas deterministe donc il n'est pas complet. ")

            elif choix == 3:
                print("\n--- Standardisation ---")
                if af.est_standard():
                    print("L'automate est deja standard, aucune action necessaire.")
                else:
                    rep = input("Voulez-vous standardiser cet automate ? (o/n) : ").strip().lower()
                    if rep == 'o':
                        af    = af.standardiser()
                        afdc  = None   # invalider AFDC/AFDCM anterieurs
                        afdcm = None
                        print("\n Automate standardise :")
                        print(af.Affichage())
                    else:
                        print("Standardisation annulée.")

            elif choix == 4:
                print("\n--- Déterminisation et complétion ---")
                if af.est_deterministe():
                    print("L'automate est déjà déterministe.")
                    af.Completion()
                    afdc = af
                else: 
                    afdc = af.Determinisation_et_completion()
                afdcm = None

            elif choix == 5:
                print("\n--- Minimisation ---")
                if afdc is None:
                    print("Action impossible : veuillez d'abord déterminiser l'automate (option 4).")
                else:
                    afdcm = afdc.Affichage_Minimisation()

            elif choix == 6:
                print("\n--- Reconnaissance de mots ---")

                cible = afdcm if afdcm is not None else afdc

                if not cible.est_deterministe():
                    print("Action impossible : l'automate utilise n'est pas deterministe.")
                    print("Veuillez d'abord éxecuter la déterminisation sur l'automate (option 4).")
                else:
                    print("Automate utilise :", "AFDC" if afdc is not None else "AF courant")
                    print("(tapez 'fin' pour revenir au menu)\n")
                    while True:
                        mot = input(" Mot a tester : ").strip()
                        if mot.lower() == 'fin':
                            print(" Retour au menu.")
                            break
                        if cible.lire_mot(mot):
                            print(f" ==> '{mot}' est RECONNU par l'automate.")
                        else:
                            print(f" ==> '{mot}' n'est PAS reconnu par l'automate.")

            elif choix == 7:
                print("\n--- Automate complementaire ---")
                if afdc is None:
                    print("Action impossible : veuillez d'abord determiniser (option 4).")
                else:
                    # Choix de la base : AFDC ou AFDCM
                    if afdcm is not None:
                        print("Construire le complementaire depuis :")
                        print("  a) L'AFDC")
                        print("  b) L'AFDCM (automate minimal)")
                        base_choix = input("Votre choix (a/b) : ").strip().lower()
                        if base_choix == 'b':
                            base, source = afdcm, "AFDCM"
                        else:
                            base, source = afdc, "AFDC"
                    else:
                        base, source = afdc, "AFDC"

                    print(f"\nComplémentaire construit depuis : {source}")
                    comp = base.automate_complementaire()

                    if comp is not None:
                        print("\nAutomate complémentaire :")
                        # Si les etats sont des tuples (AFDC non renomme), on utilise Affichage_AFDC
                        if any(isinstance(e, tuple) for e in comp.etats):
                            comp.Affichage()
                        else:
                            print(comp.Affichage())

                        rep = input("\nRemplacer l'automate courant par le complémentaire ? (o/n) : ").strip().lower()
                        if rep == 'o':
                            af    = comp
                            afdc  = None
                            afdcm = None
                            print("Automate courant mis à jour.")

            elif choix == 8:
                print("\nChangement d'automate.")
                break

            else:
                print("Option invalide. Choisissez entre 0 et 8.")



main()