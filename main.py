from functions import *


def afficher_menu():
    print("\n\nMENU PRINCIPAL\n\n")
    print("  1. Afficher l'automate courant")
    print("  2. Tests (standard / deterministe / complet)")
    print("  3. Standardiser")
    print("  4. Determiniser et completer -> AFDC")
    print("  5. Minimiser -> AFDCM")
    print("  6. Reconnaitre des mots")
    print("  7. Automate complementaire")
    print("  8. Changer d'automate")
    print("  0. Quitter\n")



def charger_automate():
    """Demande un numéro d'automate et retourne l'objet Automate chargé."""
    while True:
        try:
            num = int(input("\nNumero de l'automate a charger (1-44), ou 0 pour quitter : "))
        except ValueError:
            print("  Erreur : entier attendu.")
            continue

        if num == 0:
            return None  # signal de sortie

        if not (1 <= num <= 44):
            print("  Erreur : numero entre 1 et 44.")
            continue

        chemin = f"AF/AF{num}.txt"
        try:
            af = lecture_automate(chemin)
            print(f"\n  Automate n°{num} charge avec succes.")
            print(af.Affichage())
            return af
        except FileNotFoundError:
            print(f"  Erreur : fichier '{chemin}' introuvable.")


def main():
    print("\n" + "=" * 55)
    print("   TRAITEMENT D'AUTOMATES FINIS - EFREI P2 2025/2026")
    print("=" * 55)


    while True:

        af    = None   # Automate courant (original ou standardise)
        afdc  = None   # Automate Deterministe Complet
        afdcm = None   # Automate Deterministe Complet Minimal

        af = charger_automate()
        if af is None:
            print("\nFin du programme. Au revoir !")
            return

        while True:
            afficher_menu()

            try:
                choix = int(input("\nVotre choix : "))
            except ValueError:
                print("  Erreur : entier attendu.")
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

                print("\n--- Test : deterministe ---")
                det = af.est_deterministe()

                print("\n--- Test : complet ---")
                if det:
                    af.est_complet()
                else:
                    print("  (test 'complet' ignore : l'automate n'est pas deterministe)")

            elif choix == 3:
                print("\n--- Standardisation ---")
                if af.est_standard():
                    print("  L'automate est deja standard, aucune action necessaire.")
                else:
                    rep = input("  Voulez-vous standardiser cet automate ? (o/n) : ").strip().lower()
                    if rep == 'o':
                        af    = af.standardiser()
                        afdc  = None   # invalider AFDC/AFDCM anterieurs
                        afdcm = None
                        print("\n  Automate standardise :")
                        print(af.Affichage())
                    else:
                        print("  Standardisation annulee.")


            elif choix == 4:
                print("\n--- Determinisation et completion ---")
                #resultat = af.Determinisation_et_completion()
                resultat = af.Completion()
                if resultat is None:
                    print("  Erreur : la determinisation a echoue.")
                else:
                    afdc  = resultat
                    afdcm = None
                    afdc.Affichage_AFDC()

            elif choix == 5:
                print("\n--- Minimisation ---")
                if afdc is None:
                    print("  Action impossible : veuillez d'abord determiniser (option 4).")
                else:
                    afdcm = afdc.Affichage_Minimisation()


            elif choix == 6:
                print("\n--- Reconnaissance de mots ---")

                cible = afdc if afdc is not None else af

                if not cible.est_deterministe():
                    print("  Action impossible : l'automate utilise n'est pas deterministe.")
                    print("  Veuillez d'abord executer la determinisation (option 4).")
                else:
                    print("  Automate utilise :", "AFDC" if afdc is not None else "AF courant")
                    print("  (tapez 'fin' pour revenir au menu)\n")
                    while True:
                        mot = input("  Mot a tester : ").strip()
                        if mot.lower() == 'fin':
                            print("  Retour au menu.")
                            break
                        if cible.lire_mot(mot):
                            print(f"  ==> '{mot}' est RECONNU par l'automate.")
                        else:
                            print(f"  ==> '{mot}' n'est PAS reconnu par l'automate.")


            elif choix == 7:
                print("\n--- Automate complementaire ---")
                if afdc is None:
                    print("  Action impossible : veuillez d'abord determiniser (option 4).")
                else:
                    # Choix de la base : AFDC ou AFDCM
                    if afdcm is not None:
                        print("  Construire le complementaire depuis :")
                        print("    a) L'AFDC")
                        print("    b) L'AFDCM (automate minimal)")
                        base_choix = input("  Votre choix (a/b) : ").strip().lower()
                        if base_choix == 'b':
                            base, source = afdcm, "AFDCM"
                        else:
                            base, source = afdc, "AFDC"
                    else:
                        base, source = afdc, "AFDC"

                    print(f"\n  Complementaire construit depuis : {source}")
                    comp = base.automate_complementaire()

                    if comp is not None:
                        print("\n  Automate complementaire :")
                        # Si les etats sont des tuples (AFDC non renomme), on utilise Affichage_AFDC
                        if any(isinstance(e, tuple) for e in comp.etats):
                            comp.Affichage_AFDC("Automate Complementaire")
                        else:
                            print(comp.Affichage())

                        rep = input("\n  Remplacer l'automate courant par le complementaire ? (o/n) : ").strip().lower()
                        if rep == 'o':
                            af    = comp
                            afdc  = None
                            afdcm = None
                            print("  Automate courant mis a jour.")

            elif choix == 8:
                print("\n  Changement d'automate.")
                break

            else:
                print("  Option invalide. Choisissez entre 0 et 8.")



main()