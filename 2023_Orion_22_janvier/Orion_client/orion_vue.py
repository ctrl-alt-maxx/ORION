# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

from tkinter import *
from tkinter.ttk import *
from tkinter.simpledialog import *
from tkinter.messagebox import *
from helper import Helper as hlp
import math
# from PIL import ImageTk, Image
import tkinter as tk
import time
import os, os.path

from orion_modele import *



import random

#ffff
class Vue():
    def __init__(self, parent, urlserveur, mon_nom, msg_initial):
        self.estAccos = None
        self.parent = parent
        self.root = Tk()
        self.root.title("Player: " + mon_nom)


        self.images= {}

        self.chargerimages()

        self.mon_nom = mon_nom
        # attributs
        self.taille_minimap = 240
        self.zoom = 2
        self.ma_selection = None
        self.cadre_actif = None
        # cadre principal de l'application
        self.cadre_app = Frame(self.root, width=500, height=400, bg="red")
        self.cadre_app.pack(expand=1, fill=BOTH)
        # # un dictionnaire pour conserver les divers cadres du jeu, creer plus bas
        self.cadres = {}
        self.creer_cadres(urlserveur, mon_nom, msg_initial)
        self.changer_cadre("splash")
        # PROTOCOLE POUR INTERCEPTER LA FERMETURE DU ROOT - qui termine l'application
        # self.root.protocol("WM_DELETE_WINDOW", self.demander_abandon)

        # # sera charge apres l'initialisation de la partie, contient les donnees pour mettre l'interface a jour
        self.modele = None
        # # variable pour suivre le trace du multiselect
        self.debut_selection = []
        self.selecteur_actif = None
        self.shipSelected = []

        #Chercher les images

        #self.img = None
        #self.pathImgEclaireur = Image.open('C:/Users/2077407/Documents/GitHub/C41/2023_Orion_22_janvier/img/eclaireur.png')



        #creation label Frame pour méthode methode_installation et methode_ressource
        self.boutonAmeliorerEtoile = Button()
        self.label_installation = Label()
        self.label_ressource = Label()
        self.label_hydrogene = Label()
        self.label_fer = Label()
        self.label_or = Label()
        self.label_cuivre = Label()
        self.label_antimatiere = Label()
        self.label_pluto = Label()
        self.label_titane = Label()
        self.label_titre = Label()
        self.canev = Canvas()
        self.boutonConstruireUsine = Button()
        self.label_entrepotVaisseau = Label()
        self.boutonConstruireEntrepot = Button()
        self.label_qte_fer = Label()
        self.clickUneFoisSurInsta = 0 #pour que le frame ne reaparaisse pas si je clique 2 fois de suite sur le meme bouton
        self.clickUneFoisSurRessource = 0
        self.clickUneFoisSurVaiss = 0
        self.percentage_label = Label()
        # var global methode installation()
        self.cadre_label_ressource = Frame()
        self.label_titre = Label()
        self.cadre_img = Frame()
        self.label_img = Label()
        self.label_installation = Label()
        self.cadre_bouton = Frame()
        self.boutonConstruireUsine = Button()
        self.boutonAmeliorerUsine = Button()
        self.cadre_espacement = Frame()

        self.cadre_label_entrepot_vaisseau = Frame()
        self.label_entrepotVaisseau = Label()
        self.cadre_img2 = Frame()
        self.label_img2 = Label()
        self.label_installation2 = Label()
        self.cadre_bouton2 = Frame()
        self.boutonConstruireEntrepot = Button()

        #creation des cadres
        self.cadre_menu_installation = Frame()
        self.cadre_menu_ressource = Frame()
        self.cadre_menu_ressource_ex = Frame()
        self.cadre_bouton_construction_vaisseau = Frame()
        self.cadre_bouton_transferer = Frame()
        self.cadre_choisir_transfere = Frame()
        self.cadre_option = Frame()

        #notification
        self.cadre_notification = Frame()
        self.label_notification = Label()

        self.startTime = 0
        self.strPourcentage = 0
        self.laConstruction = ""
        self.strName = ""
        self.chiffre = 0

        self.selectedTags = None
        #pour test mais a ameliorer
        self.peutAfficherBouton = True
        self.type_vaisseau_selectionne = ""
        self.cargoArrive = False

        self.started = False
        self.nbr_entrepot = 0
        self.nbr_usine = 0
        self.recup = None
        self.idCargo = None
        self.objet = ""
        self.etoileSelectionne = None
        self.etoileOuEstPoseLeCargo = None






    def savoirSiAccoste(self, estAccoste, cargotEstAccoste): #est appele dans main
        self.estAccos = estAccoste
        self.cargoArrive = cargotEstAccoste

        if(self.estAccos): #si un vaisseau est accoste
         if(self.cargoArrive):# savoir si le cargot est accoste
                 self.cadre_bouton_transferer.pack_forget()
                 self.faireApparaitreBoutonTransfere()# on affiche le bouton
        #    else sinon on enleve le bouton

    def faireApparaitreBoutonTransfere(self):
        self.cadre_bouton_transferer = Frame(self.cadreoutils ,width=200, height=200)
        self.cadre_bouton_transferer.pack()
        self.bouton = Button(self.cadre_bouton_transferer, text="bouton transfere",command=self.choisir_transfere)
        self.bouton.pack()
        #creation des labels autres
        self.timer_partie = Label()

    def choisir_transfere(self):#methode quand on clique sur le bouton transferer qui affiche le menu permettant de transférer les ressources de l'inventaire de l'étoile à l'inventaire du cargo
        self.cadre_bouton_transferer.pack_forget()
        self.cadre_choisir_transfere = Frame(self.cadreoutils, width=400, height=200)
        # FER-----
        self.cadre_quantite_fer = Frame(self.cadre_choisir_transfere, width=200, height=200)
        self.label_qtite_fer = Label(self.cadre_quantite_fer,text="Fer:")
        self.label_chiffre_fer = Label(self.cadre_quantite_fer,text= str(round(self.recup.inventaire.get("Fer"), 2)))#quantite presente sur letoie

        self.cadre_entre_qtite_fer = Frame(self.cadre_choisir_transfere, width=400, height=200)
        self.label_entrez_qtite = Label(self.cadre_entre_qtite_fer, text="Entrez une quantite:")
        self.entree_qtiteFer = Entry(self.cadre_entre_qtite_fer)
        quantiteFerEntre = self.entree_qtiteFer.get(); #on recupere la valeur que lutilisateur a entre


        self.cadre_choisir_transfere.pack()
        self.cadre_quantite_fer.pack()
        self.label_qtite_fer.pack(side=LEFT)
        self.label_chiffre_fer.pack()
        self.cadre_entre_qtite_fer.pack(fill=X)
        self.label_entrez_qtite.pack(side=LEFT)
        self.entree_qtiteFer.pack()

        # cuivre
        self.cadre_quantite_cuivre = Frame(self.cadre_choisir_transfere, width=200, height=200)
        self.label_qtite_cuivre = Label(self.cadre_quantite_cuivre, text= "Cuivre:")
        self.label_chiffre_cuivre = Label(self.cadre_quantite_cuivre, text=str(round(self.recup.inventaire.get("Cuivre"), 2)))

        self.cadre_entre_qtite_cuivre = Frame(self.cadre_choisir_transfere, width=400, height=200)
        self.label_entrez_qtite_cuivre = Label(self.cadre_entre_qtite_cuivre, text="Entrez une quantite:")
        self.entre_qtiteCuivre = Entry(self.cadre_entre_qtite_cuivre)

        self.cadre_quantite_cuivre.pack()
        self.label_qtite_cuivre.pack(side=LEFT)
        self.label_chiffre_cuivre.pack()

        self.cadre_entre_qtite_cuivre.pack(fill=X)
        self.label_entrez_qtite_cuivre.pack(side=LEFT)
        self.entre_qtiteCuivre.pack()

        #OR
        self.cadre_quantite_or = Frame(self.cadre_choisir_transfere, width=200, height=200)
        self.label_qtite_or = Label(self.cadre_quantite_or, text="Or:")
        self.label_chiffre_or = Label(self.cadre_quantite_or, text=str(round(self.recup.inventaire.get("Or"), 2)))

        self.cadre_entre_qtite_or = Frame(self.cadre_choisir_transfere, width=400, height=200)
        self.label_entrez_qtite_or = Label(self.cadre_entre_qtite_or, text="Entrez une quantite:")
        self.entre_qtiteOr = Entry(self.cadre_entre_qtite_or)

        self.cadre_quantite_or.pack()
        self.label_qtite_or.pack(side=LEFT)
        self.label_chiffre_or.pack()

        self.cadre_entre_qtite_or.pack(fill=X)
        self.label_entrez_qtite_or.pack(side=LEFT)
        self.entre_qtiteOr.pack()

        #Titane
        self.cadre_quantite_titane = Frame(self.cadre_choisir_transfere, width=200, height=200)
        self.label_qtite_titane = Label(self.cadre_quantite_titane, text="Titane:")
        self.label_chiffre_titane = Label(self.cadre_quantite_titane, text=str(round(self.recup.inventaire.get("Titane"), 2)))

        self.cadre_entre_qtite_titane = Frame(self.cadre_choisir_transfere, width=400, height=200)
        self.label_entrez_qtite_titane = Label(self.cadre_entre_qtite_titane, text="Entrez une quantite:")
        self.entre_qtiteTitane = Entry(self.cadre_entre_qtite_titane)

        self.cadre_quantite_titane.pack()
        self.label_qtite_titane.pack(side=LEFT)
        self.label_chiffre_titane.pack()

        self.cadre_entre_qtite_titane.pack(fill=X)
        self.label_entrez_qtite_titane.pack(side=LEFT)
        self.entre_qtiteTitane.pack()

        #Hydrogene
        self.cadre_quantite_hydrogene = Frame(self.cadre_choisir_transfere, width=200, height=200)
        self.label_qtite_hydrogene = Label(self.cadre_quantite_hydrogene, text="Hydrogene:")
        self.label_chiffre_hydrogene = Label(self.cadre_quantite_hydrogene, text=str(round(self.recup.inventaire.get("Hydrogene"), 2)))

        self.cadre_entre_qtite_hydrogene = Frame(self.cadre_choisir_transfere, width=400, height=200)
        self.label_entrez_qtite_hydrogene = Label(self.cadre_entre_qtite_hydrogene, text="Entrez une quantite:")
        self.entre_qtiteHydrogene = Entry(self.cadre_entre_qtite_hydrogene)

        self.cadre_quantite_hydrogene.pack()
        self.label_qtite_hydrogene.pack(side=LEFT)
        self.label_chiffre_hydrogene.pack()

        self.cadre_entre_qtite_hydrogene.pack(fill=X)
        self.label_entrez_qtite_hydrogene.pack(side=LEFT)
        self.entre_qtiteHydrogene.pack()

        #Plutonium
        self.cadre_quantite_plutonium = Frame(self.cadre_choisir_transfere, width=200, height=200)
        self.label_qtite_plutonium = Label(self.cadre_quantite_plutonium, text="Plutonium:")
        self.label_chiffre_plutonium = Label(self.cadre_quantite_plutonium, text=str(round(self.recup.inventaire.get("Plutonium"), 2)))

        self.cadre_entre_qtite_plutonium = Frame(self.cadre_choisir_transfere, width=400, height=200)
        self.label_entrez_qtite_plutonium = Label(self.cadre_entre_qtite_plutonium, text="Entrez une quantite:")
        self.entre_qtitePlutonium = Entry(self.cadre_entre_qtite_plutonium)

        self.cadre_quantite_plutonium.pack()
        self.label_qtite_plutonium.pack(side=LEFT)
        self.label_chiffre_plutonium.pack()

        self.cadre_entre_qtite_plutonium.pack(fill=X)
        self.label_entrez_qtite_plutonium.pack(side=LEFT)
        self.entre_qtitePlutonium.pack()

        #Antimatiere
        self.cadre_quantite_anti = Frame(self.cadre_choisir_transfere, width=200, height=200)
        self.label_qtite_anti = Label(self.cadre_quantite_anti, text="Antimatiere:")
        self.label_chiffre_anti = Label(self.cadre_quantite_anti, text= str(round(self.recup.inventaire.get("Antimatiere"), 2)))

        self.cadre_entre_qtite_anti = Frame(self.cadre_choisir_transfere, width=400, height=200)
        self.label_entrez_qtite_anti = Label(self.cadre_entre_qtite_anti, text="Entrez une quantite:")
        self.entre_qtiteAntimatiere = Entry(self.cadre_entre_qtite_anti)

        self.cadre_quantite_anti.pack()
        self.label_qtite_anti.pack(side=LEFT)
        self.label_chiffre_anti.pack()

        self.cadre_entre_qtite_anti.pack(fill=X)
        self.label_entrez_qtite_anti.pack(side=LEFT)
        self.entre_qtiteAntimatiere.pack()

        #bouton transferer
        self.cadre_bouton_transferer_mat = Frame(self.cadre_choisir_transfere, width=200, height=200)
        self.boutonTransfererMat = Button(self.cadre_bouton_transferer_mat,text="TANSFERER", command=self.transferer)

        self.cadre_bouton_transferer_mat.pack()
        self.boutonTransfererMat.pack()

        self.peutConstuireEntrpot = False

    def transferer(self):#quand lutilisateur clique sur le bouton transferer on recupere les valeur quil a entre
        #mettre les quantite a 0 au cas ou lutilisateur ne rentre rien
        #quantiteFerEntre = 0;

        dict

        quantiteFerEntre = self.entree_qtiteFer.get();  # on recupere la valeur que lutilisateur a entre
        if(quantiteFerEntre == ''):
            quantiteFerEntre = '0'
        quantiteCuivreEntre = self.entre_qtiteCuivre.get();
        if(quantiteCuivreEntre == ''):
            quantiteCuivreEntre = '0'
        quantiteOrEntre = self.entre_qtiteOr.get();
        if(quantiteOrEntre == ''):
            quantiteOrEntre = '0'
        quantiteTitaneEntre = self.entre_qtiteTitane.get();
        if(quantiteTitaneEntre == ''):
            quantiteTitaneEntre = '0'
        quantiteHydrogeneEntre = self.entre_qtiteHydrogene.get();
        if(quantiteHydrogeneEntre == ''):
            quantiteHydrogeneEntre = '0'
        quantitePlutoniumEntre = self.entre_qtitePlutonium.get();
        if(quantitePlutoniumEntre == ''):
            quantitePlutoniumEntre = '0'
        quantiteAntimatiereEntre = self.entre_qtiteAntimatiere.get();
        if(quantiteAntimatiereEntre == ''):
            quantiteAntimatiereEntre = '0'
        dictChargement = {"Fer":quantiteFerEntre, "Cuivre":quantiteCuivreEntre, "Or":quantiteOrEntre, "Titane": quantiteTitaneEntre, "Hydrogene":quantiteHydrogeneEntre, "Plutonium":quantitePlutoniumEntre, "Antimatiere":quantiteAntimatiereEntre}
        #appeler transfererRessources qui est dans modele pour soustraction
        self.parent.recupQuantiteMatiereDeUtilisateur(dictChargement, self.idCargo); #la jenvoie les quantites que lutilisateur veut au Controlleur
        #memoriser letoile ou est pose le cargot
        #self.etoileOuEstPoseLeCargo = self.etoileSelectionne
        self.cadre_choisir_transfere.pack_forget()



    def chargerimages(self, chemin=None):
        if chemin == None:
            chemin = os.getcwd()
        chemin = chemin + "\\img"
        for i in os.listdir(chemin):
            che = chemin + "\\" + i
            if os.path.isdir(che):
                self.chargerimages(che)
            else:
                nom, ext = os.path.splitext(os.path.basename(i))
                if ".png" == ext:
                    self.images[nom] = PhotoImage(file=che)  # .replace("\\","/")
        return self.images


    def demander_abandon(self):
        rep = askokcancel("Vous voulez vraiment quitter?")
        if rep:
            self.root.after(500, self.root.destroy)


    ####### INTERFACES GRAPHIQUES
    def changer_cadre(self, nomcadre):
        cadre = self.cadres[nomcadre]
        if self.cadre_actif:
            self.cadre_actif.pack_forget()
        self.cadre_actif = cadre
        self.cadre_actif.pack(expand=1, fill=BOTH)

    ###### LES CADRES ############################################################################################
    def creer_cadres(self, urlserveur, mon_nom, msg_initial):
        self.cadres["splash"] = self.creer_cadre_splash(urlserveur, mon_nom, msg_initial)
        self.cadres["lobby"] = self.creer_cadre_lobby()
        self.cadres["partie"] = self.creer_cadre_partie()

    # le splash (ce qui 'splash' à l'écran lors du démarrage)
    # sera le cadre visuel initial lors du lancement de l'application
    def creer_cadre_splash(self, urlserveur, mon_nom, msg_initial):
        self.cadre_splash = Frame(self.cadre_app)
        # un canvas est utilisé pour 'dessiner' les widgets de cette fenêtre voir 'create_window' plus bas
        self.canevas_splash = Canvas(self.cadre_splash, width=600, height=480, bg="#04273d")
        self.canevas_splash.pack()

        # creation ds divers widgets (champ de texte 'Entry' et boutons cliquables (Button)
        self.etatdujeu = Label(text=msg_initial, font=("Arial", 18), borderwidth=2, relief=RIDGE, bg="#010a0f", fg="#c4c4c4")
        self.nomsplash = Entry(font=("Arial", 14), bg="#010a0f", fg="#c4c4c4")
        self.urlsplash = Entry(font=("Arial", 14), width=42, bg="#010a0f", fg="#c4c4c4")
        self.btnurlconnect = Button(text="Connecter", font=("Arial", 12), command=self.connecter_serveur, bg="#010a0f", fg="#c4c4c4")
        # on insère les infos par défaut (nom url) et reçu au démarrage (dispo)
        self.nomsplash.insert(0, mon_nom)
        self.urlsplash.insert(0, urlserveur)
        # on les place sur le canevas_splash
        self.canevas_splash.create_window(320, 100, window=self.etatdujeu, width=400, height=30)
        self.canevas_splash.create_window(320, 200, window=self.nomsplash, width=400, height=30)
        self.canevas_splash.create_window(210, 250, window=self.urlsplash, width=360, height=30)
        self.canevas_splash.create_window(480, 250, window=self.btnurlconnect, width=100, height=30)
        # les boutons d'actions -> FENETRE CONNEXION

        self.btncreerpartie = Button(text="Creer partie", font=("Arial", 12), state=DISABLED, command=self.creer_partie, bg="#010a0f", fg="#c4c4c4")
        self.btninscrirejoueur = Button(text="Inscrire joueur", font=("Arial", 12), state=DISABLED,
                                        command=self.inscrire_joueur, bg="#010a0f", fg="#c4c4c4")
        self.btnreset = Button(text="Reinitialiser partie", font=("Arial", 9), state=DISABLED,
                               command=self.reset_partie, bg="#010a0f", fg="#c4c4c4")

        # on place les autres boutons
        self.canevas_splash.create_window(420, 350, window=self.btncreerpartie, width=200, height=30)
        self.canevas_splash.create_window(420, 400, window=self.btninscrirejoueur, width=200, height=30)
        self.canevas_splash.create_window(420, 450, window=self.btnreset, width=200, height=30)

        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadre_splash
    #ON ARRIVE DANS FENETRE LOBBY -----------------------------------------------------
    ######## le lobby (où on attend les inscriptions)
    def creer_cadre_lobby(self):
        # le cadre lobby, pour isncription des autres joueurs, remplace le splash
        self.cadrelobby = Frame(self.cadre_app)
        self.canevaslobby = Canvas(self.cadrelobby, width=640, height=480, bg="#04273d")
        self.canevaslobby.pack()
        # widgets du lobby
        # un listbox pour afficher les joueurs inscrit pour la partie à lancer
        self.listelobby = Listbox(borderwidth=2, relief=GROOVE, fg="#c4c4c4", bg="#010a0f")

        # bouton pour lancer la partie, uniquement accessible à celui qui a creer la partie dans le splash
        self.btnlancerpartie = Button(text="Lancer partie", state=DISABLED, command=self.lancer_partie, fg="#c4c4c4", bg="#010a0f")
        # affichage des widgets dans le canevaslobby (similaire au splash)
        self.canevaslobby.create_window(440, 240, window=self.listelobby, width=200, height=400)
        self.canevaslobby.create_window(200, 400, window=self.btnlancerpartie, width=100, height=30)
        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadrelobby

    #FIN FENETRE LOBBY --------------------------------------------------------------------------

    #FENETRE DU JEU -----------------------------------------------------------------------------
    def creer_cadre_partie(self):
        self.ticks = IntVar() # Variable utilisé pour le temps (en secondes)
        self.cadrepartie = Frame(self.cadre_app, width=600, height=200, bg="yellow")
        self.cadrejeu = Frame(self.cadrepartie, width=600, height=200, bg="grey11")

        self.scrollX = Scrollbar(self.cadrejeu, orient=HORIZONTAL)
        self.scrollY = Scrollbar(self.cadrejeu, orient=VERTICAL)
        self.canevas = Canvas(self.cadrejeu, width=800, height=600,
                              xscrollcommand=self.scrollX.set,

                              yscrollcommand=self.scrollY.set, bg="grey11")

        #self.timer_partie = Label(self.cadrejeu, text="Temps écoulé: ", textvariable=self.ticks, width=10, height=1)


        self.scrollX.config(command=self.canevas.xview)
        self.scrollY.config(command=self.canevas.yview)

        self.scrollX.lower()
        self.scrollY.lower()

        self.canevas.grid(column=0, row=0, sticky=W + E + N + S)
        self.scrollX.grid(column=0, row=1, sticky=W + E)
        self.scrollY.grid(column=1, row=0, sticky=N + S)

        #self.timer_partie.grid(column=0, row=0, sticky=E + N, padx=20, pady=20)

        self.cadrejeu.columnconfigure(0, weight=1)
        self.cadrejeu.rowconfigure(0, weight=1)

        # SI JE CLICK DANS L'ESPACE OU SUR UNE ETOILE OU QUELQUONQUE OBJET DANS LE JEU
        self.canevas.bind("<Button>", self.cliquer_cosmos)
        self.canevas.tag_bind(ALL, "<Button>", self.cliquer_cosmos)

        # faire une multiselection
        self.canevas.bind("<Shift-Button-1>", self.debuter_multiselection)
        self.canevas.bind("<Shift-B1-Motion>", self.afficher_multiselection)
        self.canevas.bind("<Shift-ButtonRelease-1>", self.terminer_multiselection)

        # scroll avec roulette
        self.canevas.bind("<MouseWheel>", self.defiler_vertical)
        self.canevas.bind("<Control-MouseWheel>", self.defiler_horizon)

        self.creer_cadre_outils()

        self.cadrejeu.pack(side=LEFT, expand=1, fill=BOTH)
        return self.cadrepartie

    def creer_cadre_outils(self):

        self.cadreoutils = Frame(self.cadrepartie, width=200, height=200, bg="#3E363D")  #petite fenetre sur la gauche (celle juste au dessus de la mini map)->ici que l<on affiche le menu
        self.cadreoutils.pack(side=LEFT, fill=Y)

        self.cadre_option = Frame(self.cadrejeu, width=200, height=200, bg="#3E363D") # petite fenetre sur la droite / en construction

        self.cadreinfo = Frame(self.cadreoutils, width=200, height=200, bg="darkgrey")#??????????
        self.cadreinfo.pack(fill=BOTH)
        self.cadreinfogen = Frame(self.cadreinfo, width=200, height=200, bg="#3E363D")#petite fenetre en haut a gauche (JAJA et bouton MINI)
        self.cadreinfogen.pack(fill=BOTH)
        self.labid = Label(self.cadreinfogen, text="Inconnu", font=('Arial', 10))
        self.labid.bind("<Button>", self.centrer_planetemere)#bouton qui est utilise lorsque je clique sur JAJA, ca nous place sur notre planete mere
        self.labid.pack(side="left")
        self.btnmini = Button(self.cadreinfogen, text="MINI-MAP", foreground='#FCFCFC', background='#30292F', font=('Arial', 10))
        self.btnmini.bind("<Button>", self.afficher_mini)
        self.btnmini.pack(side="left")
        self.nbEtoilePossession = Label(self.cadreinfogen, foreground='#FCFCFC', background='#30292F', font=('Arial', 10))
        self.nbEtoilePossession.pack(side="left")

        # PETITE FENETRE POUR LES 2 BOUTONS VAISSEAU ET CARGO-----------------------------------------------------------------------------
        self.cadreinfochoix = Frame(self.cadreinfo, height=200, width=200, bg="light grey")
        """fenetre ou il y a bouton vaisseau, cargo et eclaireur"""



        #BOUTONS DU MENU

        #creer bouton resource

        self.btnRessources = Button(self.cadreinfochoix, text="Ressources",foreground='#FCFCFC', background='#30292F', font=('Arial', 12))
        self.btnRessources.config(command=self.menu_ressource_ex)
        self.btnRessources.pack(fill=X)

        # creer boutonInstallation ici--------------------------------------------------------------------------------------------
        self.btnInstallation = Button(self.cadreinfochoix, text="Installations",foreground='#FCFCFC', background='#30292F', font=('Arial', 12))
        """pour ouvrir le menu d'installation"""
        self.btnInstallation.config(command=self.menu_installation)
        self.btnInstallation.pack(fill=X)

        # creer bouton Inventaire ici
        self.btnInventaire = Button(self.cadreinfochoix, text="Inventaire",foreground='#FCFCFC', background='#30292F', font=('Arial', 12))
        """pour ouvrir le menu d'inventaire"""
        self.btnInventaire.config(command=self.menu_ressource)
        self.btnInventaire.pack(fill=X)

        self.boutonAmeliorerEtoile = Button(self.cadreinfochoix, text="Ameliorer Etoile",foreground='#FCFCFC', background='#B462C2', font=('Arial', 12))
        self.boutonAmeliorerEtoile.pack(fill=X)
        self.eteAfficher = False

        # ---------------------------------------------------------------------------------------------------------------------------------

        self.cadreinfoliste = Frame(self.cadreinfo)

        self.scroll_liste_Y = Scrollbar(self.cadreinfoliste, orient=VERTICAL)
        self.info_liste = Listbox(self.cadreinfoliste, width=20, height=6, yscrollcommand=self.scroll_liste_Y.set)
        self.info_liste.bind("<Button-1>", self.centrer_liste_objet)
        self.info_liste.bind("<Button-3>", self.centrer_liste_objet)
        self.info_liste.grid(column=0, row=0, sticky=W + E + N + S)
        self.scroll_liste_Y.grid(column=1, row=0, sticky=N + S)

        self.cadreinfoliste.columnconfigure(0, weight=1)
        self.cadreinfoliste.rowconfigure(0, weight=1)

        self.cadreinfoliste.pack(side=BOTTOM, expand=1, fill=BOTH)

        # IMAGE VAISSEAU-------------------------------------------------------------------
        s = Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground="red", background="red")

        self.cadreimage = Frame(self.cadreoutils, width=200, height=228, bg="black")
        self.barrevie = Progressbar(self.cadreoutils, orient=HORIZONTAL, length=100, mode="determinate", style="red.Horizontal.TProgressbar")

        # MINI MAP-----------------------------------------------------------------------
        self.cadreminimap = Frame(self.cadreoutils, height=200, width=200, bg="black")
        self.canevas_minimap = Canvas(self.cadreminimap, width=self.taille_minimap, height=self.taille_minimap,
                                      bg="#1e1e21")
        self.canevas_minimap.bind("<Button>", self.positionner_minicanevas)
        self.canevas_minimap.pack()
        self.cadreminimap.pack(side=BOTTOM)
        # FIN MINI MAP------------------------------------------------------

        self.cadres["jeu"] = self.cadrepartie
        # fonction qui affiche le nombre d'items sur le jeu
        self.canevas.bind("<Shift-Button-3>", self.calc_objets)

    def connecter_serveur(self):
        self.btninscrirejoueur.config(state=NORMAL)
        self.btncreerpartie.config(state=NORMAL)
        self.btnreset.config(state=NORMAL)
        url_serveur = self.urlsplash.get()
        self.parent.connecter_serveur(url_serveur)


    def timer_start(self,start_time,obj):
        """
        fonction qui demarre le timer
        :param start_time: le temps de depart
        """

        if obj == "entrepot":
            self.strName = "entrepot :"
            self.percentage_label = Label(self.cadreoutils, foreground='#FCFCFC', background='#30292F',
                                      font=('Arial', 12))
        elif obj == "usine":
            self.strName = "usine :"
            self.percentage_label = Label(self.cadreoutils, foreground='#FCFCFC', background='#30292F',
                                      font=('Arial', 12))
        elif obj == "vaisseau":
            self.strName = "vaisseau :"
            self.percentage_label = Label(self.cadreoutils, foreground='#FCFCFC', background='#30292F',
                                          font=('Arial', 12))
        self.objet = obj
        self.startTime = start_time
        self.started = True
        self.percentage_label.pack(fill=X)

    def timer_end(self):
        """
        fonction qui arrete le timer et le reinitalise
        """

        self.percentage_label.pack_forget()
        self.started = False
        self.strPourcentage = 0

        if self.objet == "entrepot":
            if self.nbr_entrepot == 0:
                self.nbr_entrepot += 1
                self.menu_installation()

        elif self.objet == "usine":
            if self.nbr_usine == 0:
                self.nbr_usine += 1
                self.menu_installation()
        elif self.objet == "vaisseau":
            self.menu_installation()

    def refresh(self,cadre):
        """
        fonction qui est appeler a chaque tick dans le main
        :param cadre: le temps actuel
        """

        tempC = cadre - self.startTime
        if(self.started == True and self.strPourcentage < 100):
            self.strPourcentage = int((tempC / self.parent.tempConstruction(self.objet)) * 100)
            self.percentage_label.config(text=self.strName + str(self.strPourcentage) + "%")

            print(self.strPourcentage)
            self.percentage_label.pack()

        elif self.strPourcentage == 100:
            self.timer_end()

    def refreshEtoile(self,mon_nom):
        """
        fonction qui retourn le nombre d'etoile que le joueur controle
        :param mon_nom: 
        :return:
        """
        nbEtoile = len(self.parent.recupJoueur(mon_nom).etoilescontrolees)
        self.nbEtoilePossession.config(text="Étoiles Contrôlées: " + str(nbEtoile))





    def forget_all(self):
        self.cadre_menu_ressource.pack_forget()
        self.cadre_menu_ressource_ex.pack_forget()
        self.cadre_menu_installation.pack_forget()
        self.cadre_bouton_construction_vaisseau.pack_forget()
        self.cadre_bouton_transferer.pack_forget()
        self.cadre_choisir_transfere.pack_forget()


    def menu_installation(self):#est appele quand je clique sur le bouton "Installation"
            self.recup = self.parent.recupEtoile(self.ma_selection[1])
            self.forget_all() #on oublie tout les cadres

            #on creer un cadre
            self.cadre_menu_installation = Frame(self.cadreoutils,height=200, width=200, bg="#DCE0D9")#on creer un cadre
            self.cadre_menu_installation.pack(side=LEFT, fill=Y)

            #on creer un label pour le titre
            self.cadre_label_titre = Frame(self.cadre_menu_installation, height=200, width=200,bg="#DCE0D9")
            self.cadre_label_titre.pack(fill=X)
            self.label_titre = Label(self.cadre_label_titre, text="Usine a Ressource", bg='#848484', font=('Arial', 13), foreground="white")
            self.label_titre.pack(fill=X)

            #on creer un cadre pour l'image
            self.cadre_img = Frame(self.cadre_menu_installation, height=200, width=200,bg="#DCE0D9")#cadre pour image
            self.cadre_img.pack(fill=X)
            self.label_img = Label(self.cadre_img, image=self.images["usine"],bg="#DCE0D9")#image de lusine
            self.label_img.pack(side=LEFT)
            self.label_installation = Label(self.cadre_img, text="Description: usine pour stocker ressources",bg="#DCE0D9")#label pour afficher "Description..."
            self.label_installation.pack()


            #Bouton pour construire usine
            self.cadre_bouton = Frame(self.cadre_menu_installation, height=200, width=200, bg="#DCE0D9")#cadre bouton pour mettre bouton construire usine
            self.cadre_bouton.pack(fill=X)

            self.boutonConstruireUsine = Button(self.cadre_bouton, text="Construire Usine",foreground='#F5E15D', background='#242423', font=('Arial', 12))
            self.boutonConstruireUsine.config(command=self.construire_usine)

            self.boutonAmeliorerUsine = Button(self.cadre_bouton, text="Améliorer Usine",foreground='#CB92CE', background='#242423', font=('Arial', 12))

            if self.recup.installations.get("usine") is None:
                self.boutonConstruireUsine.pack(fill=X)
            else:
                self.boutonConstruireUsine.pack_forget()
                self.boutonAmeliorerUsine.pack(fill=X)


            #cadre pour creer un espace entre Usine Ressource et Entrepot a vaisseau
            self.cadre_espacement = Frame(self.cadre_menu_installation, height=10, width=200, bg="#FFFFFF")# cadre pour creer un espace entre Usine Ressource et Entrepot a vaisseau
            self.cadre_espacement.pack(fill=X)
                     # partie basse

            # a utiliser pour chosir le menu si je construit un entrepot ou pas-----------
            recupEtoile = self.parent.recupEtoile(self.ma_selection[1]) #on recup ce quil ya dans etoile selectionne -> une des var cest celle qui a les installation presente sur etoile

            # Afficher le cout de l'entrepot
            self.afficher_cout = ""
            self.afficher_possession = ""
            if self.recup.installations.get("entrepot") is not None:
                # recuprer données de l'instlalation
                key = self.recup.installations.get("entrepot").cout.keys()
                for ke in key:
                    if self.recup.installations.get("entrepot").cout.get(ke) > 0:
                        self.afficher_cout += ke + " : " + str(self.recup.installations.get("entrepot").cout.get(ke)) + "  "
                        self.afficher_possession += ke + " : " + str(self.recup.inventaire.get(ke)) + "  "
            else:
                i = Installation(None, None, "entrepot", 30)
                keys = i.cout.keys()
                for k in keys:
                    if i.cout.get(k) > 0:
                        self.afficher_cout += k + " : " + str(i.cout.get(k)) + "  "
                        self.afficher_possession += k + " : " + str(self.recup.inventaire.get(k)) + "  "


            #Cadre et Label Entrepot a vaisseaux
            self.cadre_label_entrepot_vaisseau = Frame(self.cadre_menu_installation, height=200, width=200, bg="#848484")#cadre pour partie entrepot
            self.cadre_label_entrepot_vaisseau.pack(fill=X)
            self.label_entrepotVaisseau = Label(self.cadre_label_entrepot_vaisseau, text="Entrepot a vaisseaux",bg="#848484",font=('Arial', 13),foreground='white')
            self.label_entrepotVaisseau.pack(fill=X)

            #Cadre et Label entrepot
            self.cadre_img2 = Frame(self.cadre_menu_installation, height=200, width=200,background="#DCE0D9")#dans cadre img2 je met image + descritpion
            self.cadre_img2.pack(fill=X)
            self.label_img2 = Label(self.cadre_img2, image=self.images["entrepot"],bg="#DCE0D9")
            self.label_img2.pack(side=LEFT)
            self.label_installation2 = Label(self.cadre_img2, text="Description: Entrepot pour construire vaisseaux",bg="#DCE0D9")
            self.label_installation2.pack()


            #pour bouton construction entrepot

            self.cadre_bouton_construction_entrepot = Frame(self.cadre_menu_installation, height=200, width=200)
            self.cadre_bouton_construction_entrepot.pack(fill=X)
            self.boutonConstruireEntrepot = Button(self.cadre_bouton_construction_entrepot, text="Construire Entrepot", foreground='#F5E15D',
                                                   background='#242423', font=('Arial', 12))
            self.boutonConstruireEntrepot.config(command=self.construire_entrepot)

            self.boutonAmeliorerEntrepot = Button(self.cadre_bouton_construction_entrepot, text="Ameliorer Entrepot", foreground='#CB92CE',
                                                  background='#242423', font=('Arial', 12))

            self.cadre_nbr_installation_entrepot_present = Frame(self.cadre_menu_installation, height=200, width=200)#cadre
            self.cadre_nbr_installation_entrepot_present.pack(fill=X)

            if recupEtoile.installations.get("entrepot") is not None: #si il y a un entrepot
                self.nbr_entrepot = 1
            else:
                self.nbr_entrepot = 0
            self.label_titre_nbr_installation_entrepot_present = Label(self.cadre_nbr_installation_entrepot_present, text=" Nbr Entrepot prensent sur Etoile: " + (str) (self.nbr_entrepot) +"/ 1")
            print("nbr entrepot: " + (str)(self.nbr_entrepot))

            self.label_titre_nbr_installation_entrepot_present.pack(side=TOP)

            self.cadre_ressouce_demande = Frame(self.cadre_menu_installation, height= 200, width=200,bg="#DCE0D9")
            self.cadre_ressouce_demande.pack(fill=X)

            self.label_ressource_demande = Label(self.cadre_ressouce_demande,text="Ressource demande: " + self.afficher_cout,bg="#DCE0D9")
            self.label_ressource_demande.pack()

            self.cadre_ressource_que_possede_joueur = Frame(self.cadre_menu_installation, height=200,width=200,bg="#DCE0D9")
            self.cadre_ressource_que_possede_joueur.pack(fill=X)

            self.label_ressource_possede_joueur = Label(self.cadre_ressource_que_possede_joueur, text="Ressource en possession: " + self.afficher_possession,bg="#DCE0D9")
            self.label_ressource_possede_joueur.pack()

            if recupEtoile.installations.get("entrepot") is not None:  # si il y a un entrepot on affiche pas le bouton construire Entrepot
                print("il y a un entrepot")


                self.boutonConstruireEntrepot = Button(self.cadre_bouton_construction_entrepot, text="Construire Entrepot",
                                                       foreground='#F5E15D', background='#242423', font=('Arial', 12))
                self.boutonConstruireEntrepot.config(command=self.construire_entrepot)
                self.boutonAmeliorerEntrepot = Button(self.cadre_bouton_construction_entrepot, text="Ameliorer Entrepot",
                                                      foreground='#CB92CE', background='#242423', font=('Arial', 12))
                self.boutonConstruireEntrepot.pack(fill=X)

                # afficher menu creation vaisseau (entrepot existe)

                self.boutonConstruireEntrepot.pack_forget()
                self.boutonAmeliorerEntrepot.pack(side=LEFT)
                self.boutonConstruireVaisseau = Button(self.cadre_bouton_construction_entrepot, text="Construire Vaisseau",
                                                       foreground='#A7FCC2', background='#242423', font=('Arial', 12))
                self.boutonConstruireVaisseau.config(command=self.construction_vaisseau)
                self.boutonConstruireVaisseau.pack(side=RIGHT)

            else:  # si il ny a pas dentrepot affiche le bouton construire entrepot
                # afficher menu creation entrepot (entrepot existe pas)
                self.boutonConstruireEntrepot.pack(fill=X)





    def construction_vaisseau(self):# on arrive ici quand on clique sur le bouton "construire Vaisseau"
        #on affiche les boutons
        self.cadre_menu_installation.pack_forget()

        self.cadre_bouton_construction_vaisseau = Frame(self.cadreoutils,height=200,width=200,bg="yellow")
        self.cadre_bouton_construction_vaisseau.pack()

        self.btncreervaisseau = Button(self.cadre_bouton_construction_vaisseau, text="Attack",
                                                       foreground='#A7FCC2', background='#242423', font=('Arial', 12))
        """pour creer un vaisseau"""
        self.btncreervaisseau.bind("<Button>", self.creer_vaisseau)

        self.btncreercargo = Button(self.cadre_bouton_construction_vaisseau, text="Cargo",
                                                       foreground='#A7FCC2', background='#242423', font=('Arial', 12))
        """pour creer un cargo"""
        self.btncreercargo.bind("<Button>", self.creer_vaisseau)

        self.btncreereclaireur = Button(self.cadre_bouton_construction_vaisseau, text="Eclaireur",
                                                       foreground='#A7FCC2', background='#242423', font=('Arial', 12))
        """pour creer un éclaireur"""
        self.btncreereclaireur.bind("<Button>", self.creer_vaisseau)
        self.btncreervaisseau.pack(fill=X)
        self.btncreercargo.pack(fill=X)
        self.btncreereclaireur.pack(fill=X)

    def afficherNotification(self, notification):


        if notification is not None:
            self.cadre_notification = Frame(self.cadrejeu, bg=None)
            self.label_notification = Label(self.cadre_notification, bg="#606060", fg="#c4c4c4")
            #afficher n pendant un délaie de 5 secondes
            self.label_notification.config(text=notification)
            #retier n de la liste

        self.cadre_notification.grid(column=0, row=0, sticky=E + N, padx=10, pady=10)
        self.label_notification.pack()


    def menu_ressource(self):# on arrive ici quand on clique sur le bouton "Inventaire" -> inventaire de ce que possede le joueur
        #raffraichir valeur self.recup.inventaire.get("Fer)

            self.recup = self.parent.recupEtoile(self.ma_selection[1])
            self.forget_all()


            self.cadre_menu_ressource = Frame(self.cadreoutils, height=200, width=200, bg="#6F6D6D")
            self.cadre_menu_ressource.pack(fill=X)
            self.a_clique_sur_installation = 0
            #mettre tout ici
            self.label_fer = Label(self.cadre_menu_ressource, text="Fer : " + str(self.recup.inventaire.get("Fer")), anchor=CENTER, width=25, height=2, border=2, borderwidth=1,
                                  relief="solid", bg="green")

            #
            self.label_cuivre = Label(self.cadre_menu_ressource, text="Cuivre : " + str(self.recup.inventaire.get("Cuivre")), anchor=CENTER, width=25, height=2, border=2,
                                               borderwidth=1,
                                              relief="solid", bg="green")
            self.label_or = Label(self.cadre_menu_ressource, text="Or : " + str(self.recup.inventaire.get("Or")), anchor=CENTER, width=25, height=2, border=2,
                                           borderwidth=1,
                                           relief="solid", bg="yellow")
            #
            self.label_titane = Label(self.cadre_menu_ressource, text="Titane : " + str(self.recup.inventaire.get("Titane")), anchor=CENTER, width=25, height=2, border=2,
                                               borderwidth=1,
                                               relief="solid", bg="red")
            #
            self.label_hydrogene = Label(self.cadre_menu_ressource, text="Hydrogene : " + str(self.recup.inventaire.get("Hydrogene")), anchor=CENTER, width=25, height=2, border=2,
                                        borderwidth=1, relief="solid", bg="green")
            #
            self.label_pluto = Label(self.cadre_menu_ressource, text="Plutonium : " + str(self.recup.inventaire.get("Plutonium")), anchor=CENTER, width=25, height=2, border=2,
                                       borderwidth=1, relief="solid", bg="yellow")
            #
            self.label_antimatiere = Label(self.cadre_menu_ressource, text="???? : " + str(self.recup.inventaire.get("Antimatiere")), anchor=CENTER, width=25, height=2, border=2,
                                                   borderwidth=1,
                                                   relief="solid", bg="purple")

            self.label_fer.pack(fill=X)
            self.label_cuivre.pack(fill=X)
            self.label_or.pack(fill=X)
            self.label_titane.pack(fill=X)
            self.label_hydrogene.pack(fill=X)
            self.label_pluto.pack(fill=X)
            self.label_antimatiere.pack(fill=X)
            #self.raffraichir(self.cadre_menu_ressource)





    def menu_ressource_ex(self):#Ressource de letoile
        self.recup = self.parent.recupEtoile(self.ma_selection[1])
        self.forget_all()

        self.cadre_menu_ressource_ex = Frame(self.cadreoutils, height=200, width=100, bg="#6F6D6D")
        self.cadre_menu_ressource_ex.pack(fill=BOTH)
        self.a_clique_sur_installation = 0

        self.label_materiaux_e = Label(self.cadre_menu_ressource_ex, text="Matériaux :", anchor=CENTER,width=34, height=1, border=1, borderwidth=1,relief="solid", bg="#e0e0e0")
        self.label_ernegie_e = Label(self.cadre_menu_ressource_ex, text="Énergie : ", anchor=CENTER,width=34, height=1, border=1, borderwidth=1,relief="solid", bg="#e0e0e0")

        self.label_fer_e = Label(self.cadre_menu_ressource_ex, text="Fer : " + str(round(self.recup.ressource.get("Fer") * 100, 2)) + "%", anchor=CENTER,
                             width=34, height=2, border=2, borderwidth=1,
                             relief="solid", bg="#949392")

        self.label_cuivre_e = Label(self.cadre_menu_ressource_ex, text="Cuivre : " + str(round(self.recup.ressource.get("Cuivre") * 100, 2)) + "%",
                                  anchor=CENTER, width=34, height=2, border=2,
                                  borderwidth=1,
                                  relief="solid", bg="#703f0a")

        self.label_or_e = Label(self.cadre_menu_ressource_ex, text="Or : " + str(round(self.recup.ressource.get("Or") * 100, 2)) + "%", anchor=CENTER,
                              width=34, height=2, border=2,
                              borderwidth=1,
                              relief="solid", bg="#9c7f00")

        self.label_titane_e = Label(self.cadre_menu_ressource_ex, text="Titane : " + str(round(self.recup.ressource.get("Titane") * 100, 2)) + "%",
                                  anchor=CENTER, width=34, height=2, border=2,
                                  borderwidth=1,
                                  relief="solid", bg="#5668a3")

        self.label_hydrogene_e = Label(self.cadre_menu_ressource_ex,
                                     text="Hydrogene : " + str(round(self.recup.ressource.get("Hydrogene") * 100, 2)) + "%", anchor=CENTER,
                                     width=34, height=2, border=2,
                                     borderwidth=1, relief="solid", bg="#b4e7ed")

        self.label_pluto_e = Label(self.cadre_menu_ressource_ex, text="Plutonium : " + str(round(self.recup.ressource.get("Plutonium") * 100, 2)) + "%",
                                 anchor=CENTER, width=34, height=2, border=2,
                                 borderwidth=1, relief="solid", bg="#558a0c")

        self.label_antimatiere_e = Label(self.cadre_menu_ressource_ex, text="Antimatière : " + str(round(self.recup.ressource.get("Antimatiere") * 100, 2)) + "%",
                                       anchor=CENTER, width=34, height=2, border=2,
                                       borderwidth=1,
                                       relief="solid", bg="#3c0c8a")

        self.label_materiaux_e.pack(fill=X)
        self.label_fer_e.pack(fill=X)
        self.label_cuivre_e.pack(fill=X)
        self.label_or_e.pack(fill=X)
        self.label_titane_e.pack(fill=X)
        self.label_ernegie_e.pack(fill=X)
        self.label_hydrogene_e.pack(fill=X)
        self.label_pluto_e.pack(fill=X)
        self.label_antimatiere_e.pack(fill=X)

    def construire_entrepot(self):#on arrive ici quand on clique sur le bouton "Construire Entrepot"
        self.cadre_menu_installation.pack_forget()
        self.parent.construireInstallation("entrepot", self.ma_selection[1]) #pour construire entrepot -> la fonction va veifier si on peut construire entrepot
        self.laConstruction = "entrepot"
        #self.timer_start(self.parent.cadrejeu,"entrepot") #on lance le timer pour construire entrepot

    def construire_usine(self):# on arrive ici quand on clique sur bouton construire_usine
        self.cadre_menu_installation.pack_forget()
        self.parent.construireInstallation("usine", self.ma_selection[1])
        self.laConstruction = "usine"
        #self.timer_start(self.parent.cadrejeu,"usine")




    def centrer_liste_objet(self, evt):
        info = self.info_liste.get(self.info_liste.curselection())
        print(info)
        liste_separee = info.split(";")
        type_vaisseau = liste_separee[0]
        id = liste_separee[1][1:]
        obj = self.modele.joueurs[self.mon_nom].flotte[type_vaisseau][id]
        self.centrer_objet(obj)

    def calc_objets(self, evt):
        print("Univers = ", len(self.canevas.find_all()))

    def defiler_vertical(self, evt):
        rep = self.scrollY.get()[0]
        if evt.delta < 0:
            rep = rep + 0.01
        else:
            rep = rep - 0.01
        self.canevas.yview_moveto(rep)

    def defiler_horizon(self, evt):
        rep = self.scrollX.get()[0]
        if evt.delta < 0:
            rep = rep + 0.02
        else:
            rep = rep - 0.02
        self.canevas.xview_moveto(rep)

    ##### FONCTIONS DU SPLASH #########################################################################

    ###  FONCTIONS POUR SPLASH ET LOBBY INSCRIPTION pour participer a une partie
    def update_splash(self, etat):
        if "attente" in etat or "courante" in etat:
            self.btncreerpartie.config(state=DISABLED)
        if "courante" in etat:
            self.etatdujeu.config(text="Desole - partie encours !")
            self.btninscrirejoueur.config(state=DISABLED)
        elif "attente" in etat:
            self.etatdujeu.config(text="Partie en attente de joueurs !")
            self.btninscrirejoueur.config(state=NORMAL)
        elif "dispo" in etat:
            self.etatdujeu.config(text="Bienvenue ! Serveur disponible")
            self.btninscrirejoueur.config(state=DISABLED)
            self.btncreerpartie.config(state=NORMAL)
        else:
            self.etatdujeu.config(text="ERREUR - un probleme est survenu")

    def reset_partie(self):
        rep = self.parent.reset_partie()


    def creer_partie(self):
        nom = self.nomsplash.get()
        self.parent.creer_partie(nom)

    ##### FONCTION DU LOBBY #############
    def update_lobby(self, dico):
        self.listelobby.delete(0, END)
        for i in dico:
            self.listelobby.insert(END, i[0])
        if self.parent.joueur_createur:
            self.btnlancerpartie.config(state=NORMAL)

    def inscrire_joueur(self):
        nom = self.nomsplash.get()
        urljeu = self.urlsplash.get()
        self.parent.inscrire_joueur(nom, urljeu)

    def lancer_partie(self):
        self.parent.lancer_partie()

    def initialiser_avec_modele(self, modele):
        self.mon_nom = self.parent.mon_nom
        self.modele = modele
        self.canevas.config(scrollregion=(0, 0, modele.largeur, modele.hauteur))

        self.labid.config(text=self.mon_nom)
        self.labid.config(fg=self.modele.joueurs[self.mon_nom].couleur)

        self.afficher_decor(modele)

    ####################################################################################################

    def positionner_minicanevas(self, evt):
        x = evt.x
        y = evt.y

        pctx = x / self.taille_minimap
        pcty = y / self.taille_minimap

        xl = (self.canevas.winfo_width() / 2) / self.modele.largeur
        yl = (self.canevas.winfo_height() / 2) / self.modele.hauteur

        self.canevas.xview_moveto(pctx - xl)
        self.canevas.yview_moveto(pcty - yl)
        xl = self.canevas.winfo_width()
        yl = self.canevas.winfo_height()

    def afficher_decor(self, mod):
        # on cree un arriere fond de petites etoiles NPC pour le look
        for i in range(len(mod.etoiles) * 50):
            x = random.randrange(int(mod.largeur))
            y = random.randrange(int(mod.hauteur))
            n = random.randrange(3) + 1
            col = random.choice(["LightYellow", "azure1", "pink"])
            self.canevas.create_oval(x, y, x + n, y + n, fill=col, tags=("fond",))
        # affichage des etoiles
        for i in mod.etoiles:
            t = i.taille * self.zoom
            self.canevas.create_image(i.x, i.y,image= self.images["Starwhite"],
                                     tags=(i.proprietaire, str(i.id), "Etoile", i.x, i.y))
        # affichage des etoiles possedees par les joueurs
        for i in mod.joueurs.keys():
            for j in mod.joueurs[i].etoilescontrolees:
                t = j.taille * self.zoom
                self.canevas.create_image(j.x, j.y, image = self.images["Star" + mod.joueurs[i].couleur],
                                         tags=(j.proprietaire, str(j.id), "Etoile", j.x, j.y))
                # on affiche dans minimap
                minix = j.x / self.modele.largeur * self.taille_minimap
                miniy = j.y / self.modele.hauteur * self.taille_minimap
                self.canevas_minimap.create_rectangle(minix, miniy, minix + 3, miniy + 3,
                                                      fill=mod.joueurs[i].couleur,
                                                      tags=(j.proprietaire, str(j.id), "Etoile"))

    def afficher_mini(self, evt):  # univers(self, mod):
        self.canevas_minimap.delete("mini")
        for j in self.modele.etoiles:
            minix = j.x / self.modele.largeur * self.taille_minimap
            miniy = j.y / self.modele.hauteur * self.taille_minimap
            self.canevas_minimap.create_rectangle(minix, miniy, minix + 0, miniy + 0,
                                                  fill="black",
                                                  tags=("mini", "Etoile"))
        # # affichage des etoiles possedees par les joueurs
        # for i in mod.joueurs.keys():
        #     for j in mod.joueurs[i].etoilescontrolees:
        #         t = j.taille * self.zoom
        #         self.canevas.create_oval(j.x - t, j.y - t, j.x + t, j.y + t,
        #                                  fill=mod.joueurs[i].couleur,
        #                                  tags=(j.proprietaire, str(j.id),  "Etoile"))

    def centrer_planetemere(self, evt):#pour centre etoile pricincipal du joueur
        self.centrer_objet(self.modele.joueurs[self.mon_nom].etoilemere)

    def centrer_objet(self, objet):
        # permet de defiler l'écran jusqu'à cet objet
        x = objet.x
        y = objet.y

        x1 = self.canevas.winfo_width() / 2
        y1 = self.canevas.winfo_height() / 2

        pctx = (x - x1) / self.modele.largeur
        pcty = (y - y1) / self.modele.hauteur

        self.canevas.xview_moveto(pctx)
        self.canevas.yview_moveto(pcty)

    def afficher_info_vaisseau(self, objet):
        self.clickUneFoisSurRessource = 0
        self.clickUneFoisSurVaiss += 1
        self.clickUneFoisSurInsta = 0
        print("Efface")

        if self.clickUneFoisSurVaiss == 1:
            self.boutonConstruireUsine.pack_forget()
            self.label_titre.pack_forget()
            self.label_installation.pack_forget()
            self.label_entrepotVaisseau.pack_forget()
            self.boutonAmeliorerEtoile.pack_forget()
            self.boutonConstruireEntrepot.pack_forget()
            self.label_or.pack_forget()
            self.label_cuivre.pack_forget()
            self.label_antimatiere.pack_forget()
            self.label_pluto.pack_forget()
            self.label_titane.pack_forget()
            self.label_fer.pack_forget()
            self.label_hydrogene.pack_forget()
            self.btnInstallation.pack_forget()
            self.btnInventaire.pack_forget()



        self.barrevie.value = objet.Vie

        self.cadreinfoimage.pack(fill=BOTH)  # Debug, à remplacer par une image plus tard
        self.barrevie.pack(fill=BOTH)

        # change l'appartenance d'une etoile et donc les propriétés des dessins les représentants
    def afficher_etoile(self, joueur, cible):
        joueur1 = self.modele.joueurs[joueur]
        id = cible.id
        couleur = joueur1.couleur
        self.canevas.itemconfig(id, image= self.images["Star" + couleur])
        self.canevas.itemconfig(id, tags=(joueur, id, "Etoile", cible.x, cible.y))

    # ajuster la liste des vaisseaux
    def lister_objet(self, obj, id, niveau):
        self.info_liste.insert(END, obj + "; " + id + "; Nv." + str(niveau))

    def creer_vaisseau(self, evt):
        self.forget_all()
        type_vaisseau = evt.widget.cget("text")
        self.parent.creer_vaisseau(type_vaisseau, int(self.selectedTags[3]) + random.choice([i for i in range(-30, 30) if i not in [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]), int(self.selectedTags[4]) + random.choice([i for i in range(-30, 30) if i not in [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]), self.ma_selection[1])
        self.canevas.delete("marqueur")
        self.timer_start(self.parent.cadrejeu,"vaisseau")




    def afficher_jeu(self):#LA ON AFFICHE BEAUCOUP DE CHOSE!!!:)-------------------------------------------------------------
        mod = self.modele
        self.canevas.delete("artefact")
        self.canevas.delete("objet_spatial")
        self.canevas.delete("marqueur")
        self.listeVaisseau = []

        if self.ma_selection != None:  # SI JE NE SELECTIONNE RIEN
            joueur = mod.joueurs[self.ma_selection[0]]  # joueurs[] liste des nom des joueurs
            if self.ma_selection[2] == "Etoile":
                for i in joueur.etoilescontrolees:
                    if i.id == self.ma_selection[1]:
                        x = i.x
                        y = i.y
                        t = 10 * self.zoom
                        self.canevas.create_oval(x - t, y - t, x + t, y + t,
                                                 dash=(2, 2), outline=mod.joueurs[self.mon_nom].couleur,
                                                 tags=("multiselection", "marqueur"))  # fonction dans pyCharme
            elif self.ma_selection[2] == "Flotte":
                for j in joueur.flotte:
                    for i in joueur.flotte[j]:
                        i = joueur.flotte[j][i]
                        if i.id == self.ma_selection[1]:
                            x = i.x
                            y = i.y
                            t = 10 * self.zoom
                            self.canevas.create_rectangle(x - t, y - t, x + t, y + t,
                                                          dash=(2, 2), outline=mod.joueurs[self.mon_nom].couleur,
                                                          tags=("multiselection", "marqueur"))
        # afficher asset (LES RESSOURCES QU'A LE JOUEUR) des joueurs
        for i in mod.joueurs.keys():
            i = mod.joueurs[i]
            for k in i.flotte:
                for j in i.flotte[k]:
                    j = i.flotte[k][j]
                    recupCouleur = self.parent.recupJoueur(j.proprietaire)
                    if k == "Attack":  # CREATION DU CARRE ROUGE REPRESENTANT LE VAISSEAU

                        self.canevas.create_image(j.x, j.y, image= self.images["Atck"+ recupCouleur.couleur],
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact", "True"))
                    elif k == "Cargo":  # CREATION DU CARGO
                        x = self.canevas.create_image(j.x, j.y, image=self.images["cargo"],
                                                      tags=(
                                                      j.proprietaire, str(j.id), "Flotte", k, "artefact", "False"))
                        self.listeVaisseau.append(x)

                    elif k == "Eclaireur": #CREATION DE L'ÉCLAIREUR
                        x = self.canevas.create_image(j.x, j.y, image=self.images["Spy" + recupCouleur.couleur],
                                                      tags=(
                                                      j.proprietaire, str(j.id), "Flotte", k, "artefact", "True"))
                        self.listeVaisseau.append(x)
        for t in self.modele.trou_de_vers:
            i = t.porte_a
            for i in [t.porte_a, t.porte_b]:
                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

        self.ticks.set(value=self.parent.to_secondes(self.parent.cadrejeu))

    def dessiner_cargo(self, obj, tailleF, joueur, type_obj):
        t = obj.taille * self.zoom
        a = obj.ang
        x, y = hlp.getAngledPoint(obj.angle_cible, int(t / 4 * 3), obj.x, obj.y)
        dt = t / 2
        self.canevas.create_oval((obj.x - tailleF), (obj.y - tailleF),
                                 (obj.x + tailleF), (obj.y + tailleF), fill=joueur.couleur,
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))
        self.canevas.create_oval((x - dt), (y - dt),
                                 (x + dt), (y + dt), fill="yellow",
                                 tags=(obj.proprietaire, str(obj.id), "Flotte", type_obj, "artefact"))

    def dessiner_cargo1(self, j, tailleF, i, k):
        self.canevas.create_oval((j.x - tailleF), (j.y - tailleF),
                                 (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                                 tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))

    def supprimer_vaisseau(self, id):
        print(id)
        print(self.canevas.gettags(id))
        self.canevas.delete(id)



    def cliquer_cosmos(self, evt):  # DES QU'ON CLIQUE QUELQUE PART DANS LE JEU -> travailler avec ca
        self.selectedTags = self.canevas.gettags(CURRENT)
        tags = self.selectedTags #contient
        if tags:  # Il y a des tags => On a cliqué sur un objet de la carte (Vaisseau, Étoile, ...)

            if tags[0] == self.mon_nom:#si je clique sur quelque chose qui mappartient
                self.ma_selection = [self.mon_nom, tags[1], tags[2]]
                if tags[2] == "Etoile":
                    self.montrer_etoile_selection()
                    print("nom de letoile = " + tags[1])
                    self.etoileSelectionne = tags[1]
                    if (self.cargoArrive):  # si il est accoste
                        # avoir id de letoile ou il est accoste
                        self.etoileOuEstPoseLeCargo = tags[1]
                        print("etoile selectionne = " + self.etoileSelectionne + "  Idetoile ou est pose le cargot : " + self.etoileOuEstPoseLeCargo)

                    elif (self.estAccos == False):
                        self.cadre_bouton_transferer.pack_forget()

                    #enlenver menu transferer pour vaisseau cargo
                    self.cadre_choisir_transfere.pack_forget()
                    #pour transferer, on fait apparaitre le bouton transferer quand le cargot arrive sur l'etoile. On doit cliquer sur l'etoile pour voir le bouton
                    # affiche le bouton transferer
                    if (self.etoileSelectionne != self.etoileOuEstPoseLeCargo):
                        print("est rentre!!!")
                        self.faireApparaitreBoutonTransfere()

                    elif (self.etoileSelectionne == self.etoileOuEstPoseLeCargo):
                        print("enleve le bouton")
                        self.cadre_bouton_transferer.pack_forget()

                    if self.shipSelected != []: #TOUT LES VAISSEAUX SELECTIONNE
                        for ship in self.shipSelected:
                            self.parent.cibler_flotte(ship[1], tags[1], tags[2])#cest ca qui envoi le vaisseau a letoile selectionne
                        self.shipSelected = []
                        self.ma_selection = []
                    else:
                        self.montrer_etoile_selection()

                elif tags[2] == "Flotte": #quand je clique sur un vaisseau
                    self.montrer_flotte_selection()
                    self.type_vaisseau_selectionne = tags[3] #je recupere le type de vaisseau selectionne
                    print("Type vaisseau = " + self.type_vaisseau_selectionne)

                    if self.type_vaisseau_selectionne == "Cargo":
                        self.idCargo = tags[1]


                    self.cadreinfochoix.pack_forget()# on enleve le menu du haut ici quand on clique sur le vaisseau car on ne veut plus savoir ce quil y a sur l'étoile
                    self.cadre_bouton_transferer.pack_forget()#on enleve le bouton transferer
                    self.cadre_menu_ressource.pack_forget()#on enleve le menu de linventaire
                    self.cadre_menu_ressource_ex.pack_forget()
                    self.forget_all()
                    #si je clique sur le cargot
                    # if(self.type_vaisseau_selectionne == "Cargo"):
                    #     if(self.cargoArrive):#si il est accoste
                    #         #avoir id de letoile ou il est accoste
                    #         self.etoileOuEstPoseLeCargo = tags[1]
                            # print("Val CargoEstAccoste : " + str(self.cargoArrive))
                            # print("Cargot est accoste sur letoile : " + self.etoileOuEstPoseLeCargo)



                        # elif(self.estAccos == False):#mais quand il reaprt il ne repasse pas a False seul..
                        #     self.cadre_bouton_transferer.pack_forget()

                    self.shipSelected.append(tags)
            elif ("Etoile" == tags[2] or "Porte_de_ver" == tags[2]) and self.shipSelected != []:
                for ship in self.shipSelected:
                    if "Etoile" == tags[2] and ship[5] == "True":
                        if ("neutre" == tags[0] and ship[3] == "Eclaireur") or (not "neutre" == tags[0] and ship[3] == "Attack"):
                            self.parent.cibler_flotte(ship[1], tags[1], tags[2])
                            self.shipSelected = []
                    elif "Porte_de_ver" == tags[2]:
                        self.parent.cibler_flotte(ship[1], tags[1], tags[2])
                        self.shipSelected = []
                    self.ma_selection = None

        else:  # aucun tag => On a clické dans le vide donc aucun objet sur la carte
            print("Region inconnue")
            self.forget_all()
            self.ma_selection = None

    def montrer_etoile_selection(self):  # montrer le tag de letoile selectionne
        self.cadre_bouton_transferer.pack_forget() #jenleve le bouton transferer si il est present
        self.btnInventaire.pack()
        self.btnInstallation.pack()
        self.cadreinfochoix.pack(fill=BOTH)

    def montrer_flotte_selection(self):  # montrer le tag du vaisseau selectionne
        #print("À IMPLANTER - FLOTTE de ", self.mon_nom)

        print("vaisseau selectionne")


    # Methodes pour multiselect#########################################################
    def debuter_multiselection(self, evt):
        self.debutselect = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
        x1, y1 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
        self.selecteur_actif = self.canevas.create_rectangle(x1, y1, x1 + 1, y1 + 1, outline=self.modele.joueurs[self.mon_nom].couleur, width=2,
                                                             dash=(2, 2), tags=("", "selecteur", "", ""))

    def afficher_multiselection(self, evt):
        if self.debutselect:
            x1, y1 = self.debutselect
            x2, y2 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.canevas.coords(self.selecteur_actif, x1, y1, x2, y2)

    def terminer_multiselection(self, evt):
        if self.debutselect:
            x1, y1 = self.debutselect
            x2, y2 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.debutselect = []
            objchoisi = (list(self.canevas.find_enclosed(x1, y1, x2, y2)))
            for i in objchoisi:
                if self.canevas.gettags(i)[0] == self.mon_nom and self.canevas.gettags(i)[2] == "Flotte":
                    self.shipSelected.append(self.canevas.gettags(i))

            self.canevas.delete("selecteur")

    ### FIN du multiselect
