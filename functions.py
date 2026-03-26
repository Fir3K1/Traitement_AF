from tabulate import tabulate


class Automate :

    def __init__(self, alphabet, etats, initial, final, transitions):
        self.alphabet = alphabet    #['a', 'b']
        self.etats = etats  #['0', '1', '2', '3', '4']
        self.initial = initial  #['1', '3']
        self.final = final  #['2', '4']
        self.transitions = transitions    #[('0', 'a', '0'), ('0', 'b', '0'), ('1', 'a', '2'), ('1', 'b', '0'), ('3', 'a', '0'), ('3', 'b', '4')]

    def __str__(self):
        return (
            f"Alphabet : {self.alphabet}\n"
            f"Etats : {self.etats}\n"
            f"Initial : {self.initial}\n"
            f"Final : {self.final}\n"
            f"Transitions : {self.transitions}\n"
        )

    def est_deterministe(self):
        # 1 seul état initial
        if len(self.initial)!=1:
            print("Non déterministe : on retrouve plusieurs états initiaux !")
            return False
        transition_vues=set()
        for transition in self.transitions:
            e = transition[0]  # état de départ
            l = transition[1]  # symbole
            f = transition[2]  # état d’arrivée
            if (e,l) in transition_vues:
                print(f"Non déterministe : plusieurs transitions depuis {e} avec le même symbole {l} !")
                return False
            transition_vues.add((e,l))
        return True

    def est_complet(self):
        for e in self.etats:
            for l in self.alphabet:
                trouve = False
                for transition in self.transitions:
                    tmpe= transition[0]
                    tmpl= transition[1]
                    f= transition[2]
                    if tmpe==e and tmpl==l:
                        trouve = True
                        break
                if not trouve:
                    print(f"Non complet : pas de transition de {e} avec le symbole {l} !")
        return True #on peut retourner trouve aussi, mais pour être rigoureux, on retourne True.

    def est_standard(self):
        # 1 seul état initial
        if len(self.initial) != 1:
            print("Non standard : plusieurs états initiaux !")
            return False

        i = self.initial[0]

        # Aucune transition ne doit arriver vers l'état initial
        for transition in self.transitions:
            dep = transition[0]
            lettre = transition[1]
            arr = transition[2]

            if arr == i:
                print(f"Non standard : transition vers l’état initial depuis {dep} avec le symbole {lettre}")
                return False

        return True

    def standardiser(self):
        # 1) Si l'automate est déjà standard, on ne fait rien
        if self.est_standard():
            print("Déjà standard")
            return self

        # 2) Créer un nouvel état initial
        nouveau_init = "i"

        # 3) Ajouter ce nouvel état aux états existants
        nouveaux_etats = self.etats + [nouveau_init]

        # 4) Copier toutes les transitions existantes
        nouvelles_transitions = self.transitions.copy()

        # 5) Copier les transitions des anciens états initiaux
        for ancien_init in self.initial:
            for transition in self.transitions:
                dep = transition[0]
                lettre = transition[1]
                arr = transition[2]

                # Si une transition part d'un ancien état initial, on la duplique en partant du nouvel état initial
                if dep == ancien_init:
                    nouvelles_transitions.append((nouveau_init, lettre, arr))

        # 6) Construire et renvoyer le nouvel automate standardisé
        return Automate(
            self.alphabet,
            nouveaux_etats,
            [nouveau_init],  # le nouvel état initial
            self.final,
            nouvelles_transitions
        )

    def Appartenance_groupe(self, destination: int, groupes: dict):
        """renvoie le nom du groupe auquel la destination appartient"""
        for cle in groupes.keys():
            if destination in groupes[cle]: return cle


    def Diviseur_Etat(self, etats: list[str], groupes: dict):
        '''Diviser etats en groupes quand les transitions sont les mêmes
        Retourne un dictionnaire (groupes)'''
        groupes_temp = {}
        for etat in etats:
            chaine_transi = ""  # chaque destination (groupe) pour chaque lettre dans l'ordre
            for lettre in self.alphabet:
                for transition in self.transitions:
                    if (transition[0] == etat) and (
                            transition[1] == lettre):  # si transi qui concerne état et lettre trouvée
                        # print(etat, lettre, transition)
                        chaine_transi += self.Appartenance_groupe(transition[2],
                                                             groupes)  # reconstruction de table de transi linéaire
                        break
            if chaine_transi in groupes_temp.keys():
                groupes_temp[chaine_transi].append(etat)
            else:
                groupes_temp[chaine_transi] = [etat]
        return groupes_temp  # {'01': ['0', '1'], '23': ['2'], '12': ['3']} clés sont les chemins pour chaque lettre, valeurs


    def Fusion_dicos(self, dico1: dict, dico2: dict):
        """crée un nouveau dictionnaire et renomme les états au passage"""
        res = {}
        for i in range(len(dico1)):
            res[f"I{i}"] = list(dico1.values())[i]
        for i in range(len(dico2)):
            res[f"I{i + len(dico1)}"] = list(dico2.values())[i]
        return res





    def Minimisation(self):
        terminaux = self.final.copy()
        print(terminaux)
        non_terminaux = [x for x in self.etats if x not in terminaux]
        groupes_temp = {"I0": terminaux, "I1": non_terminaux}
        groupes_next = self.Fusion_dicos(self.Diviseur_Etat(groupes_temp['I0'], groupes_temp),
                                    self.Diviseur_Etat(groupes_temp['I1'], groupes_temp))
        while groupes_temp != groupes_next:
            groupes_temp = groupes_next.copy()
            groupes_next = dict()
            for cle in groupes_temp.keys():
                groupes_next = self.Fusion_dicos(groupes_next, self.Diviseur_Etat(groupes_temp[cle], groupes_temp))
        return groupes_next


def lecture_automate(chemin):

    with open(chemin, 'r') as AF:
        lignes = [ligne.strip() for ligne in AF.readlines()]

    nb_transitions = int(lignes[4]) # int : nombre de transitions

    etats_initiaux = lignes[2].split()[1:] # char : récupère l'état initial
    etats_finaux = lignes[3].split()[1:] # char : récupère l'état final

    transitions = [] # liste dans laquel il y aura des tuples de trois éléments (départ, lettre, arrivée) représentant une transition
    lettres = [] # liste des lettres 
    etats = [] #liste des états

    for ligne in lignes[5:5+nb_transitions]:
        depart, lettre, arrivee = ligne.split() #récupère les éléments (char) qui son séparés d'un espace

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

#print(lecture_automate(r"C:\Users\tsunt\Desktop\Traitement_AF\AF\AF5.txt").alphabet)


test = Automate(['a', 'b'],
                ['0', '0.1', '0.1.2', '0.3', '0.4'],
                ['0'],
                ['0', '0.1', '0.1.2', '0.3'],
                [("0", "a", "0"), ("0", "b", "0.1"),
                 ("0.1", "a", "0"), ("0.1", "b", "0.1.2"),
                 ("0.1.2", "a", "0.3"), ("0.1.2", "b", "0.1.2"),
                 ("0.3", "a", "0.4"), ("0.3", "b", "0.1"),
                 ("0.4", "a", "0"),("0.4", "b", "0.1")]
         )

print(test.Minimisation())


def Affichage(alphabet, etats, etats_initiaux, etats_finaux, transitions):
    donnee = []
    en_tete =[' ', ' '] + alphabet

    for etat in etats:
        ligne = []

        if etat in etats_initiaux and etat in etats_finaux:
            ligne.append('ES')
        elif etat in etats_initiaux:
            ligne.append('E')
        elif etat in etats_finaux:
            ligne.append('S')
        else :
            ligne.append(' ')

        ligne.append(etat)

        for lettre in alphabet:
            arrivee = []
            for elt in transitions:
                if elt[0] == etat and elt[1] == lettre:
                    arrivee.append(elt[2])

            ligne.append(','.join(arrivee))

        donnee.append(ligne)
 
    colonne = ["center"]*(2 + len(alphabet))

    return tabulate(donnee, en_tete, tablefmt="fancy_grid", colalign=colonne)
   


