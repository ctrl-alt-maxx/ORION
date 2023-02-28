# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

from tkinter import *
from tkinter.ttk import *
from tkinter.simpledialog import *
from tkinter.messagebox import *
from helper import Helper as hlp
import math
from PIL import Image

import random

#ffff
class Vue():
    def __init__(self, parent, urlserveur, mon_nom, msg_initial):
        self.parent = parent
        self.root = Tk()
        self.root.title("Je suis " + mon_nom)
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
        self.shipSelected = ""

        #cree un bouton global que lon va pouvoir reutiliser
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

        self.boutonConstruire = Button()
        self.label_entrepotVaisseau = Label()
        self.boutonConstruireEntrepot = Button()

        self.label_qte_fer = Label()


        self.clickUneFoisSurInsta = 0 #pour que le frame ne reaparaisse pas si je clique 2 fois de suite sur le meme bouton
        self.clickUneFoisSurRessource = 0
        self.clickUneFoisSurVaiss = 0

        self.selectedTags = None

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
        self.canevas_splash = Canvas(self.cadre_splash, width=600, height=480, bg="pink")
        self.canevas_splash.pack()

        # creation ds divers widgets (champ de texte 'Entry' et boutons cliquables (Button)
        self.etatdujeu = Label(text=msg_initial, font=("Arial", 18), borderwidth=2, relief=RIDGE)
        self.nomsplash = Entry(font=("Arial", 14))
        self.urlsplash = Entry(font=("Arial", 14), width=42)
        self.btnurlconnect = Button(text="Connecter", font=("Arial", 12), command=self.connecter_serveur)
        # on insère les infos par défaut (nom url) et reçu au démarrage (dispo)
        self.nomsplash.insert(0, mon_nom)
        self.urlsplash.insert(0, urlserveur)
        # on les place sur le canevas_splash
        self.canevas_splash.create_window(320, 100, window=self.etatdujeu, width=400, height=30)
        self.canevas_splash.create_window(320, 200, window=self.nomsplash, width=400, height=30)
        self.canevas_splash.create_window(210, 250, window=self.urlsplash, width=360, height=30)
        self.canevas_splash.create_window(480, 250, window=self.btnurlconnect, width=100, height=30)
        # les boutons d'actions -> FENETRE CONNEXION

        self.btncreerpartie = Button(text="Creer partie", font=("Arial", 12), state=DISABLED, command=self.creer_partie)
        self.btninscrirejoueur = Button(text="Inscrire joueur", font=("Arial", 12), state=DISABLED,
                                        command=self.inscrire_joueur)
        self.btnreset = Button(text="Reinitialiser partie", font=("Arial", 9), state=DISABLED,
                               command=self.reset_partie)

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
        self.canevaslobby = Canvas(self.cadrelobby, width=640, height=480, bg="lightblue")
        self.canevaslobby.pack()
        # widgets du lobby
        # un listbox pour afficher les joueurs inscrit pour la partie à lancer
        self.listelobby = Listbox(borderwidth=2, relief=GROOVE)

        # bouton pour lancer la partie, uniquement accessible à celui qui a creer la partie dans le splash
        self.btnlancerpartie = Button(text="Lancer partie", state=DISABLED, command=self.lancer_partie)
        # affichage des widgets dans le canevaslobby (similaire au splash)
        self.canevaslobby.create_window(440, 240, window=self.listelobby, width=200, height=400)
        self.canevaslobby.create_window(200, 400, window=self.btnlancerpartie, width=100, height=30)
        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadrelobby

    #FIN FENETRE LOBBY --------------------------------------------------------------------------

    #FENETRE DU JEU -----------------------------------------------------------------------------
    def creer_cadre_partie(self):
        self.cadrepartie = Frame(self.cadre_app, width=600, height=200, bg="yellow")
        self.cadrejeu = Frame(self.cadrepartie, width=600, height=200, bg="teal")

        self.scrollX = Scrollbar(self.cadrejeu, orient=HORIZONTAL)
        self.scrollY = Scrollbar(self.cadrejeu, orient=VERTICAL)
        self.canevas = Canvas(self.cadrejeu, width=800, height=600,
                              xscrollcommand=self.scrollX.set,
                              yscrollcommand=self.scrollY.set, bg="grey11")

        self.scrollX.config(command=self.canevas.xview)
        self.scrollY.config(command=self.canevas.yview)

        self.canevas.grid(column=0, row=0, sticky=W + E + N + S)
        self.scrollX.grid(column=0, row=1, sticky=W + E)
        self.scrollY.grid(column=1, row=0, sticky=N + S)

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
        self.cadreoutils = Frame(self.cadrepartie, width=200, height=200, bg="red")  #petite fenetre sur la gauche (celle juste au dessus de la mini map)->ici que l<on affiche le menu
        self.cadreoutils.pack(side=LEFT, fill=Y)
        self.cadreinfo = Frame(self.cadreoutils, width=200, height=200, bg="darkgrey")#??????????
        self.cadreinfo.pack(fill=BOTH)

        self.cadreinfogen = Frame(self.cadreinfo, width=200, height=200, bg="grey50")#petite fenetre en haut a gauche (JAJA et bouton MINI)
        self.cadreinfogen.pack(fill=BOTH)
        self.labid = Label(self.cadreinfogen, text="Inconnu")
        self.labid.bind("<Button>", self.centrer_planetemere)#bouton qui est utilise lorsque je clique sur JAJA, ca nous place sur notre planete mere
        self.labid.pack()
        self.btnmini = Button(self.cadreinfogen, text="MINI")
        self.btnmini.bind("<Button>", self.afficher_mini)
        self.btnmini.pack()

        # PETITE FENETRE POUR LES 2 BOUTONS VAISSEAU ET CARGO-----------------------------------------------------------------------------
        self.cadreinfochoix = Frame(self.cadreinfo, height=200, width=200, bg="light grey")
        """fenetre ou il y a bouton vaisseau et cargo"""

        self.btncreervaisseau = Button(self.cadreinfochoix, text="Vaisseau")
        """pour creer un vaisseau"""
        self.btncreervaisseau.bind("<Button>", self.creer_vaisseau)

        self.btncreercargo = Button(self.cadreinfochoix, text="Cargo")
        """pour creer un cargo"""
        self.btncreercargo.bind("<Button>", self.creer_vaisseau)

        self.btncreervaisseau.pack()
        # self.btncreercargo.pack()

        # creer boutonInstallation ici--------------------------------------------------------------------------------------------
        self.btnInstallation = Button(self.cadreinfochoix, text="Installations")
        """pour ouvrir le menu d'installation"""
        self.btnInstallation.config(command=self.methode_installation)
        self.btnInstallation.pack()

        # creer boutonResource ici
        self.btnResource = Button(self.cadreinfochoix, text="Ressources")
        """pour ouvrir le menu de ressource"""
        self.btnResource.config(command=self.methode_resource)
        self.btnResource.pack()

        self.boutonAmeliorerEtoile = Button(self.cadreinfochoix, text="Ameliorer Etoile")
        self.boutonAmeliorerEtoile.pack()
        self.eteAfficher = False

        # ---------------------------------------------------------------------------------------------------------------------------------

        self.cadreinfoliste = Frame(self.cadreinfo)

        self.scroll_liste_Y = Scrollbar(self.cadreinfoliste, orient=VERTICAL)
        self.info_liste = Listbox(self.cadreinfoliste, width=20, height=6, yscrollcommand=self.scroll_liste_Y.set)
        self.info_liste.bind("<Button-1>", self.info_liste_objet)
        self.info_liste.bind("<Button-3>", self.info_liste_objet)
        self.info_liste.grid(column=0, row=0, sticky=W + E + N + S)
        self.scroll_liste_Y.grid(column=1, row=0, sticky=N + S)

        self.cadreinfoliste.columnconfigure(0, weight=1)
        self.cadreinfoliste.rowconfigure(0, weight=1)

        self.cadreinfoliste.pack(fill=BOTH)

        # IMAGE VAISSEAU + VIE --------------------------------------------------------------------------------
        s = Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

        self.cadreinfoimage = Frame(self.cadreoutils, width=200, height=228, background="black")
        self.barrevie = Progressbar(self.cadreoutils, style="red.Horizontal.TProgressbar", orient=HORIZONTAL,
                                    mode="determinate", length=100)

        # MINI MAP-----------------------------------------------------------------------
        self.cadreminimap = Frame(self.cadreoutils, height=200, width=200, bg="black")
        self.canevas_minimap = Canvas(self.cadreminimap, width=self.taille_minimap, height=self.taille_minimap,
                                      bg="pink")
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

    def methode_installation(self):  # afficher
        self.clickUneFoisSurRessource = 0
        self.clickUneFoisSurVaiss = 0
        self.clickUneFoisSurInsta += 1
        print(self.clickUneFoisSurInsta)

        #ENLEVER LABEL RESSOURCES + VAISSEAU
        if self.clickUneFoisSurInsta == 1:
            self.label_or.pack_forget()
            self.label_cuivre.pack_forget()
            self.label_antimatiere.pack_forget()
            self.label_pluto.pack_forget()
            self.label_titane.pack_forget()
            self.label_fer.pack_forget()
            self.label_hydrogene.pack_forget()
            self.barrevie.pack_forget()
            self.cadreinfoimage.pack_forget()
            testHp = "3"  # il faudra recuperer la vrai valeur ici

            self.label_titre = Label(self.cadreoutils, text="Usine Ressource")
            self.label_titre.pack(side=TOP)


            self.label_installation = Label(self.cadreoutils, text="Description: usine pour stocker ressource", bd=1,
                                            relief="solid", width=25, height=4, anchor=W,
                                            )
            self.label_installation.pack()

            self.boutonConstruire = Button(self.cadreoutils, text="Construire Usine")
            self.boutonConstruire.pack()

            self.label_entrepotVaisseau = Label(self.cadreoutils, text="Entrepot a Vaisseaux", bd=1, relief="solid", width=25, height=8, anchor=W)
            self.label_entrepotVaisseau.pack()

            self.boutonConstruireEntrepot = Button(self.cadreoutils, text="Construire Entrepot")
            self.boutonConstruireEntrepot.pack()


    def methode_resource(self):  # afficher

        self.clickUneFoisSurInsta = 0
        self.clickUneFoisSurVaiss = 0
        self.clickUneFoisSurRessource += 1
        self.recup = self.parent.recupEtoile(self.ma_selection[1])

        if self.clickUneFoisSurRessource == 1:
            self.boutonConstruire.pack_forget()
            self.label_titre.pack_forget()
            self.label_installation.pack_forget()
            self.label_entrepotVaisseau.pack_forget()
            self.boutonAmeliorerEtoile.pack_forget()
            self.boutonConstruireEntrepot.pack_forget()
            self.boutonAmeliorerEtoile.pack_forget()
            self.barrevie.pack_forget()
            self.cadreinfoimage.pack_forget()

            self.label_fer = Label(self.cadreoutils, text="Fer : " + str(self.recup.inventaire.get("Fer")), anchor=CENTER, width=25, height=2, border=2, borderwidth=1,
                         relief="solid", bg="green")

            self.label_cuivre = Label(self.cadreoutils, text="Cuivre : " + str(self.recup.inventaire.get("Cuivre")), anchor=CENTER, width=25, height=2, border=2,
                                      borderwidth=1,
                                      relief="solid", bg="green")

            self.label_or = Label(self.cadreoutils, text="Or : " + str(self.recup.inventaire.get("Or")), anchor=CENTER, width=25, height=2, border=2,
                                  borderwidth=1,
                                  relief="solid", bg="yellow")

            self.label_titane = Label(self.cadreoutils, text="Titane : " + str(self.recup.inventaire.get("Titane")), anchor=CENTER, width=25, height=2, border=2,
                                      borderwidth=1,
                                      relief="solid", bg="red")

            self.label_hydrogene = Label(self.cadreoutils, text="Hydrogene : " + str(self.recup.inventaire.get("Hydrogene")), anchor=CENTER, width=25, height=2, border=2,
                               borderwidth=1, relief="solid", bg="green")

            self.label_pluto = Label(self.cadreoutils, text="Plutonium : " + str(self.recup.inventaire.get("Plutonium")), anchor=CENTER, width=25, height=2, border=2,
                               borderwidth=1, relief="solid", bg="yellow")

            self.label_antimatiere = Label(self.cadreoutils, text="???? : " + str(self.recup.inventaire.get("Antimatiere")), anchor=CENTER, width=25, height=2, border=2,
                                           borderwidth=1,
                                           relief="solid", bg="purple")

            #lOr = Label(self.cadreoutils, text="Or", anchor=CENTER, width=25, height=2, border=2, borderwidth=1,
                       # relief="solid", bg="yellow")

            self.label_fer.pack()
            self.label_cuivre.pack()
            self.label_or.pack()
            self.label_titane.pack()
            self.label_hydrogene.pack()
            self.label_pluto.pack()
            self.label_antimatiere.pack()
        #lPlutonium.pack()


    def info_liste_objet(self, evt):
        info = self.info_liste.get(self.info_liste.curselection())
        print(info)
        liste_separee = info.split(";")
        type_vaisseau = liste_separee[0]
        id = liste_separee[1][1:]
        obj = self.modele.joueurs[self.mon_nom].flotte[type_vaisseau][id]
        if evt.num == 1:
            self.afficher_info_vaisseau(obj)
        else:
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
            self.canevas.create_oval(i.x - t, i.y - t, i.x + t, i.y + t,
                                     fill="grey80", outline=col,
                                     tags=(i.proprietaire, str(i.id), "Etoile", i.x, i.y))
        # affichage des etoiles possedees par les joueurs
        for i in mod.joueurs.keys():
            for j in mod.joueurs[i].etoilescontrolees:
                t = j.taille * self.zoom
                self.canevas.create_oval(j.x - t, j.y - t, j.x + t, j.y + t,
                                         fill=mod.joueurs[i].couleur,
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

        if self.clickUneFoisSurVaiss == 1:
            self.boutonConstruire.pack_forget()
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
            self.btnResource.pack_forget()

        self.barrevie.value = objet.Vie

        self.cadreinfoimage.pack(fill=BOTH)  # Debug, à remplacer par une image plus tard
        self.barrevie.pack(fill=BOTH)

    # change l'appartenance d'une etoile et donc les propriétés des dessins les représentants
    def afficher_etoile(self, joueur, cible):
        joueur1 = self.modele.joueurs[joueur]
        id = cible.id
        couleur = joueur1.couleur
        self.canevas.itemconfig(id, fill=couleur)
        self.canevas.itemconfig(id, tags=(joueur, id, "Etoile",))

    # ajuster la liste des vaisseaux
    def lister_objet(self, obj, id, niveau):
        self.info_liste.insert(END, obj + "; " + id + "; Nv." + str(niveau))

    def creer_vaisseau(self, evt):
        type_vaisseau = evt.widget.cget("text")
        self.parent.creer_vaisseau(type_vaisseau, self.selectedTags[3], self.selectedTags[4]) # Il faut que tu trouve comment changer les tags après une capture
        self.ma_selection = None
        self.canevas.delete("marqueur")
        self.cadreinfochoix.pack_forget()



    def afficher_jeu(self):#LA ON AFFICHE BEAUCOUP DE CHOSE!!!:)-------------------------------------------------------------
        mod = self.modele
        self.canevas.delete("artefact")
        self.canevas.delete("objet_spatial")
        self.canevas.delete("marqueur")

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
            vaisseau_local = []
            for k in i.flotte:
                for j in i.flotte[k]:
                    j = i.flotte[k][j]
                    tailleF = j.taille * self.zoom
                    if k == "Vaisseau":  # CREATION DU CARRE ROUGE REPRESENTANT LE VAISSEAU
                        self.canevas.create_rectangle((j.x - tailleF), (j.y - tailleF),
                                                      (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                                                      tags=(j.proprietaire, str(j.id), "Flotte", k, "artefact"))
                    elif k == "Cargo":  # CREATION DU CARGO
                        # self.dessiner_cargo(j,tailleF,i,k)
                        self.dessiner_cargo(j, tailleF, i, k)
                        # self.canevas.create_oval((j.x - tailleF), (j.y - tailleF),
                        #                          (j.x + tailleF), (j.y + tailleF), fill=i.couleur,
                        #                          tags=(j.proprietaire, str(j.id), "Flotte",k,"artefact"))
        for t in self.modele.trou_de_vers:
            i = t.porte_a
            for i in [t.porte_a, t.porte_b]:
                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

                self.canevas.create_oval(i.x - i.pulse, i.y - i.pulse,
                                         i.x + i.pulse, i.y + i.pulse, outline=i.couleur, width=2, fill="grey15",
                                         tags=("", i.id, "Porte_de_ver", "objet_spatial"))

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

    def cliquer_cosmos(self, evt):  # DES QUE LON CLIQUE QUELQUE PART DANS LE JEU
        self.selectedTags = self.canevas.gettags(CURRENT)  # self.canevas = Canvas(self.cadrejeu, width=800, height=600,
        tags = self.selectedTags
        if tags:  # Il y a des tags => On a cliqué sur un objet de la carte (Vaisseau, Étoile, ...)
            if tags[0] == self.mon_nom:
                self.ma_selection = [self.mon_nom, tags[1], tags[2]]
                if tags[2] == "Etoile":
                    self.montrer_etoile_selection()
                    if self.shipSelected:
                        self.parent.cibler_flotte(self.shipSelected, tags[1], tags[2])
                        self.shipSelected = ""
                        self.ma_selection = None
                    else:
                        self.montrer_etoile_selection()
                elif tags[2] == "Flotte":
                    self.montrer_flotte_selection()
                    self.shipSelected = self.ma_selection[1]
            elif ("Etoile" == tags[2] or "Porte_de_ver" == tags[2]):  # Si c'est un objet qui nous appartient pas
                if self.ma_selection:  # Si une sélection de nos vaisseaux a été faites, on les envoi sur l'étoile avec "cibler_flotte"
                    self.parent.cibler_flotte(self.ma_selection[1], tags[1], tags[2])

                self.ma_selection = None
        else:  # aucun tag => On a clické dans le vide donc aucun objet sur la carte
            print("Region inconnue")
            self.ma_selection = None

    def montrer_etoile_selection(self):  # montrer le tag de letoile selectionne
        self.cadreinfoimage.pack_forget()
        self.barrevie.pack_forget()
        self.btnResource.pack()
        self.btnInstallation.pack()
        self.cadreinfochoix.pack(fill=BOTH)

    def montrer_flotte_selection(self):  # montrer le tag du vaisseau selectionne
        print("À IMPLANTER - FLOTTE de ", self.mon_nom)

    # Methodes pour multiselect#########################################################
    def debuter_multiselection(self, evt):
        self.debutselect = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
        x1, y1 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
        self.selecteur_actif = self.canevas.create_rectangle(x1, y1, x1 + 1, y1 + 1, outline="red", width=2,
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
                if self.parent.mon_nom not in self.canevas.gettags(i):
                    objchoisi.remove(i)
                else:
                    self.objets_selectionnes.append(self.canevas.gettags(i)[2])

            self.canevas.delete("selecteur")

    ### FIN du multiselect
