from tabulate import tabulate


class Automate:
    def __init__(self, alphabet, etats, initial, final, transitions):
        self.alphabet = sorted(alphabet)
        self.etats = etats
        self.initial = initial
        self.final = final
        self.transitions = transitions

    def etat_to_string(self, etat):
        """ Convertit état (liste) en str."""
        return ".".join(str(e) for e in etat)

    # fonction récursive
    def Fermeture_epsilon(self, etats: list):
        """Retourne tous les états atteignables par ε depuis les états dans la liste (longueur 1 si un seul état)"""
        if etats == []: #condition d'arrêt
            return []
        accessibles = []
        for etat in etats:
            for (depart, lettre, arrivee) in self.transitions:
                if depart == etat and lettre == 'e' and (arrivee not in accessibles): # condition initiale
                    accessibles.append(arrivee)
        return accessibles + self.Fermeture_epsilon(accessibles) # états accessibles déjà trouvés + ceux qu'on va trouver


    def Groupes_Fermeture_Epsilon(self, etats: list):
        """Prend une liste d'états en paramètre et renvoie un dico avec chaque état en clé et leurs fermetures ε"""
        res = dict()
        for etat in etats:
            res[etat] = [etat] + self.Fermeture_epsilon(etats)
        return res


    def Fusion_dicos(self, dico1: dict, dico2: dict):
        """Fusionne les dicos (ajoute ou additionne les listes)"""
        res = dict(dico1)
        for cle in dico2.keys():
            if cle in res.keys():
                res[cle] += [x for x in dico2[cle] if x not in res[cle]]
            else:
                res[cle] = dico2[cle]
        return res


    def Affichage(self):
        """Retourne une table de transitions formatée (str)."""
        alphabet_affiche = [l for l in self.alphabet if l != 'e']

        donnee = []
        en_tete = [' ', 'etats'] + alphabet_affiche
        if 'e' in self.alphabet:
            en_tete.append('ε')

        for etat in self.etats:
            if etat in self.initial and etat in self.final:
                marqueur = 'ES' #entrée sortie
            elif etat in self.initial:
                marqueur = 'E' #entrée 
            elif etat in self.final:
                marqueur = 'S' #sortie
            else:
                marqueur = ''

            ligne = [marqueur, str(etat)]
            for lettre in self.alphabet:
                arrivees = [str(t[2]) for t in self.transitions
                              if t[0] == etat and t[1] == lettre]
                arrivees = sorted(arrivees)
                ligne.append('.'.join(arrivees) if arrivees else '-')

            donnee.append(ligne)

        colonne = ['center'] * len(en_tete)
        return tabulate(donnee, en_tete, tablefmt='fancy_grid', colalign=colonne)


    def est_standard(self):
        if len(self.initial) != 1:
            print(f"Non standard : {len(self.initial)} état(s) initial/initiaux.")
            return False
        
        i = self.initial[0]
        cpt = 0
        for (dep, lettre, arr) in self.transitions:
            if arr == i:
                print(f"Non standard : transition vers l'état initial "f"depuis '{dep}' avec '{lettre}'.")
                cpt += 1
        if cpt != 0:
            return False
        
        print("L'automate est standard.")
        return True


    def est_deterministe(self):
        if len(self.initial) != 1:
            print(f"Non déterministe : {len(self.initial)} état(s) initial/initiaux.")
            return False
        
        if 'e' in self.alphabet:
            print("Non déterministe : présence de ε-transitions (automate asynchrone).")
            return False
        
        vus = {}
        for (dep, lettre, arr) in self.transitions:
            cle = (dep, lettre)
            if cle in vus:
                print(f"Non déterministe : plusieurs transitions depuis "f"'{dep}' par '{lettre}'.")
                return False
            vus[cle] = True
        print("L'automate est déterministe.")
        return True

    def est_complet(self):
        cpt = 0

        for etat in self.etats:
            l = []
            for lettre in [x for x in self.alphabet if x != "e"]:
                trouve = []
                for (depart, fleche, arrivee) in self.transitions:
                    if depart == etat and fleche == lettre and arrivee != "":
                        trouve.append(lettre)
                if lettre not in trouve : 
                    l.append(lettre)       
                    cpt += 1
            if l :
                print(f"L'état {etat} ne possède pas de transition avec la lettre {l}.")

        if cpt != 0:
            return False
        return True



    def standardiser(self):
        if self.est_standard():
            return self

        nouveau_init = 'i'
        nouveaux_etats = [nouveau_init] + self.etats
        nouvelles_transitions = list(self.transitions)

        for ancien_init in self.initial:
            for (dep, lettre, arr) in self.transitions:
                if dep == ancien_init:
                    t = (nouveau_init, lettre, arr)
                    if t not in nouvelles_transitions:
                        nouvelles_transitions.append(t)

        nouveaux_finaux = list(self.final)
        if any(e in self.final for e in self.initial):
            if nouveau_init not in nouveaux_finaux:
                nouveaux_finaux.append(nouveau_init)

        return Automate(self.alphabet, nouveaux_etats,
                        [nouveau_init], nouveaux_finaux, nouvelles_transitions)
 
    
    def Completion(self):
        """
        Retourne un automate déterministe complet en ajoutant un état
        poubelle 'P' si des transitions manquent.
        """
        if self.est_complet():
            return
        # on parcourt tous les etats et leurs transitions pour detecter si une transition manque ou est = ""
        nouv_transitions = []

        if '' in self.etats:
            self.etats.remove('')
            self.etats.append('P')

        for etat in self.etats:
            for lettre in self.alphabet:
                trouve = False
                for (depart, fleche, arrivee) in self.transitions:
                    nouv_depart = depart
                    nouv_arrivee = arrivee
                    if (depart == ""):
                        nouv_depart = "P"
                    if (arrivee == ""):
                        nouv_arrivee = "P"
                    if (depart == etat) and (fleche == lettre):
                        trouve = True
                        break
                if trouve:
                    nouv_transitions.append((nouv_depart, lettre, nouv_arrivee))
                else:
                    nouv_transitions.append((etat, lettre, "P"))  # si transi manquant pour un état, ajout transi direction Poubelle
                    if "P" not in self.etats:
                        self.etats.append("P")  # on ajoute l'etat poubelle p à la liste d'états
        for lettre in self.alphabet:
            if ("P", lettre, "P") not in nouv_transitions:
                nouv_transitions.append(("P", lettre, "P"))  # l'état poubelle a ses propres transitions vers lui meme pour chaque lettre

        self.transitions = nouv_transitions
        return

    def est_asynchrone(self):
        return "e" in self.alphabet


    def Determinisation_et_completion_asynchrone(self):
        """Déterminise un automate ASYNCHRONE et met à jour ses attributs. Renvoie l'automate ainsi que ses fermetures sous la forme d'un dico"""
        nouv_alphabet = [l for l in self.alphabet if l != 'e']
        nouv_etats = [self.etat_to_string(self.initial)]
        nouv_transitions = []
        nouv_initial = [self.etat_to_string(self.initial)]
        nouv_final = []

        groupes_fermeture_epsilon = self.Groupes_Fermeture_Epsilon(self.initial)

        etats_a_traiter = [self.initial] #on commence la deter avec états init
        etats_deja_traite = [list(self.initial)] #donc on considère états init comme déjà traités

        while etats_a_traiter:
            etat_present = etats_a_traiter.pop()  # On prend le 1er element et on le retire de la liste
            for lettre in nouv_alphabet:  # ["a", "b"] pour chaque lettre, calcul des etats atteignables

                # 1. recherche de toutes les dest depuis un état
                destinations = [] # represente les etats d'arrivés pour une lettre
                i = 0
                # ajout différents état arrivée dans destination
                for etat in etat_present:  # tous les états dans l'état présent (pour couvrir les états composés) [['2'], ['2', '3', '4', '5', '6']]
                    for sous_etat in self.Groupes_Fermeture_Epsilon([etat])[etat]: #dico des fermetures epsilone {'3': ['3', '2', '6']} --> ['3', '2', '6']
                        for (depart, fleche, arrivee) in self.transitions:
                            if depart == sous_etat and fleche == lettre and (arrivee not in destinations): #choisit la transition qui nous interesse
                                destinations.append(arrivee)
                                groupes_fermeture_epsilon = self.Fusion_dicos(groupes_fermeture_epsilon,self.Groupes_Fermeture_Epsilon(arrivee))
                    i += 1

                # 2. traitement des novueaux états trouvés
                destinations.sort()  # trier pour éviter différentes combi de même état composé
                for etat in destinations:
                    for sous_etat in self.Groupes_Fermeture_Epsilon(etat)[etat]: #dico des fermetures epsilone {'3': ['3', '2', '6']} --> ['3', '2', '6']
                        if sous_etat in self.final and self.etat_to_string(destinations) not in nouv_final:
                            nouv_final.append(self.etat_to_string(destinations))  # modif finals

                # 3. maj automate nouv_etats et nouv_transitions
                if self.etat_to_string(destinations) not in nouv_etats:
                    nouv_etats.append(self.etat_to_string(destinations))  # modif etats
                # print(etat_present, lettre, destinations)
                nouv_transitions.append(
                    (self.etat_to_string(etat_present), lettre, self.etat_to_string(destinations)))  # modif transi

                if destinations not in etats_deja_traite:  # si pas encore traité
                    etats_a_traiter.append(destinations)  # marquer état comme à traiter
                    etats_deja_traite.append(destinations)  # marquer état comme déjà traité

        # 4. remplacement par nouveaux etats + transitions
        self.alphabet = nouv_alphabet
        self.etats = nouv_etats
        self.transitions = nouv_transitions
        self.initial = nouv_initial
        self.final = nouv_final

        # 5 completion
        self.Completion()

        return self, groupes_fermeture_epsilon


    def Determinisation_et_completion_synchrone(self):
        """Déterminise un automate et mets à jour ses attributs. Renvoie l'automate"""
        nouv_etats= []
        nouv_transitions = []
        nouv_initial = [self.etat_to_string(self.initial)]
        nouv_final = []

        etats_a_traiter = [self.initial] #on commence la deter avec états init
        etats_deja_traite = [list(self.initial)] #donc on considère états init comme déjà traités

        while etats_a_traiter:
            etat_present = etats_a_traiter.pop()  # On prend le 1er element et on le retire de la liste
            for lettre in self.alphabet:  # ["a", "b"] pour chaque lettre, calcul des etats atteignables
                # 1. recherche de toutes les dest depuis un état
                destinations = []  # represente les etats d'arrivés pour une lettre
                # ajout différents état arrivée dans destination
                for etat in etat_present:  # tous les états dans l'état présent (pour couvrir les états composés) [['2'], ['2', '3', '4', '5', '6']]
                    for (depart, fleche, arrivee) in self.transitions:
                        if depart == etat and fleche == lettre and arrivee not in destinations:
                            destinations.append(arrivee)

                # 2. traitement des novueaux états trouvés
                destinations.sort()  # trier pour éviter différentes combi de même état composé
                for sous_etat in destinations:
                    if sous_etat in self.final and self.etat_to_string(destinations) not in nouv_final:
                        nouv_final.append(self.etat_to_string(destinations))  # modif finals

                # 3. maj automate nouv_etats et nouv_transitions
                if self.etat_to_string(destinations) not in nouv_etats:
                    nouv_etats.append(self.etat_to_string(destinations))  # modif etats
                # print(etat_present, lettre, destinations)
                nouv_transitions.append(
                    (self.etat_to_string(etat_present), lettre, self.etat_to_string(destinations)))  # modif transi

                if destinations not in etats_deja_traite:  # si pas encore traité
                    etats_a_traiter.append(destinations)  # marquer état comme à traiter
                    etats_deja_traite.append(destinations)  # marquer état comme déjà traité

        # 4. remplacement par nouveaux etats + transitions
        self.etats = nouv_etats
        self.transitions = nouv_transitions
        self.initial = nouv_initial
        self.final = nouv_final

        # 5 completion
        self.Completion()

        return self

    def Determinisation_et_completion(self):
        if self.est_asynchrone():
            automate, dico = self.Determinisation_et_completion_asynchrone()
            print(automate.Affichage())
            for item in sorted(dico.items()):
                print(f"{item[0]}' : {sorted(item[1])}")
        else:
            automate = self.Determinisation_et_completion_synchrone()
            print(automate.Affichage())
        return self



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

    def Fusion_dicos_minimisation(self, dico1: dict, dico2: dict):
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
        groupes_next = self.Fusion_dicos_minimisation(self.Diviseur_Etat(groupes_temp['I0'], groupes_temp),
                                         self.Diviseur_Etat(groupes_temp['I1'], groupes_temp))
        while groupes_temp != groupes_next:
            groupes_temp = groupes_next.copy()
            groupes_next = dict()
            for cle in groupes_temp.keys():
                groupes_next = self.Fusion_dicos_minimisation(groupes_next, self.Diviseur_Etat(groupes_temp[cle], groupes_temp))

        nouv_etat = list(groupes_next.keys())
        nouv_transi = []
        nouv_initial = []
        nouv_final = []
        print(self.transitions)
        print(groupes_next.keys())

        for cle in groupes_next.keys():   

            for sous_etat in groupes_next[cle]: #etat dans ['3.5', '3']
                if sous_etat in self.initial and sous_etat not in nouv_initial:
                    nouv_initial.append(cle) #Ajout nouveaux états init
                if sous_etat in self.final and sous_etat not in nouv_final:
                    nouv_final.append(cle) #Ajout nouveaux états finaux

                for transition in self.transitions:
                    for lettre in self.alphabet:
                        destinations_sous_etat = []
                        if (transition[0] == sous_etat) and (transition[1] == lettre) and transition[2] not in destinations_sous_etat:
                            destinations_sous_etat.append(transition[2])
                        for cle2 in groupes_next.keys():
                            for sous_etat2 in destinations_sous_etat:
                                if sous_etat2 in groupes_next[cle2] and (cle, lettre, cle2) not in nouv_transi:
                                    nouv_transi.append((cle, lettre, cle2))

        self.etats = nouv_etat
        self.transitions = nouv_transi
        self.initial = nouv_initial
        self.final = nouv_final
        print(self.transitions)

        return self, groupes_next

    def Affichage_Minimisation(self):
        automate, dico = self.Minimisation()
        print(automate.Affichage())
        for item in dico.items():
            print(f"{item[0]}' : {item[1]}")


    def lire_mot(self, mot):

        if not self.est_deterministe():
            print("Reconnaissance de mot impossible, veuillez déterminiser l'automate d'abord")
            return False
        
        etat_courant = self.initial[0]
        alphabet_sync = [l for l in self.alphabet if l != 'e']

        for symbole in mot:
            if symbole not in alphabet_sync:
                print(f"Symbole '{symbole}' n'appartient pas à l'alphabet {alphabet_sync} de l'automate.")
                return False
                
            dest = None
            for (dep, lettre, arr) in self.transitions:
                if etat_courant == dep and symbole == lettre:
                    dest = arr
                    break
            if dest is None:
                return False
            etat_courant = dest

        return etat_courant in self.final


    def automate_complementaire(self):
        """
        Retourne l'automate reconnaissant le langage complémentaire
        (échange états finaux / non-finaux).
        Nécessite un AFDC en entrée.
        """
        if not self.est_deterministe():
            print("Erreur : l'automate doit être déterministe et complet.")
            return None
        if not self.est_complet():
            print("Erreur : l'automate doit être complet.")
            return None
        nouveaux_finaux = [e for e in self.etats if e not in self.final]
        return Automate(self.alphabet, self.etats, self.initial,
                        nouveaux_finaux, self.transitions)


def lecture_automate(chemin):
    with open(chemin, 'r') as f:
        donnees = [ligne.strip() for ligne in f.readlines() if ligne.strip()]  # ignorer lignes vides

    nb_symboles = int(donnees[0]) # récupére le nombre de lettre
    nb_etats = int(donnees[1])
    etats_initiaux = donnees[2].split()[1:] # récupère les états initiaux à partir du rang 1 car le rang 0 représente le nombre de valeurs initiales
    etats_finaux = donnees[3].split()[1:]
    nb_transitions = int(donnees[4])

    transitions = []
    lettres = []
    for donnee in donnees[5: 5 + nb_transitions]:
        parts = donnee.split() # split() permet de retirer les espaces vides
        depart, lettre, arrivee = parts[0], parts[1], parts[2]
        transitions.append((depart, lettre, arrivee))
        if lettre not in lettres :
            lettres.append(lettre)

    etats = [str(i) for i in range(nb_etats)]

    return Automate(sorted(lettres), etats, etats_initiaux, etats_finaux, transitions)



def Ecriture_trace(chemin_automate: str, chemin_trace: str):
    """
    Lit un automate depuis chemin_automate, exécute toutes les opérations
    et écrit la trace dans chemin_trace (créé ou remplacé).
    """
    automate = lecture_automate(chemin_automate)

    with open(chemin_trace, 'w', encoding='utf-8') as f:

        f.write("=== AUTOMATE INITIAL ===\n")
        f.write(automate.Affichage() + "\n\n")

        f.write("=== STANDARDISATION ===\n")
        std = automate.standardiser()
        f.write(std.Affichage() + "\n\n")

        f.write("=== DETERMINISATION ET COMPLETION ===\n")
        det = lecture_automate(chemin_automate)  # on recharge pour repartir de zéro
        det.Determinisation_et_completion()
        f.write(det.Affichage() + "\n\n")

        f.write("=== MINIMISATION ===\n")
        min, groupes = det.Minimisation()
        f.write(min.Affichage() + "\n")
        for cle, etats in groupes.items():
            f.write(f"  {cle} : {etats}\n")
        f.write("\n")

        f.write("=== COMPLEMENTAIRE ===\n")
        comp = det.automate_complementaire()
        if comp:
            f.write(comp.Affichage() + "\n")

