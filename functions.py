from tabulate import tabulate


class Automate:

    def __init__(self, alphabet, etats, initial, final, transitions):
        self.alphabet    = sorted(alphabet)
        self.etats       = etats
        self.initial     = initial
        self.final       = final
        self.transitions = transitions

    def __str__(self):
        return (
            f"Alphabet    : {self.alphabet}\n"
            f"Etats       : {self.etats}\n"
            f"Initial(aux): {self.initial}\n"
            f"Final(aux)  : {self.final}\n"
            f"Transitions : {self.transitions}\n"
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
        fermeture  = list(etats)
        a_traiter  = list(etats)
        while a_traiter: #si encore des éléments dans la liste
            etat = a_traiter.pop(0)
            for (dep, lettre, arr) in transitions:
                if dep == etat and lettre == 'e' and arr not in fermeture:
                    fermeture.append(arr)
                    a_traiter.append(arr)
        return fermeture



    def Affichage(self):
        """Retourne une table de transitions formatée (str)."""
        alphabet_affiche = [l for l in self.alphabet if l != 'e']
        if 'e' in self.alphabet:
            alphabet_affiche.append('ε')

        donnee  = []
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
            for lettre in self.alphabet:
                lettre_cle = 'e' if lettre == 'ε' else lettre
                arrivees   = [str(t[2]) for t in self.transitions
                              if t[0] == etat and t[1] == lettre_cle]
                ligne.append(','.join(arrivees) if arrivees else '-')

            donnee.append(ligne)

        colonne = ['center'] * len(en_tete)
        return tabulate(donnee, en_tete, tablefmt='fancy_grid', colalign=colonne)


    def est_standard(self, verbose=True):
        if len(self.initial) != 1:
            if verbose:
                print(f"  Non standard : {len(self.initial)} état(s) initial/initiaux.")
            return False
        i = self.initial[0]
        for (dep, lettre, arr) in self.transitions:
            if arr == i:
                if verbose:
                    print(f"  Non standard : transition vers l'état initial "
                          f"depuis '{dep}' avec '{lettre}'.")
                return False
        if verbose:
            print("  L'automate est standard.")
        return True

    def est_deterministe(self, verbose=True):
        if len(self.initial) != 1:
            if verbose:
                print(f"  Non déterministe : {len(self.initial)} état(s) initial/initiaux.")
            return False
        if 'e' in self.alphabet:
            if verbose:
                print("  Non déterministe : présence de ε-transitions (automate asynchrone).")
            return False
        vus = {}
        for (dep, lettre, arr) in self.transitions:
            cle = (dep, lettre)
            if cle in vus:
                if verbose:
                    print(f"  Non déterministe : plusieurs transitions depuis "
                          f"'{dep}' par '{lettre}'.")
                return False
            vus[cle] = True
        if verbose:
            print("  L'automate est déterministe.")
        return True

    def est_complet(self, verbose=True):
        alphabet_sync = [l for l in self.alphabet if l != 'e']
        for e in self.etats:
            for l in alphabet_sync:
                if not any(t[0] == e and t[1] == l for t in self.transitions):
                    if verbose:
                        print(f"  Non complet : pas de transition depuis '{e}' avec '{l}'.")
                    return False
        if verbose:
            print("  L'automate est complet.")
        return True

    def standardiser(self):
        if self.est_standard(verbose=False):
            return self

        nouveau_init         = 'i'
        nouveaux_etats       = [nouveau_init] + self.etats
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
        if self.est_complet(verbose=False):
            return self

        poubelle         = 'P'
        nouv_etats       = list(self.etats)
        nouv_transitions = list(self.transitions)
        poubelle_ajoutee = False
        alphabet_sync    = [l for l in self.alphabet if l != 'e']

        for etat in self.etats:
            for lettre in alphabet_sync:
                if not any(t[0] == etat and t[1] == lettre
                           for t in nouv_transitions):
                    if not poubelle_ajoutee:
                        # Ajouter l'état poubelle et ses auto-boucles
                        nouv_etats.append(poubelle)
                        for l in alphabet_sync:
                            nouv_transitions.append((poubelle, l, poubelle))
                        poubelle_ajoutee = True
                    nouv_transitions.append((etat, lettre, poubelle))

        return Automate(self.alphabet, nouv_etats, self.initial,
                        self.final, nouv_transitions)


        if self.est_deterministe(verbose=False):
            if self.est_complet(verbose=False):
                print("  L'automate est déjà déterministe et complet.")
                return self
            else:
                print("  L'automate est déterministe mais incomplet → complétion.")
                return self.Completion()

        transitions_orig = self.transitions          # on ne modifie pas self
        alphabet_sync    = [l for l in self.alphabet if l != 'e']

        etat_initial  = tuple(sorted(
            self.fermeture_epsilon(self.initial, transitions_orig), key=str))
        a_traiter     = [etat_initial]
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

    def Affichage_AFDC(self, titre="Automate Déterministe Complet"):
        """Affiche la table de transitions et la table de correspondance."""
        print(f"\n--- {titre} ---")

        # Construire le dictionnaire nom_etats : état → chaîne affichable
        nom_etats = {}
        for etat in self.etats:
            cle = tuple(etat) if isinstance(etat, list) else etat
            nom_etats[cle] = self.etat_to_string(etat)

        alphabet_sync = [l for l in self.alphabet if l != 'e']
        en_tete       = [' ', 'État'] + alphabet_sync
        donnees       = []

        for etat in self.etats:
            cle     = tuple(etat) if isinstance(etat, list) else etat
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
        print("\n  Table de correspondance des états :")
        print("  " + "-" * 38)
        for etat in self.etats:
            cle     = tuple(etat) if isinstance(etat, list) else etat
            nom_str = nom_etats[cle]
            if isinstance(etat, (list, tuple)):
                if len(etat) == 0:
                    anciens = 'ø (poubelle)'
                else:
                    anciens = ', '.join(str(e) for e in etat)
                print(f"  {nom_str:12s} ← {{{anciens}}}")
            else:
                print(f"  {nom_str:12s} ← {etat}")

    def Appartenance_groupe(self, destination, groupes):
        for cle, membres in groupes.items():
            if destination in membres:
                return cle
        return '∅'   # destination inconnue (état poubelle non nommé)

    def Diviseur_Etat(self, etats, groupes):
        groupes_temp  = {}
        alphabet_sync = [l for l in self.alphabet if l != 'e']
        for etat in etats:
            chaine = ''
            for lettre in alphabet_sync:
                dest = None
                for (dep, l, arr) in self.transitions:
                    if dep == etat and l == lettre:
                        dest = arr
                        break
                chaine += str(self.Appartenance_groupe(dest, groupes)
                              if dest is not None else '∅')
            if chaine in groupes_temp:
                groupes_temp[chaine].append(etat)
            else:
                groupes_temp[chaine] = [etat]
        return groupes_temp

    def Fusion_dicos(self, dico1, dico2):
        res    = {}
        offset = 0
        for v in dico1.values():
            res[f'I{offset}'] = list(v)
            offset += 1
        for v in dico2.values():
            res[f'I{offset}'] = list(v)
            offset += 1
        return res

    def Minimisation(self):
        terminaux     = list(self.final)
        non_terminaux = [x for x in self.etats if x not in terminaux]

        # Partition initiale P0 : on ignore les groupes vides
        groupes_temp = {}
        if terminaux:
            groupes_temp['I0'] = terminaux
        if non_terminaux:
            groupes_temp[f'I{len(groupes_temp)}'] = non_terminaux

        iteration = 0
        print(f"\n  P{iteration} : {groupes_temp}")

        while True:
            groupes_next = {}
            for cle, membres in groupes_temp.items():
                sous = self.Diviseur_Etat(membres, groupes_temp)
                groupes_next = self.Fusion_dicos(groupes_next, sous)

            iteration += 1
            print(f"  P{iteration} : {groupes_next}")

            # Convergence si les listes de groupes sont identiques (à renommage près)
            if (sorted(str(v) for v in groupes_temp.values()) ==
                    sorted(str(v) for v in groupes_next.values())):
                break
            groupes_temp = groupes_next

        return groupes_next

    def Affichage_Minimisation(self):
        print("\n--- Calcul des partitions de minimisation ---")
        groupes = self.Minimisation()

        if len(groupes) == len(self.etats):
            print("\n  L'automate est déjà minimal (aucun état fusionné).")
        else:
            print(f"\n  {len(self.etats)} états → {len(groupes)} états après minimisation.")

        # Représentant de chaque groupe (premier élément)
        repr_groupe = {cle: membres[0] for cle, membres in groupes.items()}

        def groupe_de(etat):
            for cle, membres in groupes.items():
                if etat in membres:
                    return cle
            return None

        nouveaux_etats = list(groupes.keys())
        nouv_initial = [groupe_de(self.initial[0])]
        nouv_final = [cle for cle, membres in groupes.items()
                             if any(m in self.final for m in membres)]
        nouv_transitions = []
        alphabet_sync = [l for l in self.alphabet if l != 'e']

        for cle, membres in groupes.items():
            rep = repr_groupe[cle]
            for lettre in alphabet_sync:
                dest = None
                for (dep, l, arr) in self.transitions:
                    if dep == rep and l == lettre:
                        dest = arr
                        break
                if dest is not None:
                    dest_groupe = groupe_de(dest)
                    t = (cle, lettre, dest_groupe)
                    if t not in nouv_transitions:
                        nouv_transitions.append(t)

        AFDCM = Automate(self.alphabet, nouveaux_etats,
                         nouv_initial, nouv_final, nouv_transitions)

        print("\n  Automate minimal (AFDCM) :")
        print(AFDCM.Affichage())

        print("\n  Table de correspondance AFDCM ← AFDC :")
        print("  " + "-" * 40)
        for cle, membres in groupes.items():
            print(f"  {cle:6s}  ←  {{{', '.join(str(m) for m in membres)}}}")

        return AFDCM


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
            print("  Erreur : l'automate doit être déterministe et complet.")
            return None
        if not self.est_complet(verbose=False):
            print("  Erreur : l'automate doit être complet.")
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
        lettres.append('e')

    etats = [str(i) for i in range(nb_etats)]

    return Automate(lettres, etats, etats_initiaux, etats_finaux, transitions)