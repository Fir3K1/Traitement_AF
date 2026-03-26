class Automate :

    def __init__(self, alphabet, etats, initial, final, transitions):
        self.alphabet = alphabet    #['a', 'b']
        self.etats = etats  #['0', '1', '2', '3', '4']
        self.initial = initial  #['1', '3']
        self.final = final  #['2', '4']
        self.transitions = transitions    #[('0', 'a', '0'), ('0', 'b', '0'), ('1', 'a', '2'), ('1', 'b', '0'), ('3', 'a', '0'), ('3', 'b', '4')]

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

#print(lecture_automate(r"C:\Users\tsunt\Desktop\Traitement_AF\AF\AF5.txt").alphabet)

def Completion(self):
    #on définir la poubelle
    p=len(self.etats)
    #on parcours tous les etats et leurs transitions pour detecter si une transition manque
    for etat in self.etats:
        for lettre in self.alphabet:
            trouve=False
            for transi in self.transitions:
                if transi[0]==etat and transi[1]==lettre:
                    trouve=True
            if trouve==False:
                new_transi=(etat,lettre,p)
                self.transitions.append(new_transi) #on redirige les transitions manquantes vers cet état poubelle

    self.etats.append(p)
    #on ajoute l'etat poubelle p à la liste d'états
    for lettre in self.alphabet:
        new_transi=(p, lettre,p )   
        self.transitions.append(new_transi) 
        #l'état poubelle a ses propres transitions vers lui meme pour chaque lettre
      

 



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

