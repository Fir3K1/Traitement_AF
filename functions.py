from functions import *

def affichage (path):
    with open(path, mode="r", encoding="utf-8") as automate:
        contenu = automate.read()
        return contenu