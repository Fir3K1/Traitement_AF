from functions import *

def main():
    print("\n" + "="*55)
    print("   TRAITEMENT D'AUTOMATES FINIS - EFREI P2 2025/2026")
    print("="*55)
 
    # Boucle externe : permet de traiter plusieurs automates sans relancer
    while True:
 
        af    = None
        afdc  = None
        afdcm = None
 
        # -- Chargement obligatoire avant tout traitement ----------
        while af is None:
            try:
                num = int(input("\nNumero de l'automate a charger (1-44), ou 0 pour quitter : "))
            except ValueError:
                print("  Entier attendu.")
                continue
            if num == 0:
                print("Fin du programme. Au revoir !")
                return
            if not (1 <= num <= 44):
                print("  Numero entre 1 et 44.")
                continue
            chemin = f"AF/AF{num}.txt"
            try:
                af = lecture_automate(chemin)
                print(f"\n  Automate n°{num} charge.")
                print(af.Affichage())
            except FileNotFoundError:
                print(f"  Fichier '{chemin}' introuvable.")
 
        # -- Boucle de traitement sur l'automate charge ------------
        while True:
            print("\n" + "="*40)
            print("            MENU")
            print("="*40)
            print("  1. Afficher l'automate courant")
            print("  2. Tests (standard / deterministe / complet)")
            print("  3. Standardiser")
            print("  4. Determiniser et completer  -> AFDC")
            print("  5. Minimiser                  -> AFDCM")
            print("  6. Reconnaitre des mots")
            print("  7. Automate complementaire")
            print("  8. Changer d'automate")
            print("  0. Quitter")
 
            try:
                choix = int(input("\nVotre choix : "))
            except ValueError:
                print("  Entier attendu.")
                continue
 
            # -- 0 : Quitter --------------------------------------
            if choix == 0:
                print("Fin du programme. Au revoir !")
                return
 
            # -- 1 : Afficher -------------------------------------
            elif choix == 1:
                print(af.Affichage())
 
            # -- 2 : Tests ----------------------------------------
            elif choix == 2:
                print("\n  --- Test standard ---")
                af.est_standard()
                print("\n  --- Test deterministe ---")
                af.est_deterministe()
                print("\n  --- Test complet ---")
                if af.est_complet():
                    print("L'automate est complet.")
 
            # -- 3 : Standardisation ------------------------------
            elif choix == 3:
                print("\n--- Standardisation ---")
                if af.est_standard():
                    print("L'automate est deja standard, aucune action necessaire.")
                else:
                    rep = input("Voulez-vous standardiser cet automate ? (o/n) : ").strip().lower()
                    if rep == 'o':
                        af   = af.standardiser()
                        afdc = afdcm = None   # invalider AFDC/AFDCM anterieurs
                        print("\nAutomate standardise :")
                        print(af.Affichage())
 
            # -- 4 : Determinisation + completion -----------------
            elif choix == 4:
                print("\n--- Determinisation et completion ---")
                afdc  = af.Determinisation_et_completion()
                afdcm = None
                afdc.Affichage_AFDC()
 
            # -- 5 : Minimisation ---------------------------------
            elif choix == 5:
                print("\n--- Minimisation ---")
                if afdc is None:
                    print("  Action impossible : veuillez d'abord determiniser (option 4).")
                else:
                    afdcm = afdc.Affichage_Minimisation()
 
            # -- 6 : Reconnaissance de mots -----------------------
            elif choix == 6:
                print("\n--- Reconnaissance de mots ---")
                cible = afdc if afdc is not None else af
 
                if not cible.est_deterministe():
                    print("  Action impossible : l'automate n'est pas deterministe.")
                    print("  Veuillez d'abord executer la determinisation (option 4).")
                else:
                    print("  (tapez 'fin' pour revenir au menu)")
                    while True:
                        mot = input("\n  Mot a tester : ").strip()
                        if mot.lower() == 'fin':
                            print("  Retour au menu...")
                            break
                        if cible.lire_mot(mot):
                            print(f"  ==> '{mot}' est RECONNU par l'automate.")
                        else:
                            print(f"  ==> '{mot}' n'est PAS reconnu par l'automate.")
 
            # -- 7 : Automate complementaire ----------------------
            elif choix == 7:
                print("\n--- Automate complementaire ---")
                if afdc is None:
                    print("  Action impossible : veuillez d'abord determiniser (option 4).")
                else:
                    # Le sujet autorise AFDC ou AFDCM au choix
                    if afdcm is not None:
                        print("  Construire le complementaire depuis :")
                        print("    a) L'AFDC")
                        print("    b) L'AFDCM (automate minimal)")
                        base_choix = input("  Votre choix (a/b) : ").strip().lower()
                        base   = afdcm if base_choix == 'b' else afdc
                        source = "AFDCM" if base_choix == 'b' else "AFDC"
                    else:
                        base   = afdc
                        source = "AFDC"
 
                    print(f"\n  Complementaire construit depuis : {source}")
                    comp = base.automate_complementaire()
                    if comp:
                        print("\n  Automate complementaire :")
                        if any(isinstance(e, tuple) for e in comp.etats):
                            comp.Affichage_AFDC("Automate Complementaire")
                        else:
                            print(comp.Affichage())
 
                        rep = input("\n  Remplacer l'automate courant par le complementaire ? (o/n) : ").strip().lower()
                        if rep == 'o':
                            af   = comp
                            afdc = afdcm = None
                            print("  Automate courant mis a jour.")
 
            # -- 8 : Changer d'automate ---------------------------
            elif choix == 8:
                break
 
            else:
                print("  Option invalide. Choisissez entre 0 et 8.")
 
 
if __name__ == "__main__":
    main()
