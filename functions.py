class Automate :

    def __init__(self, alphabet, etats, initial, final, transition):
        self.alphabet = alphabet
        self.etats = etats
        self.initial = initial
        self.final = final
        self.transition = transition

def lecture_automate(chemin):

    with open(chemin, 'r') as AF:
        donnees = [ligne.strip() for ligne in AF.readlines()]

    nb_transitions = int(donnees[4])

    etats_initiaux = donnees[2].split()[1:]
    etats_finaux = donnees[3].split()[1:]

    transitions = []
    lettres = []
    etats = []

    for donnee in donnees[5:5+nb_transitions]:
        depart, lettre, arrivee = donnee.split()

        transitions.append((depart, lettre, arrivee))

        if lettre not in lettres:
                lettres.append(lettre)
        lettres.sort()

        if depart not in etats:
            etats.append(depart)

        if arrivee not in etats:
                etats.append(arrivee)
            
        etats.sort()

    return Automate(lettres, etats, etats_initiaux, etats_finaux, transitions)
