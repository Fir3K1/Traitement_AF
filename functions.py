from pytmx.pytmx import prop_type
from tabulate import tabulate


class Automate:

    def __init__(self, alphabet, etats, initial, final, transitions):
        self.alphabet = sorted(alphabet)
        self.etats = etats
        self.initial = initial
        self.final = final
        self.transitions = transitions

    def __str__(self):
        return (
            f"Alphabet    : {self.alphabet}\n"
            f"Etats       : {self.etats}\n"
            f"Alphabet: {self.alphabet}\n"
            f"Etats: {self.etats}\n"
            f"Initial(aux): {self.initial}\n"
            f"Final(aux)  : {self.final}\n"
            f"Transitions : {self.transitions}\n"
            f"Final(s): {self.final}\n"
            f"Transitions: {self.transitions}\n"
        )

    def etat_to_string(self, etat):
        """
        Convertit un état (str, liste ou tuple) en chaîne lisible.
        Tuple/liste vide  → 'P'  (état poubelle issu de la déterminisation)
        String            → inchangée
        Tuple/liste ['1','2','3'] → '123'  (si tous les sous-états font 1 char)
                                 → '1.2.3' (sinon, pour éviter l'ambiguïté)
        """
        # Tuple/liste vide = état poubelle créé par la déterminisation
        if isinstance(etat, (list, tuple)) and len(etat) == 0:
            return 'P'
        if isinstance(etat, str):
            return etat
        parts = [str(e) for e in etat]
        if all(len(p) == 1 for p in parts):
            return ''.join(parts)
        return '.'.join(parts)



    def fermeture_epsilon(self, etats, transitions=None):
        """Retourne tous les états atteignables par ε depuis `etats`."""
        if transitions is None:
            transitions = self.transitions
        fermeture = list(etats)
        a_traiter = list(etats)
        while a_traiter: #si encore des éléments dans la liste
            etat = a_traiter.pop(0)
            for (dep, lettre, arr) in transitions:
                if dep == etat and lettre == 'e' and arr not in fermeture:
                    fermeture.append(arr)
                    a_traiter.append(arr)
        return fermeture
        """ Convertit état (liste) en str."""
        return ".".join(str(e) for e in etat)

    #fonction récursive
    def Fermeture_epsilon(self, etats: list):
        """Retourne tous les états atteignables par ε depuis les états dans la liste (longueur 1 si un seul état)"""
        if etats == []: #condition d'arrêt
            return []
        accessibles = []
        for etat in etats:
            for (depart, lettre, arrivee) in self.transitions:
                if depart == etat and lettre == 'e' and (arrivee not in accessibles): #condition initiale
                    accessibles.append(arrivee)
        return accessibles + self.Fermeture_epsilon(accessibles) #etats accessibles déjà trouvés + ceux qu'on va trouver


    def Groupes_Fermeture_Epsilon(self, etats: list):
        """Prend une liste d'états en paramètre et renvoie un dico avec chaque état en clé et leurs fermetures ε"""
        res = dict()
        for etat in etats:
            res[etat+"'"] = [etat] + self.Fermeture_epsilon(etats)
        return res


    def Affichage(self):
        """Retourne une table de transitions formatée (str)."""
        alphabet_affiche = [l for l in self.alphabet if l != 'e']

        donnee = []
        en_tete = [' ', 'etats'] + alphabet_affiche

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
            for lettre in alphabet_affiche:
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


    def est_complet(self, verbose=True):
        alphabet_sync = [l for l in self.alphabet if l != 'e']
        cpt = 0
        for e in self.etats:
            for l in alphabet_sync:
                if not any(t[0] == e and t[1] == l for t in self.transitions):
                    print(f"Non complet : pas de transition depuis '{e}' avec '{l}'.")
                    cpt += 1
        if cpt != 0:
            return False

        print("L'automate est complet.")
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
 #


    def Completion(self):
        """
        Retourne un automate déterministe complet en ajoutant un état
        poubelle 'P' si des transitions manquent.
        """
        if self.est_complet():
            return self

        poubelle = 'P'
        nouv_etats = list(self.etats)
        nouv_transitions = list(self.transitions)
        poubelle_ajoutee = False
        alphabet_sync = [l for l in self.alphabet if l != 'e']

        for etat in self.etats:
            for lettre in alphabet_sync:
                if not any(t[0] == etat and t[1] == lettre for t in nouv_transitions):
                    if not poubelle_ajoutee:
                        # Ajouter l'état poubelle et ses auto-boucles
                        nouv_etats.append(poubelle)
                        for l in alphabet_sync:
                            nouv_transitions.append((poubelle, l, poubelle))
                        poubelle_ajoutee = True
                    nouv_transitions.append((etat, lettre, poubelle))

        return Automate(self.alphabet, nouv_etats, self.initial,
                        self.final, nouv_transitions)

    def determinisation_et_completion(self):
        if self.est_deterministe(verbose=False):
            if self.est_complet(verbose=False):
                print("L'automate est déjà déterministe et complet.")
                return self
            else:
                print("L'automate est déterministe mais incomplet → complétion.")
                return self.Completion()

        transitions_orig = self.transitions          # on ne modifie pas self
        alphabet_sync = [l for l in self.alphabet if l != 'e']
    def est_asynchrone(self):
        return "e" in [transi[1] for transi in self.transitions]

        etat_initial = tuple(sorted(
            self.fermeture_epsilon(self.initial, transitions_orig), key=str))
        a_traiter = [etat_initial]
        nouveaux_etats = [etat_initial]
        nouv_transitions = []

        while a_traiter:
            etat = a_traiter.pop(0)
            for lettre in alphabet_sync:
                # Calcul des états atteignables
                cible = []
                for sous_etat in etat:
                    for (dep, l, arr) in transitions_orig:
                        if dep == sous_etat and l == lettre and arr not in cible:
                            cible.append(arr)
                # Fermeture-ε de la cible
                cible = self.fermeture_epsilon(cible, transitions_orig)
                cible = tuple(sorted(cible, key=str))

                nouv_transitions.append((etat, lettre, cible))
                if cible not in nouveaux_etats:
                    nouveaux_etats.append(cible)
                    a_traiter.append(cible)

        # États finaux : tout sous-ensemble contenant un état final original
        nouv_etats_finaux = [m for m in nouveaux_etats
                             if any(f in m for f in self.final)]

        AFDC = Automate(self.alphabet, nouveaux_etats,
                        [etat_initial], nouv_etats_finaux, nouv_transitions)

        # Complétion si nécessaire (le tuple vide () remplace la poubelle)
        if not AFDC.est_complet(verbose=False):
            AFDC = AFDC.Completion()

        return AFDC
    def Determinisation_et_completion(self):
        """Déterminise un automate et mets à jour ses attributs. Renvoie l'automate"""
        nouv_etats= []
        nouv_transitions = []
        nouv_initial = [self.etat_to_string(self.initial)]
        nouv_final = []

        etats_a_traiter = [self.initial] #on commence la deter avec états init
        etats_deja_traite = [list(self.initial)] #donc on considère états init comme déjà traités

        while etats_a_traiter:
            if self.est_asynchrone():
                pass
            else :
                pass
            etat_present = etats_a_traiter.pop()  # On prend le 1er element et on le retire de la liste
            for lettre in self.alphabet:  #["a", "b"] pour chaque lettre, calcul des etats atteignables
                #1. recherche de toutes les dest depuis un état
                destinations = []  # represente les etats d'arrivés pour une lettre
                for etat in etat_present:  # tous les états dans l'état présent (pour couvrir les états composés)
                    for (depart, fleche, arrivee) in self.transitions:
                        if depart == etat and fleche == lettre and arrivee not in destinations:
                            destinations.append(arrivee)  # ajoute dans liste etats atteignables pour chaque lettre, chaque etat

                #2. traitement des novueaux états trouvés
                destinations.sort() #trier pour éviter différentes combi de même état composé
                for sous_etat in destinations:
                    if sous_etat in self.final and self.etat_to_string(destinations) not in nouv_final:
                        nouv_final.append(self.etat_to_string(destinations)) #modif finals

                #3. maj automate nouv_etats et nouv_transitions
                if self.etat_to_string(destinations) not in nouv_etats:
                    nouv_etats.append(self.etat_to_string(destinations)) #modif etats
                nouv_transitions.append((self.etat_to_string(etat_present), lettre, self.etat_to_string(destinations))) #modif transi

                if destinations not in etats_deja_traite: #si pas encore traité
                    etats_a_traiter.append(destinations) #marquer état comme à traiter
                    etats_deja_traite.append(destinations) #marquer état comme déjà traité

        #4. remplacement par nouveaux etats + transitions
        self.etats = nouv_etats
        self.transitions = nouv_transitions
        self.initial = nouv_initial
        self.final = nouv_final

        #5 completion
        self.Completion()

    def Affichage_AFDC(self, titre="Automate Déterministe Complet"):
        """Affiche la table de transitions et la table de correspondance."""
        print(f"\n--- {titre} ---")

        # Construire le dictionnaire nom_etats : état → chaîne affichable
        nom_etats = {}
        for etat in self.etats:
            cle = tuple(etat) if isinstance(etat, list) else etat
            nom_etats[cle] = self.etat_to_string(etat)

        alphabet_sync = [l for l in self.alphabet if l != 'e']
        en_tete = [' ', 'État'] + alphabet_sync
        donnees = []

        for etat in self.etats:
            cle = tuple(etat) if isinstance(etat, list) else etat
            nom_str = nom_etats[cle]

            if etat in self.initial and etat in self.final:
                marqueur = 'ES'
            elif etat in self.initial:
                marqueur = 'E'
            elif etat in self.final:
                marqueur = 'S'
            else:
                marqueur = ''

            ligne = [marqueur, nom_str]
            for lettre in alphabet_sync:
                dest = [t[2] for t in self.transitions
                        if t[0] == etat and t[1] == lettre]
                if dest:
                    noms_dest = []
                    for d in dest:
                        cle_d = tuple(d) if isinstance(d, list) else d
                        noms_dest.append(
                            nom_etats.get(cle_d, self.etat_to_string(d)))
                    ligne.append(','.join(noms_dest))
                else:
                    ligne.append('-')
            donnees.append(ligne)

        colalign = ['center'] * len(en_tete)
        print(tabulate(donnees, en_tete,
                       tablefmt='fancy_grid', colalign=colalign))

        # Table de correspondance
        print("\nTable de correspondance des états :")
        print("  " + "-" * 38)
        for etat in self.etats:
            cle = tuple(etat) if isinstance(etat, list) else etat
            nom_str = nom_etats[cle]
            if isinstance(etat, (list, tuple)):
                if len(etat) == 0:
                    anciens = 'ø (poubelle)'
                else:
                    anciens = ', '.join(str(e) for e in etat)
                print(f"{nom_str:12s} ← {{{anciens}}}")
            else:
                print(f"{nom_str:12s} ← {etat}")

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

    def Fusion_dicos(self, dico1, dico2):
        res = {}
        offset = 0
        for v in dico1.values():
            res[f'I{offset}'] = list(v)
            offset += 1
        for v in dico2.values():
            res[f'I{offset}'] = list(v)
            offset += 1
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
        etat_courant = self.initial[0]
        alphabet_sync = [l for l in self.alphabet if l != 'e']

        for symbole in mot:
            if symbole not in alphabet_sync:
                print(f"  Symbole '{symbole}' hors alphabet {alphabet_sync}.")
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
        if not self.est_deterministe(verbose=False):
            print("Erreur : l'automate doit être déterministe et complet.")
            return None
        if not self.est_complet(verbose=False):
            print("Erreur : l'automate doit être complet.")
            return None
        nouveaux_finaux = [e for e in self.etats if e not in self.final]
        return Automate(self.alphabet, self.etats, self.initial,
                        nouveaux_finaux, self.transitions)


def lecture_automate(chemin):
    with open(chemin, 'r') as f:
        donnees = [ligne.strip() for ligne in f.readlines()
                   if ligne.strip()]        # ignorer lignes vides

    nb_symboles = int(donnees[0])
    nb_etats = int(donnees[1])
    etats_initiaux = donnees[2].split()[1:]
    etats_finaux = donnees[3].split()[1:]
    nb_transitions = int(donnees[4])

    transitions = []
    for donnee in donnees[5: 5 + nb_transitions]:
        parts = donnee.split()
        depart, lettre, arrivee = parts[0], parts[1], parts[2]
        transitions.append((depart, lettre, arrivee))

    # Alphabet : 'a', 'b', … selon nb_symboles
    # On ajoute 'e' seulement si des ε-transitions existent dans le fichier
    lettres = [chr(ord('a') + i) for i in range(nb_symboles)]
    if any(t[1] == 'e' for t in transitions) and 'e' not in lettres:
        lettres[len(lettres)-1] = ('e')

    etats = [str(i) for i in range(nb_etats)]

    return Automate(lettres, etats, etats_initiaux, etats_finaux, transitions)    return Automate(lettres, etats, etats_initiaux, etats_finaux, transitions)


"""  
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

"""


test = Automate(alphabet = ['a', 'b'],
                initial = ["0", "2"],
                final = ["3"],
                etats = ['0', '1', '2', '3'],
                transitions = [("0", "a", "0"), ("0", "b", "2"),
                               ("1", "a", "1"), ("1", "b", "1"),
                               ("2", "a", "2"), ("2", "b", "3"),
                               ("3", "a", "1"), ("3", "b", "2")]
)




#automate 34
test2 = Automate(alphabet = ['a', 'b', 'e'],
                initial = ["0"],
                final = ["6"],
                etats = ["0", "1", "2", "3", "4", "5", "6"],
                transitions = [("0", "e", "1"), ("0", "e", "4"), 
                               ("1", "e", "2"), ("1", "a", "2"),
                               ("2", "b", "3"), 
                               ("3", "e", "2"), ("3", "e", "6"),
                               ("4", "b", "5"),
                               ("5", "e", "4"), ("5", "e", "6")]
)



"""
test = Automate(alphabet = ['a', 'b', 'e'],
                initial = ["0"],
                final = ["6"],
                etats = ["0", "1", "2", "3", "4", "5", "6"],
                transitions = [("0", "e", "1"), ("0", "e", "4"), 
                               ("1", "e", "2"), ("1", "a", "2"),
                               ("2", "b", "3"), 
                               ("3", "e", "2"), ("3", "e", "6"),
                               ("4", "b", "5"),
                               ("5", "e", "4"), ("5", "e", "6")]
)
"""

test.Determinisation_et_completion()
print(test)

