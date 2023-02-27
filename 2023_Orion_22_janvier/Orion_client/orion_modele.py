# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd
import math
import random
import ast
from id import *
from helper import Helper as hlp


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
        self.tempsExtraction = rarete * rarete * 5;

class Etoile():
    def __init__(self, parent, x, y, nomEtoile, ressource, vie):

        self.id = get_prochain_id()
        self.parent = parent
        #self.proprietaire = ""
        self.x = x
        self.y = y
        self.taille = random.randrange(4, 8)
        self.nomEtoile = nomEtoile
        self.ressources = ressource ## ressources = [] ressources
        self.proprietaire = "neutre" #proprietaire = etoile owner
        self.installation = None #installation = [] des installations du joueur
        self.vaisseaux = None # [] de vaisseaux pose sur letoile
        self.estEclaire = False #etoile selectionne ou pas True ou False = False au debut du jeu
        self.niveauEtoile = 1 #niveau de l'étoile = 1/2/3 = toutes les étoiles seront de niveau 1 au debut du jeu
        self.inventaire = None  # inventaire = [] d'inventaire de ce que possede le joueur
        self.vie = vie # nbr de vie de la planete

class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Deplacement():
    def __init__(self, positionOrigine, positionDestination):
        self.positionOrigine = positionOrigine
        self.positionDestination = positionDestination


class Vaisseau():
    def __init__(self, parent, nom, x, y,niveau_Vaisseau,type_Vaisseau,estAccoste,tempsConstruction,Vie,Icone):
        self.parent = parent
        self.id = get_prochain_id()
        self.proprietaire = nom
        self.type_Vaisseau = type_Vaisseau
        self.niveau_Vaisseau = niveau_Vaisseau
        self.tempsConstruction = tempsConstruction
        self.estAccoste = estAccoste
        self.Deplacement = None
        #HP du vaiseau
        self.Vie = Vie
        #Image du vaisseau
        self.Icone = Icone
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
            x = self.cible.x
            y = self.cible.y
            self.x, self.y = hlp.getAngledPoint(self.angle_cible, self.vitesse, self.x, self.y)
            if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
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


class Cargo(Vaisseau):  #TODO À CHANGER
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.cargo = 1000
        self.energie = 500
        self.taille = 6
        self.vitesse = 1
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
                       "Cargo": {}}
        self.actions = {"creervaisseau": self.creervaisseau,    #Appel la fonction de création de vaisseau : À DÉPLACER DANS LA CLASS ENTREPOT
                        "ciblerflotte": self.ciblerflotte}      #Appel la fonction

    def creervaisseau(self, params): #Fonction qui permet de créer un vaisseau \\\ À DÉPLACER DANS LA CLASSE ENTREPOT : IL FAUT CRÉER UN VAISSEAU DANS UN ENTREPOT, PAS PAR LE JOUEUR
        type_vaisseau = params[0]
        if type_vaisseau == "Cargo":
            v = Cargo(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y)
        else:
            v = Vaisseau(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y, 1, "a",True,15,15,0)
        self.flotte[type_vaisseau][v.id] = v

        if self.nom == self.parent.parent.mon_nom:
            self.parent.parent.lister_objet(type_vaisseau, v.id)
        return v

    def ciblerflotte(self, ids): #Cette fonction sera complètement refaite.
        idori, iddesti, type_cible = ids        #idor = origine, iddesti = destination
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
                            print("Hitbox collided")
                            self.etoilescontrolees.append(rep[1])
                            self.parent.parent.afficher_etoile(self.nom, rep[1])
                    elif rep[0] == "Porte_de_ver":
                        pass

class Installation():
    def __init__(self, parent, proprietaire, type, niveau, cout, temps):
        self.parent = parent
        self.proprietaire = proprietaire
        self.type = type
        self.niveau = niveau
        self.cout = cout
        self.temps = temps

class Usine(Installation):
    def __init__(self, parent, proprietaire, type, niveau, cout, temps, production):
        Installation.__init__(self, parent, proprietaire, type, niveau, cout, temps)
        self.production = production

class Entrepot(Installation):
    def __init(self, parent, proprietaire, type, niveau, cout, temps, capacite):
        Installation.__init__(self, parent, proprietaire, type, niveau, cout, temps)
        self.capacite = capacite

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
            self.etoiles.append(Etoile(self,x,y,nom,ressourcesExploitables,100))
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
        ressourcesExploitables = []
        ressource = []
        nbRessources:int = 1
        isFer:bool = True #il y aua toujours du fer sur une étoile
        isCuivre:bool = False
        isOr:bool = False
        isTitane:bool = False

        isHydrogene:bool = False
        isPlutonium:bool = False
        isAntimatiere:bool = False

        rareteMateriaux:int = random.randrange(0, 100) #représente un "dé"
        rareteEnergie:int = random.randrange(0, 100)
        distTitane:float = 0

        #dé des matériaux
        if rareteMateriaux >= 40:
            isCuivre = True
            nbRessources +=1
            if rareteMateriaux >= 70:
                isOr = True
                nbRessources += 1
                if rareteMateriaux >= 90:
                    isTitane = True
                    nbRessources += 1
        #dé des énergies
        if rareteEnergie >= 25:
            isHydrogene = True
            nbRessources += 1
            if rareteMateriaux >= 75:
                isPlutonium = True
                nbRessources += 1
                if rareteEnergie >= 97:
                    isAntimatiere = True
                    nbRessources += 1

        distFer:float = self.distributionFer(nbRessources) #distribution du fer / étoile (un %)
        distFer = round(distFer,2)
        ressource.append("Fer")
        ressource.append(distFer)
        ressourcesExploitables.append(ressource)
        print(ressourcesExploitables)
        if isCuivre:
            aCuivre:float = ((self.distributionFer(4) + 0.4) - 1) / 2 #Pour calculer le taux de variation de l'équation de distribution du cuivre
            distCuivre:float = aCuivre * nbRessources + 0.9
            distCuivre = round(distCuivre,2)
            ressource.append("Cuivre")
            ressource.append(distCuivre)
            ressourcesExploitables.append(ressource)

        print(ressourcesExploitables)
        return ressourcesExploitables

    def distributionFer(self, nbRessources:int):
        return -0.481 * math.log(nbRessources) + 1.0072

    ##############################################################################
    def jouer_prochain_coup(self, cadre):
        #  NE PAS TOUCHER LES LIGNES SUIVANTES  ################
        self.cadre_courant = cadre
        # insertion de la prochaine action demandée par le joueur
        if cadre in self.actions_a_faire:
            for i in self.actions_a_faire[cadre]:
                self.joueurs[i[0]].actions[i[1]](i[2])
                """
                i a la forme suivante [nomjoueur, action, [arguments]
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
