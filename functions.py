from tabulate import *

class Automate :

    def __init__(self, alphabet, etats, initial, final, transitions):
        self.alphabet = sorted(alphabet)    #['a', 'b']
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

    def Affichage(self):
        alphabet_affiche = [l for l in self.alphabet if l != 'e']
        if 'e' in self.alphabet:
            alphabet_affiche.append('ε')

        donnee = []
        en_tete =[' ', 'etats'] + alphabet_affiche

        for etat in self.etats:
            marqueur = ''

            if etat in self.initial and etat in self.final:
                marqueur = 'ES'
            elif etat in self.initial:
                marqueur = 'E'
            elif etat in self.final:
                marqueur = 'S'

            ligne = [marqueur, etat]
            for lettre in self.alphabet:
                lettre_cle = 'e' if lettre == 'ε' else lettre
                arrivees = [t[2] for t in self.transitions if t[0] == etat and t[1] == lettre_cle]
                ligne.append(','.join(arrivees) if arrivees else '-')

            donnee.append(ligne)

        colonne = ["center"] * len(en_tete)
        return tabulate(donnee, en_tete, tablefmt="fancy_grid", colalign=colonne)


    def est_standard(self):
        # 1 seul état initial
        if len(self.initial) != 1:
            print("Non standard : plusieurs états initiaux.")
            return False

        i = self.initial[0]

        # Aucune transition ne doit arriver vers l'état initial
        for (dep, lettre, arr) in self.transitions:

            if arr == i:
                print(f"Non standard : transition vers l’état initial depuis {dep} avec le symbole {lettre}")
                return False

        print("L'automate est standard.")
        return True


    def standardiser(self):
        # 1) Si l'automate est déjà standard, on ne fait rien
        if self.est_standard():
            print("Déjà standard")
            return self

        # 2) Créer un nouvel état initial
        nouveau_init = "i"

        # 3) Ajouter ce nouvel état aux états existants
        nouveaux_etats = [nouveau_init] + self.etats

        # 4) Copier toutes les transitions existantes
        nouvelles_transitions = list(self.transitions)

        # 5) Copier les transitions des anciens états initiaux
        for ancien_init in self.initial:
            for (dep, lettre, arr) in self.transitions:
                
                # Si une transition part d'un ancien état initial, on la duplique en partant du nouvel état initial
                if dep == ancien_init:
                    t = (nouveau_init, lettre, arr)
                    if t not in nouvelles_transitions:
                        nouvelles_transitions.append(t)

        # 6) Construire et renvoyer le nouvel automate standardisé
        return Automate(
            self.alphabet,
            nouveaux_etats,
            [nouveau_init],  # le nouvel état initial
            self.final,
            nouvelles_transitions
        )


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
                    return False
        return True #on peut retourner trouve aussi, mais pour être rigoureux, on retourne True.
    

    def Completion(self):
        if self.est_complet():
            return self
        
        poubelle = 'P'
        nouv_etats = list(self.etats)
        nouv_transitions = list(self.transitions)
        poubelle_ajoutee = False

        #on parcours tous les etats et leurs transitions pour detecter si une transition manque
        for etat in self.etats:
            for lettre in self.alphabet:
                if not any(t[0] == etat and t[1] == lettre for t in nouv_transitions):
                    if not poubelle_ajoutee:
                        for l in self.alphabet:
                            nouv_transitions.append((poubelle, l, poubelle))
                        poubelle_ajoutee = True
                    nouv_transitions.append((etat, lettre, poubelle))

        return Automate(
            self.alphabet,
            nouv_etats,
            self.initial,
            self.final,
            nouv_transitions
        )
    

    def est_deterministe(self):
        # 1. Vérifier qu'il n'y a qu'un seul état initial
        if len(self.initial) != 1:
            print(f"Non déterministe : {len(self.initial)} état(s) initial/initiaux.")
            return False

        # 2. Vérifier qu'il n'y a pas de ε-transitions
        if 'e' in self.alphabet:
            print("Non déterministe : l'automate est asynchrone (ε-transitions).")
            return False

        # 3. Vérifier qu'il n'y a pas de transitions multiples pour un même état et symbole
        vus = {}
        for (dep, lettre, arr) in self.transitions:
            cle = (dep, lettre)
            if cle in vus:
                print(f"Non déterministe : plusieurs transitions depuis '{dep}' par '{lettre}'.")
                return False
            vus[cle] = True

        print("L'automate est déterministe.")
        return True


    def etat_to_string(self, etat):
        return ".".join(str(e) for e in etat)

    def fermeture_epsilon(self, etats, transitions):
        #etats est une liste d'états
        #la fonction retourne tous les états atteignables par epsilon depuis ces états
        fermeture = list(etats)  #on part des états donnés
        a_traiter = list(etats)
        
        while a_traiter:
            etat = a_traiter.pop(0)
            for transi in transitions:
                if transi[0] == etat and transi[1] == 'e': 
                    if transi[2] not in fermeture:
                        fermeture.append(transi[2])
                        a_traiter.append(transi[2])
        
        return fermeture


    def Determinisation_et_completion(self):
        #D'abord on gère les états initiaux
        transitions_originales = self.transitions.copy()

        new_etat_initial = self.fermeture_epsilon(self.initial, self.transitions)
        self.initial=new_etat_initial

        etats_a_traiter=[self.etat_to_string(self.initial)]
        etats_deja_traite=[list(self.initial)]
        self.etats=list(self.initial)
        self.transitions=[]

        #Ensuite, on déterminise
        while etats_a_traiter:
            etat_present = etats_a_traiter.pop(0) #On prend le 1er element et on le retire de la liste
            for lettre in self.alphabet: #pour chaque lettre, calcul des etats atteignables
                destinations=[] #represente les etats d'arrivés pour une lettre
                for etat in etat_present: #tous les états dans l'état présent (pour couvrir les états composés)
                    for transi in transitions_originales:
                        if transi[0]==etat and transi[1]==lettre and transi[2] not in destinations:
                            destinations.append(transi[2]) #liste d'etats atteignables pour chaque lettre de chaque etat

                destinations = self.fermeture_epsilon(destinations ,transitions_originales)

                if sorted(destinations) not in etats_deja_traite:
                    etats_deja_traite.append(sorted(destinations))
                    etats_a_traiter.append(sorted(destinations))
                self.transitions.append((self.etat_to_string(etat_present), lettre, self.etat_to_string(sorted(destinations))))
        
        #Enfin, on complète l'automate s'il n'est pas deja complet
        self.Completion()
    


    def Affichage_AFDC(self):
        nom_etats = {}

        for etat in self.etats:
            cle = tuple(etat) if isinstance(etat, list) else etat
            if isinstance(etat, (list, tuple)):
                nom_etats[cle] = self.etat_to_string(etat)
            else:
                nom_etats[cle] = str(etat)

        alphabet_sync = [l for l in self.alphabet if l != 'e']
        en_tete = [' ', 'État'] + alphabet_sync
        donnees = []

        for etat in self.etats:
            cle = tuple(etat) if isinstance(etat, list) else etat
            nom_str = nom_etats[cle]

            marqueur = ''
            if etat in self.initial and etat in self.final:
                marqueur = 'ES'
            elif etat in self.initial:
                marqueur = 'E'
            elif etat in self.final:
                marqueur = 'S'

            ligne = [marqueur, nom_str]

            for lettre in alphabet_sync:
                dest = [t[2] for t in self.transitions if t[0] == etat and t[1] == lettre]

                if dest:
                    noms_dest = []
                    for d in dest:
                        cle_d = tuple(d) if isinstance(d, list) else d
                        noms_dest.append(nom_etats.get(cle_d, str(d)))
                    ligne.append(",".join(noms_dest))
                else:
                    ligne.append('-')

            donnees.append(ligne)

        colalign = ['center'] * len(en_tete)
        print(tabulate(donnees, en_tete, tablefmt='fancy_grid', colalign=colalign))

        print("\nTable de correspondance des états :")
        print("-" * 40)

        for etat in self.etats:
            cle = tuple(etat) if isinstance(etat, list) else etat
            nom_str = nom_etats[cle]

            if isinstance(etat, (list, tuple)):
                anciens = ', '.join(str(e) for e in etat)
                print(f"{nom_str:10s} ← {{{anciens}}}")
            else:
                print(f"{nom_str:10s} ← {etat}")

        def etat_to_str(self, etat):
            if not etat:
                return 'P'
            if isinstance(etat, str):
                return etat
            parts = [str(e) for e in etat]

            if all(len(p) == 1 for p in parts):
                return ''.join(parts)
            return '.'.join(parts)



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
    
    from tabulate import tabulate


    def Affichage_Minimisation(self, groupes: dict):
        donnee = []
        en_tete = [' ', 'etats'] + self.alphabet

        for etat in groupes.values():
            marqueur = ''

            if etat[0] in self.initial and etat in self.final:
                marqueur = 'ES'
            elif etat[0] in self.initial:
                marqueur = 'E'
            elif etat[0] in self.final:
                marqueur = 'S'

            ligne = [marqueur, etat]
            for lettre in self.alphabet:
                ligne.append(groupes[self.Appartenance_groupe(etat[0], groupes)])
            print(ligne)
            donnee.append(ligne)
    

    def lire_mot(self, mot):
        
        if not self.est_deterministe():
            print("Erreur : La reconnaissance de mots nécessite un automate déterministe.")
            return False
            
        etat_courant = self.initial[0]
        
        for symbole in mot:
            if symbole not in self.alphabet:
                print(f"Symbole invalide : {symbole}.\nL'automate ne reconnaît pas le mot {mot}.")
                return False
            
            dest = None

            for (dep, lettre, arr) in self.transitions:
                if etat_courant == dep and symbole == lettre :
                    dest = arr
                    break
            
            if dest is None:
                return False 
            etat_courant = dest
            
        return etat_courant in self.final
        

    def automate_complementaire(self):

        if not self.est_deterministe() :
            print("Erreur : L'automate doit être déterministe et complet (AFDC) pour créer son complémentaire.")
            return None
        
        if not self.est_complet():
            print("L'automate doitêtre complet. Faire d'abord la complétion.")
            return None
        
        # Création des nouveaux états finaux (inversion)
        nouveaux_finaux = [etat for etat in self.etats if etat not in self.final]

        # Création et retour du nouvel automate
        return Automate(
            self.alphabet, 
            self.etats, 
            self.initial, 
            nouveaux_finaux, 
            self.transitions
        )


def lecture_automate(chemin):

    with open(chemin, 'r') as AF:
        donnees = [ligne.strip() for ligne in AF.readlines()]

    nb_transitions = int(donnees[4]) # int : nombre de transitions
    nb_etats = int(donnees[1])

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

    for i in range (nb_etats):
        etats.append(str(i))

    return Automate(lettres, etats, etats_initiaux, etats_finaux, transitions)

