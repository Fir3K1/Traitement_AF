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

    nb_transitions = int(donnees[4]) # int : nombre de transitions

    etats_initiaux = donnees[2].split()[1:] # char : récupère l'état initial
    etats_finaux = donnees[3].split()[1:] # char : récupère l'état final

    transitions = [] # liste dans laquel il y aura des tuples de trois éléments (départ, lettre, arrivée) représentant une transition
    lettres = [] # liste des lettres 
    etats = [] #liste des états

    for donnee in donnees[5:5+nb_transitions]:
        depart, lettre, arrivee = donnee.split() #récupère les éléments (char) qui son séparés d'un espace

        transitions.append((depart, lettre, arrivee)) #insère le tuple dans la liste des transitions

        #insère la lettre dans la liste si elle n'y est pas encore 
        if lettre not in lettres:
                lettres.append(lettre)
        lettres.sort() #range dans l'ordre

        if depart not in etats:
            etats.append(depart)

        if arrivee not in etats:
                etats.append(arrivee)
            
        etats.sort()

    return Automate(lettres, etats, etats_initiaux, etats_finaux, transitions)
