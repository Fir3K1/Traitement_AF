from functions import *

def main():
    print("Quel automate souhaitez-vous tester ?")

    while True:
        try:
            AF = int(input("Saisissez un numéro entre 1 et 44 : "))
            if 1 <= AF <= 44:
                break
            else:
                print("\nValeur incorrecte. ")
        except ValueError:
            print("\nValeur incorrecte. ")

    chemin = f"AF/AF{str(AF)}.txt"

    automate = lecture_automate(chemin)
    print(automate)

    print(Affichage(automate.alphabet, automate.etats, automate.initial, automate.final, automate.transitions))

    print("Déterministe :", automate.est_deterministe())
    print("Complet :", automate.est_complet())
    print("Standard :", automate.est_standard())

    if not automate.est_standard():
        choix = input("Standardiser ? (o/n) : ")
        if choix == 'o':
            automate = automate.standardiser()
            print("Automate standardisé :")
            print(Affichage(automate.alphabet, automate.etats, automate.initial, automate.final, automate.transitions))

    print("Fin")
    
main()