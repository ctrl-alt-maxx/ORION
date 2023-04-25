# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd
import math
import random
import ast
import string

from id import *
from helper import Helper as hlp

cadreActuel = None

class Porte_de_vers(): #Porte dans laquelle on rentre dans le trou de ver
    def __init__(self, parent, x, y, couleur, taille):
        self.parent = parent
        self.id = get_prochain_id()
        self.x = x
        self.y = y
        self.pulsemax = taille
        self.pulse = random.randrange(self.pulsemax)
        self.couleur = couleur

    def jouer_prochain_coup(self): #Affichage
        self.pulse += 1
        if self.pulse >= self.pulsemax:
            self.pulse = 0


class Trou_de_vers(): #Chemin jusqu'à l'autre porte de vers
    def __init__(self, x1, y1, x2, y2):
        self.id = get_prochain_id()
        taille = random.randrange(6, 20)
        self.porte_a = Porte_de_vers(self, x1, y1, "red", taille)
        self.porte_b = Porte_de_vers(self, x2, y2, "orange", taille)
        self.liste_transit = []  # pour mettre les vaisseaux qui ne sont plus dans l'espace mais maintenant l'hyper-espace

    def jouer_prochain_coup(self):
        self.porte_a.jouer_prochain_coup() #Exécute affichage des portes
        self.porte_b.jouer_prochain_coup()

class Ressources():
    def __init__(self, type, rarete):
        self.type = type
        self.rarete = rarete
        self.tempsExtraction = rarete * rarete * 5

class Etoile():
    def __init__(self, parent, x, y, nomEtoile, ressources):

        self.id = get_prochain_id()
        self.parent = parent
        #self.proprietaire = ""
        self.x = x
        self.y = y
        self.taille = random.randrange(4, 8)
        self.nomEtoile = nomEtoile
        self.ressource = ressources ## ressources = {} ressources
        self.proprietaire = "neutre" #proprietaire = etoile owner
        self.installations = {"entrepot": None,
                              "usine": None} #installation = [] des installations du joueur
        self.en_construction = {"entrepot": None,
                              "usine": None} # installations en construction
        self.vaisseaux = None # [] de vaisseaux pose sur letoile
        self.estEclaire = False #etoile selectionne ou pas True ou False = False au debut du jeu
        self.niveauEtoile = 1 #niveau de l'étoile = 1/2/3 = toutes les étoiles seront de niveau 1 au debut du jeu
        self.inventaire ={"Fer":100,
                          "Cuivre":35,
                          "Or":5,
                          "Titane":0,
                          "Hydrogene":30,
                          "Plutonium":0,
                          "Antimatiere":0}

        self.vie = 500 # nbr de vie de la planete
        self.key_en_construction = None
        self.cout = self.cout_selon_niveau()

    # Amélioration de l'étoile

    '''
    Fonction définit les ressources nécessaires pour l'amélioration de l'étoile vers le prochain niveau
    Args:
    
    '''
    def cout_selon_niveau(self):
        if self.niveauEtoile == 1:
            self.cout = {  "Fer": 1000,
                            "Cuivre": 750,
                            "Or" : 500,
                            "Titane": 250,
                            "Hydrogene": 200,
                            "Plutonium": 100,
                            "Antimatiere": 0}

        elif self.niveauEtoile == 2:
            self.cout = {   "Fer": 2000,
                            "Cuivre": 2500,
                            "Or": 1000,
                            "Titane": 500,
                            "Hydrogene": 400,
                            "Plutonium": 200,
                            "Antimatiere": 50}

    '''
        Fonction vérifie si l'amélioration de l'étoile est possible et valide
        Args:

    '''
    def is_amelioration_possible(self):
        if self.isRessourcesValides(self):
            if self.niveauEtoile != 3:
                return True
        return False

    '''
        Fonction exécute l'amélioration de l'étoile et augmente son niveau
        Args:

    '''
    def ameliorer_etoile(self):
        key_ressources = self.inventaire.keys()
        if self.is_amelioration_possible():
            for i in key_ressources:
                self.inventaire.update({i:self.inventaire.get(i) - self.cout.get(i)})
            self.niveauEtoile += 1
            self.cout_selon_niveau()
            print("L'étoile ", self.nomEtoile, " a été amélioré. Elle est maintenant au niveau ", self.niveauEtoile, ".")


    # Construction des installations

    '''
    Fonction permet de construire ou d'améliorer une installation, elle retire les ressources utilisées et update les installations de l'étoile
    Args:
        installation est un objet Installation représentant l'installation à construire
    '''
    def creer_installation(self, type, cadre):
        if type == "entrepot":
            installation = Entrepot(self.parent,self.proprietaire,"entrepot", cadre)
        else:
            installation = Usine(self.parent, self.proprietaire, "usine", 25, cadre)
        if self.is_construisible(installation):
            #TODO POSSIBILITÉ DE CHANGER LA FONCTION EN BOUCLE
            self.inventaire.update({"Fer":          self.inventaire.get("Fer") - installation.cout.get("Fer")})
            self.inventaire.update({"Cuivre":       self.inventaire.get("Cuivre") - installation.cout.get("Cuivre")})
            self.inventaire.update({"Or":           self.inventaire.get("Or") - installation.cout.get("Or")})
            self.inventaire.update({"Titane":       self.inventaire.get("Titane") - installation.cout.get("Titane")})
            self.inventaire.update({"Hydrogene":    self.inventaire.get("Hydrogene") - installation.cout.get("Hydrogene")})
            self.inventaire.update({"Plutonium":    self.inventaire.get("Plutonium") - installation.cout.get("Plutonium")})
            self.inventaire.update({"Antimatiere":  self.inventaire.get("Antimatiere") - installation.cout.get("Antimatiere")})
            self.en_construction.update({installation.type:installation})
            print(self.en_construction)

    '''
    Permet de déterminer si l'étoile possède les ressources suffisantes pour construire ou améliorer l'installation voulue.
    Args:
        installation est un objet Installation représentant l'installation à construire
    Return true si la construction est possible, false si l'étoile ne possède pas les ressources suffisantes
    '''
    def is_construisible(self, installation):
        if self.isRessourcesValides(installation):
            if self.installations.get(installation.type) is None:
                return True
        return False

    '''
    Permet de déterminer si l'étoile possède toute les ressources nécéssaire à la construction de l'installation
    Args:
        installation est un objet Installation représentant l'installation à construire
    Returns true si l'étoile possède toutes les ressources nécéssaires, false si l'étoile ne possède pas toutes les ressources nécéssaires
    '''
    def isRessourcesValides(self, installation):
        listeRessources = self.inventaire.keys()
        for i in listeRessources:
            if self.inventaire.get(i) < installation.cout.get(i):
                return False
        return True

    def verifier_fin_construction(self, cadre):
        self.key_en_construction = self.en_construction.keys()

        for k in self.key_en_construction:
            if self.en_construction.get(k) is not None:
                if k =="entrepot":
                    self.verifier_fin_construction_selon_installation(cadre, k, 100) # Temps à changer
                else:
                    self.verifier_fin_construction_selon_installation(cadre, k, 200) # Temps à changer


    def verifier_fin_construction_selon_installation(self, cadre, k, temps_construction):
        if cadre == self.en_construction.get(k).cadre_debut_construction + temps_construction:  # Temps à modifier
            i = self.en_construction.get(k)
            print("La construction de ", i, "est terminé.")
            self.fin_construction_installation(i)
            self.en_construction.update({k: None})

    def fin_construction_installation(self, installation):
        self.installations.update({installation.type:installation})

    # Production des ressources

    '''
    Permet de produire dans chaque usine les ressources de l'étoile. La fonction est appelée à chaque tick.
    Args:
        tick est le cadre de jeu, permet de moduler la vitese de production
    '''
    def production(self, tick):
        if self.installations.get("usine") is not None:
            usine = self.installations.get("usine")
            #représente le tableau du nombre de chaque ressource qui serait produite à chaque tick de production
            valeursRessources = {"Fer": 5,
                                 "Cuivre": 4,
                                 "Or": 3,
                                 "Titane": 2,
                                 "Hydrogene": 6,
                                 "Plutonium": 3,
                                 "Antimatiere": 1}

            #Récupère la liste des ressources disponibles sur l'étoile
            keys = self.ressource.keys()
            generation = []
            for k in keys:
                if self.ressource.get(k) != 0:
                    generation.append(k)

            #Effectue la production des ressources
            for k in generation:
                if tick % 75 == 0:
                    qt = valeursRessources.get(k) * (usine.niveau + 1)
                    newValeur = self.inventaire.get(k) + qt;
                    self.inventaire.update({k:newValeur})

class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Deplacement():
    def __init__(self, positionOrigine, positionDestination):
        self.positionOrigine = positionOrigine
        self.positionDestination = positionDestination


class Vaisseau():
    def __init__(self, parent, nom, x, y, estAccoste, tempsConstruction, cadreDebutConstruction, type_vaisseau):
        self.parent = parent
        self.id = get_prochain_id()
        self.proprietaire = nom
        self.niveau_Vaisseau = 1
        self.tempsConstruction = tempsConstruction
        self.estAccoste = estAccoste #Étoile sur laquelle le vaisseau est accosté
        self.Deplacement = None
        self.cadreDebutConstruction = cadreDebutConstruction
        self.type_vaisseau = type_vaisseau


        #HP du vaiseau
        self.vie = 100

        #Image du vaisseau
        self.x = x
        self.y = y
        self.espace_cargo = 0
        self.energie = 100
        self.taille = 5
        self.vitesse = 2
        self.cible = 0
        self.type_cible = None                              # Type de cible (Étoile ou porte de ver)
        self.angle_cible = 0                                # Angle de direction
        self.arriver = {"Etoile": self.arriver_etoile,      # Action à exécuter selon le type de cible(Étoile ou porte de vers)
                        "Porte_de_vers": self.arriver_porte}

    def jouer_prochain_coup(self, trouver_nouveau=0):
        if self.cible != 0:                                     #S'il y a une cible qui a été choisie (donc cliquée)
            return self.avancer()
        elif trouver_nouveau:                                   #Déplacement AI
            cible = random.choice(self.parent.parent.etoiles)
            self.acquerir_cible(cible, "Etoile")

    def acquerir_cible(self, cible, type_cible):                #Utilisé seulement par l'AI
        self.type_cible = type_cible
        self.cible = cible
        self.angle_cible = hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)

    def avancer(self):                                  #Permet le déplacement d'un vaisseau
        if self.cible != 0:
            x = self.cible.x + random.randint(-15,15) # Distance de l'étoile à l'arrivée
            y = self.cible.y + random.randint(-15,15)

            self.estAccoste = False #quand le vaisseau se deplace estAccoste = False
            #recuperer estAccoste ici pour l<avoir ligne.408
            self.x, self.y = hlp.getAngledPoint(self.angle_cible, self.vitesse, self.x, self.y)
            if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse + 15:
                type_obj = type(self.cible).__name__                        #Trouver le type de la cible (Étoile, Porte de vers)
                rep = self.arriver[type_obj]()                              #Lancer l'action à faire selon le type de cible (arriver_etoile ou arriver_porte)
                return rep

    def arriver_etoile(self):   #Fonction pour prendre possession d'une étoile
        #self.parent.log.append(                                                                                            journal de débogagge (inutile)
            #["Arrive:", self.parent.parent.cadre_courant, "Etoile", self.id, self.cible.id, self.cible.proprietaire])
        if not self.cible.proprietaire:
            self.cible.proprietaire = self.proprietaire     #Associer un nouveau propriétaire
        cible = self.cible
        self.cible = 0
        return ["Etoile", cible]

    def arriver_porte(self): #Fonction pour aller dans un trou de vers
        #self.parent.log.append(["Arrive:", self.parent.parent.cadre_courant, "Porte", self.id, self.cible.id, ])           journal de débogage (inutile)
        cible = self.cible
        trou = cible.parent
        if cible == trou.porte_a:
            self.x = trou.porte_b.x + random.randrange(6) + 2
            self.y = trou.porte_b.y
        elif cible == trou.porte_b:
            self.x = trou.porte_a.x - random.randrange(6) + 2
            self.y = trou.porte_a.y
        self.cible = 0
        return ["Porte_de_ver", cible]

    def upgrade_vaisseau(self):
        self.vitesse += 1

        if(self.type_Vaisseau == "Cargo"):
            self.espace_cargo += 500
        elif(self.type_Vaisseau == "Vaisseau"):
            self.vie += 250


class Cargo(Vaisseau):  #TODO À CHANGER
    def __init__(self, parent, nom, x, y, estAccoste, tempsConstruction, cadreDebutConstruction, type_vaisseau):
        Vaisseau.__init__(self, parent, nom, x, y, estAccoste, tempsConstruction, cadreDebutConstruction, type_vaisseau)
        self.capaciteMax = 1000
        self.capaciteUtilise = 0
        self.inventaire = {"Fer":0,
                          "Cuivre":0,
                          "Or":0,
                          "Titane":0,
                          "Hydrogene":0,
                          "Plutonium":0,
                          "Antimatiere":0}
        self.energie = 500
        self.taille = 6
        self.vitesse = 1
        self.cible = 0
        self.ang = 0

    '''
        Fonction effectue le transfert automatique de toutes les ressources du cargo pour les entreposer à l'étoile accosté.
        Args:
        
    '''
    # NON TESTÉ
    # NON IMPLEMENTÉ
    def vider_cargo(self):
        if self.estAccoste is None:
            return
        listeRessources = self.inventaire.keys()

        for i in listeRessources:
            self.estAccoste.inventaire.update({i: self.estAccoste.inventaire.get(i) + self.inventaire.get(i)})
            self.inventaire.update({i: 0})

    '''
    Fonction effectue le transfert des ressources en ajoutant les quantités de ressources dans l'inventaire du cargo et en enlevant les quantités de ressources dans l'inventaire de l'étoile accostée
    Args:
        chargment est un dictionnaire des ressources à transferer de l'étoile -> cargo
    '''

    def transfererRessources(self, chargement):# chargement contient les quantite de matiere que lutilisateur veut

        if self.isTransferable(chargement):
            listeRessources = chargement.keys()
            #pour le cargo
            for i in range (0, len(listeRessources)):
                self.inventaire.update(listeRessources[i], self.inventaire.get(listeRessources[i]) + chargement.get(listeRessources[i]))
            #pour l'étoile
            for i in range (0, len(listeRessources)):
                self.estAccoste.inventaire.update(listeRessources[i], self.estAccoste.inventaire.get(listeRessources) - chargement.get(listeRessources[i]))

    '''
    Fonction détermine si un transfert de ressources d'étoile -> cargo est possible.
    Args : 
        chargement est un dictionnaire des ressources à transferer de l'étoile -> cargo
    Returns false si le transfert est impossible, true si le transfert est valide
    '''
    def isTransferable(self, chargement):
        listeQuantites = chargement.values()
        listeRessources = chargement.keys()
        qtTotale:int = 0

        #Pour déterminer si la capacité du cargo n'est pas dépassée
        for i in range (0, len(listeQuantites)):
            qtTotale += listeQuantites[i]
        if qtTotale > self.capaciteMax:
            return False

        #Pour déterminer si les quantités choisies sont valides
        for i in range (0, len(listeRessources)):
            if chargement.get(listeRessources[i]) > self.estAccoste.inventaire.get(listeRessources[i]):
                return False
        return True

    '''
    Fonction permet de déterminer la quantité maximale qu'une ressource peut être transférée d'une étoile -> cargo
    Args:
        ressource : string représentant le nom de la ressource à prendre son maximum
    Returns un int représentant la quantité maximale de la ressource à prendre
    '''
    def maximumRessource(self, ressource:str):
        qtMax:int = 0
        if self.estAccoste.inventaire.get(ressource) <= self.capaciteMax - self.capaciteUtilise:
            qtMax = self.estAccoste.inventaire.get(ressource)
        else:
            qtMax = self.capaciteMax - self.capaciteUtilise
        return qtMax

class Eclaireur(Vaisseau):  #TODO À CHANGER
    def __init__(self, parent, nom, x, y, estAccoste, tempsConstruction, cadreDebutConstruction, type_vaisseau):
        Vaisseau.__init__(self, parent, nom, x, y, estAccoste, tempsConstruction, cadreDebutConstruction, type_vaisseau)
        self.energie = 500
        self.taille = 4
        self.vitesse = 5
        self.cible = 0
        self.ang = 0


class Joueur(): #TODO renommer dictionnaire Vaisseau pour Explorateur, ajouter attaquant
    def __init__(self, parent, nom, etoilemere, couleur):
        self.id = get_prochain_id()
        self.parent = parent
        self.nom = nom
        self.etoilemere = etoilemere
        self.etoilemere.proprietaire = self.nom
        self.couleur = couleur
        #self.log = []      journal de débogage
        self.etoilescontrolees = [etoilemere]   #tableau de toutes les étoiles de l'empire contenant l'étoile mère par défaut
        self.flotte = {"Vaisseau": {},  #Dictionnaire contenant un dictionnaire de tous les vaisseaux par type de vaisseau
                       "Cargo": {},
                       "Eclaireur": {}}
        self.actions = {"creervaisseau": self.creervaisseau,    #Appel la fonction de création de vaisseau : À DÉPLACER DANS LA CLASS ENTREPOT
                        "ciblerflotte": self.ciblerflotte,
                        "construire": self.construire}      #Appel la fonction

    def construire(self, params):
        typeInstallation = params[0]
        idEtoile = params[1]
        for e in self.etoilescontrolees:
            if e.id == idEtoile:
                e.creer_installation(typeInstallation, params[2])

    def creervaisseau(self, params): #Fonction qui permet de créer un vaisseau \\\ À DÉPLACER DANS LA CLASSE ENTREPOT : IL FAUT CRÉER UN VAISSEAU DANS UN ENTREPOT, PAS PAR LE JOUEUR
        for e in self.etoilescontrolees:
            if e.id == params[3]:
                if e.installations.get("entrepot").isLibre() is not None:
                    type_vaisseau = params[0]
                    cadreDebutConstruction = params[4]
                    if type_vaisseau == "Cargo":
                        v = Cargo(self, self.nom, int(params[1]) + 10, int(params[2]), e.id, 15, cadreDebutConstruction, type_vaisseau)
                    elif type_vaisseau == "Vaisseau":
                        v = Vaisseau(self, self.nom, int(params[1]) + 10, int(params[2]), e.id, 15, cadreDebutConstruction, type_vaisseau)
                    else:
                        v = Eclaireur(self, self.nom, int(params[1]) + 10, int(params[2]), e.id, 15, cadreDebutConstruction, type_vaisseau)

                    slot = e.installations.get("entrepot").isLibre()
                    e.installations.get("entrepot").capacite.update({slot:v}) #Attribue le vaisseau en construction dans le premier slot de l'entrepot

    def finConstructionVaisseau(self, vaisseau):
        self.flotte[vaisseau.type_vaisseau][vaisseau.id] = vaisseau
        if self.nom == self.parent.parent.mon_nom:
            self.parent.parent.lister_objet(vaisseau.type_vaisseau, vaisseau.id, vaisseau.niveau_Vaisseau)

    def ciblerflotte(self, ids): #Cette fonction sera complètement refaite. //fait avancer les vaisseaux
        idori, iddesti, type_cible = ids        #idor = orig-ine, iddesti = destination
        ori = None
        for i in self.flotte.keys():
            if idori in self.flotte[i]:
                ori = self.flotte[i][idori]

        if ori:
            if type_cible == "Etoile":
                for j in self.parent.etoiles:
                    if j.id == iddesti:
                        ori.acquerir_cible(j, type_cible)
                        return
            elif type_cible == "Porte_de_ver":
                cible = None
                for j in self.parent.trou_de_vers:
                    if j.porte_a.id == iddesti:
                        cible = j.porte_a
                    elif j.porte_b.id == iddesti:
                        cible = j.porte_b
                    if cible:
                        ori.acquerir_cible(cible, type_cible)
                        return


    def jouer_prochain_coup(self):
        self.avancer_flotte()

    def avancer_flotte(self, chercher_nouveau=0):
        cargoEstAccost = False
        for i in self.flotte: #Chaque type de vaisseau

             for j in self.flotte[i]:
                j = self.flotte[i][j]
                rep = j.jouer_prochain_coup(chercher_nouveau) #Retourne liste ["TypeObjet", objet]
                if rep:
                    if rep[0] == "Etoile":
                        xEtoile = rep[1].x
                        yEtoile = rep[1].y
                        xVaisseau = j.x
                        yVaisseau = j.y

                        if(abs(xEtoile - xVaisseau) <= 100 and abs(yEtoile - yVaisseau) <= 100): #Création de la hitbox
                            print("Hitbox collided")#quand le cargot arrive sur etoile on arrive ICI!!!
                            #si i == "Eclaireur"
                            #si la planete est neutre
                            #bool peuConstruireEntrepot = true
                            if(i == "Cargo"):#si je selectionne un cargo
                                #si le cargot est accoste
                                 cargoEstAccost = True
                                #faire boolean cargotEstAccos = true -> mais il faut remettre cette variable a false a la ligne 208. Comment la recuperer la variable de la ligne 208??
                                #utiliser cette variable avec la fonction recupererValeurEstAccoste dans le main et levoyer dans Vue.



                            j.estAccoste = rep[1] #dans estAccoste est stocke l<id de letoile ou le cargot est accoste -> donc il a une valeur id donc sera true
                            self.parent.parent.recupererValeurEstAccoste(j.estAccoste, cargoEstAccost)#cette fonction est cree dans le main -> pb: sera toujours true
                            self.etoilescontrolees.append(rep[1])
                            if rep[1].proprietaire == 'neutre' or rep[1].vie <= 0:
                                rep[1].proprietaire = j.proprietaire
                                self.parent.parent.afficher_etoile(self.nom, rep[1])
                            print(rep[1].proprietaire, j.proprietaire)

                            if rep[1].proprietaire != j.proprietaire and rep[1].proprietaire != 'neutre':
                                if( rep[1].vie > j.vie):
                                    rep[1].vie -= j.vie
                                    j.vie = 0
                                else:
                                    j.vie -= rep[1].vie
                                    rep[1].vie = 0


                                print(rep[1].vie, j.vie)





                    elif rep[0] == "Porte_de_ver":
                        pass

class Installation():
    def __init__(self, parent, proprietaire, type, cadre_debut_construction):
        self.parent = parent
        self.proprietaire = proprietaire
        self.type = type
        self.niveau = 0
        self.cout = self.cout_selon_niveau()
        self.cadre_debut_construction = cadre_debut_construction

    def cout_selon_niveau(self):
        if self.type == "entrepot":
            if self.niveau == 0: #niveau 0 = entrepôt à construire
                self.cout = {"Fer":50,
                             "Cuivre":15,
                             "Or":0,
                             "Titane":0,
                             "Hydrogene":25,
                             "Plutonium":0,
                             "Antimatiere":0}
            elif self.niveau == 1:
                self.cout = {"Fer":75,
                             "Cuivre":25,
                             "Or":5,
                             "Titane": 0,
                             "Hydrogene":40,
                             "Plutonium":0,
                             "Antimatiere":0}
            elif self.niveau == 2:
                self.cout = {"Fer":100,
                             "Cuivre":35,
                             "Or":15,
                             "Titane": 0,
                             "Hydrogene":55,
                             "Plutonium": 5,
                             "Antimatiere":0}
            elif self.niveau == 3:
                self.cout = {"Fer": 150,
                             "Cuivre": 55,
                             "Or": 25,
                             "Titane": 15,
                             "Hydrogene": 85,
                             "Plutonium": 25,
                             "Antimatiere":2}

        elif self.type == "usine":
            if self.niveau == 0: #niveau 0 = usine à construire
                self.cout = {"Fer":35,
                             "Cuivre":5,
                             "Or": 0,
                             "Titane": 0,
                             "Hydrogene":15,
                             "Plutonium":0,
                             "Antimatiere":0}
            elif self.niveau == 1:
                self.cout = {"Fer":50,
                             "Cuivre":15,
                             "Or":5,
                             "Titane": 0,
                             "Hydrogene":30,
                             "Plutonium":0,
                             "Antimatiere":0}
            elif self.niveau == 2:
                self.cout = {"Fer":80,
                             "Cuivre":30,
                             "Or":15,
                             "Titane": 0,
                             "Hydrogene":55,
                             "Plutonium": 5,
                             "Antimatiere":0}
            elif self.niveau == 3:
                self.cout = {"Fer": 125,
                             "Cuivre": 55,
                             "Or": 20,
                             "Titane": 25,
                             "Hydrogene": 85,
                             "Plutonium": 45,
                             "Antimatiere":3}
        return self.cout

class Usine(Installation):
    def __init__(self, parent, proprietaire, type, cadre_debut_construction, production):
        self.production = production
        super().__init__(parent, proprietaire, type, cadre_debut_construction)


class Entrepot(Installation):
    def __init__(self, parent, proprietaire, type, cadre_debut_construction):
        self.capacite = {"slot1": None,
                         "slot2": None,
                         "slot3": None}
        super().__init__( parent, proprietaire, type, cadre_debut_construction)
        self.keysSlots = None

    '''
        La fonction détermine si un emplacement dans l'entrepot est libre pour y construire un vaisseau. 
        Returns le slot libre ou false si aucun slot n'est disponible.
    '''
    def isLibre(self):
        self.keysSlots = self.capacite.keys()
        for k in self.keysSlots:
            if self.capacite.get(k) is None:
                return k
        return False

    def constructionVaisseau(self, cadre):
        self.keysSlots = self.capacite.keys()
        for k in self.keysSlots:
            if self.capacite.get(k) is not None:
                if cadre == self.capacite.get(k).cadreDebutConstruction + 100:
                    self.v = self.capacite.get(k)
                    print(self.v)
                    self.v.parent.finConstructionVaisseau(self.v)
                    self.capacite.update({k:None})


class Modele():
    def __init__(self, parent, joueurs):
        self.parent = parent
        self.largeur = 9000
        self.hauteur = 9000
        self.nb_etoiles = int((self.hauteur * self.largeur) / 500000)
        self.joueurs = {}
        self.actions_a_faire = {}
        self.etoiles = []
        self.trou_de_vers = []
        self.cadre_courant = None
        self.ressources = {"Fer": Ressources("Fer", 1),
                           "Cuivre": Ressources("Cuivre", 1),
                           "Or": Ressources("Or", 2),
                           "Titane": Ressources("Titane", 3),
                           "Hydrogene": Ressources("Hydrogene", 1),
                           "Plutonium": Ressources("Plutonium", 2),
                           "Antimatiere": Ressources("Antimatiere", 3)}
        self.creeretoiles(joueurs)
        nb_trou = int((self.hauteur * self.largeur) / 5000000)
        self.creer_troudevers(nb_trou)

    def recupererEtoile(self, id):
        id_text = str(id)
        for e in self.etoiles:
            if e.id == id_text:
                recup = e
        return recup

    def recupererJoueur(self, id):
        keys = self.joueurs.keys()
        for j in keys:
            if self.joueurs.get(j).nom == id:
                recup = self.joueurs.get(j)
        return recup


    def creer_troudevers(self, n):
        bordure = 10
        for i in range(n):
            x1 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y1 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            x2 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y2 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.trou_de_vers.append(Trou_de_vers(x1, y1, x2, y2))

    def creeretoiles(self, joueurs):
        bordure = 10
        for i in range(self.nb_etoiles):
            x = random.randrange(self.largeur - (2 * bordure)) + bordure
            y = random.randrange(self.hauteur - (2 * bordure)) + bordure
            nom:str = "Etoile" + str(i)
            ressourcesExploitables = self.genererRessources()
            self.etoiles.append(Etoile(self,x,y,nom,ressourcesExploitables))
        np = len(joueurs) #np = number of players
        etoile_occupee = []
        while np:   #Choisi les étoiles mères
            p = random.choice(self.etoiles)
            if p not in etoile_occupee:
                etoile_occupee.append(p)
                np -= 1

        couleurs = ["red", "blue", "lightgreen", "yellow",
                    "lightblue", "pink", "gold", "purple"]
        for i in joueurs:
            etoile = etoile_occupee.pop(0) #Attribution d'une étoile mère à un joueur
            self.joueurs[i] = Joueur(self, i, etoile, couleurs.pop(0))


    def genererRessources(self):
        #Ajouter algorithme de génération des ressources ici - ressources possibles : Fer, Cuivre, Or, Titane || Hydrogène, Plutonium, Antimatière
        nbMateriaux:int = 1;
        nbEnergie:int = 0;

        distFer:float = 0
        distCuivre:float = 0
        distOr:float = 0
        distTitane:float = 0
        distHydrogene:float = 0
        distPlutonium:float = 0
        distAntimatiere:float = 0
        distZoneGrise:float = 0

        ressourcesExploitables = {"Fer":0.00,
                                  "Cuivre":0.00,
                                  "Or":0.00,
                                  "Titane":0.00,
                                  "Hydrogene":0.00,
                                  "Plutonium":0.00,
                                  "Antimatiere":0.00}

        isFer:bool = True #il y aua toujours du fer sur une étoile
        isCuivre:bool = False
        isOr:bool = False
        isTitane:bool = False
        isHydrogene:bool = False
        isPlutonium:bool = False
        isAntimatiere:bool = False

        rareteMateriaux:int = random.randrange(0, 100) #représente un "dé"
        rareteEnergie:int = random.randrange(0, 100)

        #dé des matériaux
        if rareteMateriaux >= 40:
            isCuivre = True
            nbMateriaux +=1
            if rareteMateriaux >= 70:
                isOr = True
                nbMateriaux += 1
                if rareteMateriaux >= 90:
                    isTitane = True
                    nbMateriaux += 1

        #dé des énergies
        if rareteEnergie >= 25:
            isHydrogene = True
            nbEnergie += 1
            if rareteMateriaux >= 75:
                isPlutonium = True
                nbEnergie += 1
                if rareteEnergie >= 97:
                    isAntimatiere = True
                    nbEnergie += 1

        #Distribution matériaux / étoile
        if nbMateriaux == 1:
            distFer = 1.00
        elif nbMateriaux == 2:
            distZoneGrise = round(self.zoneGrise(), 2)
            distFer = 0.65 + distZoneGrise
            distCuivre = 0.25 + (0.10 - distZoneGrise)
        elif nbMateriaux == 3:
            distZoneGrise = round(self.zoneGrise(), 2) #pour déterminer la zone tampon entre le fer et le cuivre
            distFer = 0.50 + distZoneGrise
            distCuivre = 0.20 + (0.10 - distZoneGrise)
            distZoneGrise = round(self.zoneGrise(), 2) #pour déterminer la zone tampon entre le cuivre et l'or
            distCuivre += distZoneGrise
            distOr = 0.10 + (0.10 - distZoneGrise)
        elif nbMateriaux == 4:
            distZoneGrise = round(self.zoneGrise(), 2)
            distFer = 0.40 + distZoneGrise
            distCuivre = 0.15 + (0.10 - distZoneGrise)
            distZoneGrise = round(self.zoneGrise(), 2) #pour zone tampon entre cuivre et or
            distCuivre += distZoneGrise
            distOr = 0.10 + (0.10 - distZoneGrise)
            distZoneGrise = round(self.zoneGrise(), 2) #pour zone tampon entre or et titane
            distOr += distZoneGrise
            distTitane = 0.05 + (0.10 - distZoneGrise)

        #Distribution énergie / étoile
        if nbEnergie == 1:
            distHydrogene = 1.00
        elif nbEnergie == 2:
            distZoneGrise = self.zoneGrise()
            distHydrogene = 0.65 + distZoneGrise
            distPlutonium = 0.25 + (0.10 - distZoneGrise)
        elif nbEnergie == 3:
            distZoneGrise = self.zoneGrise()
            distHydrogene = 0.60 + distZoneGrise
            distPlutonium = 0.17 + (0.10 - distZoneGrise)
            distZoneGrise = self.zoneGrise()
            distPlutonium += distZoneGrise
            distAntimatiere = 0.03 + (0.10 - distZoneGrise)

        #Attribution des distributions
        ressourcesExploitables.update({"Fer": distFer})
        ressourcesExploitables.update({"Cuivre":distCuivre})
        ressourcesExploitables.update({"Or":distOr})
        ressourcesExploitables.update({"Titane":distTitane})
        ressourcesExploitables.update({"Hydrogene":distHydrogene})
        ressourcesExploitables.update({"Plutonium":distPlutonium})
        ressourcesExploitables.update({"Antimatiere":distAntimatiere})

        return ressourcesExploitables

    def zoneGrise(self):
        return random.uniform(0.00, 0.10)


    ##############################################################################
    def jouer_prochain_coup(self, cadre):
        #  NE PAS TOUCHER LES LIGNES SUIVANTES  ################
        self.cadre_courant = cadre
        cadreActuel = cadre
        # insertion de la prochaine action demandée par le joueur
        if cadre in self.actions_a_faire:
            for i in self.actions_a_faire[cadre]:
                self.joueurs[i[0]].actions[i[1]](i[2])
                """
                i a la forme suivante [nomjoueur, action, [arguments]]
                alors self.joueurs[i[0]] -> trouve l'objet représentant le joueur de ce nom
                """
            del self.actions_a_faire[cadre]
        # FIN DE L'INTERDICTION #################################

        # demander aux objets de jouer leur prochain coup
        # aux joueurs en premier
        for i in self.joueurs:
            self.joueurs[i].jouer_prochain_coup()

        # NOTE si le modele (qui représente l'univers !!! )
        #      fait des actions - on les activera ici...
        for i in self.trou_de_vers:
            i.jouer_prochain_coup()

        coefProduction = 0
        for i in self.etoiles:
           i.production(cadre)

        # Timers de construction - Gère la construction
        # Des vaisseaux
        for i in self.etoiles:
            if i.installations.get("entrepot") is not None:
                i.installations.get("entrepot").constructionVaisseau(cadre)

        # Des installations
        for i in self.etoiles:
            if i.installations.get("entrepot") is None:
                i.verifier_fin_construction(cadre)
            else:
                i.verifier_fin_construction(cadre)

       # for i in self.etoiles:
         #   self.etoiles[i].jouer_prochain_coup()

    def creer_bibittes_spatiales(self, nb_biittes=0):
        pass

    #############################################################################
    # ATTENTION : NE PAS TOUCHER
    def ajouter_actions_a_faire(self, actionsrecues):
        cadrecle = None
        for i in actionsrecues:
            cadrecle = i[0]
            if cadrecle:
                if (self.parent.cadrejeu - 1) > int(cadrecle):
                    print("PEUX PASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                action = ast.literal_eval(i[1])

                if cadrecle not in self.actions_a_faire.keys():
                    self.actions_a_faire[cadrecle] = action
                else:
                    self.actions_a_faire[cadrecle].append(action)
    # NE PAS TOUCHER - FIN
##############################################################################
