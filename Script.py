"""
Nom du Projet : Jeu Escape Game
Auteur : Binna
Date : 19 avril 2021
Le joueur se déplace dans le labyrinthe d'un château et doit atteindre la sortie pour gagner.
Sur son chemin, il trouvera des portes verrouillées lui bloquant le passage.
Ces portes s'ouvrent à la condition de donner la bonne réponse à la question qu'elles posent.
Le joueur trouvera en chemin des indices lui permettant de répondre à ces questions...

"""

# import des modules externes
import turtle, time

# -------------------------- CONSTANTES GLOBALES ----------------------------

from CONFIGS import *
GAUCHE = (0, -1) # constantes globales décrivant les différents mouvements 
DROITE = (0, 1)
HAUT = (-1, 0)
BAS = (1, 0)

ANNONCES = "annonces" # répété plusieurs fois dans le code --> une constante globale évite les erreurs
HAUTEUR_ZONE_ANNONCES = POINT_AFFICHAGE_ANNONCES[1] - ZONE_PLAN_MAXI[1]
LARGEUR_ZONE_ANNONCES = POINT_AFFICHAGE_ANNONCES[1] - POINT_AFFICHAGE_ANNONCES[0]
PADDING_TOP_ANNONCE = 20 # espace entre l'annonce et le bord supérieur de sa zone
PADDING_LEFT_ANNONCE = 1 # espace entre l'annonce et le bord gauche de sa zone
COORDONNEES_DEPART_ANNONCE = POINT_AFFICHAGE_ANNONCES[0] + PADDING_LEFT_ANNONCE, POINT_AFFICHAGE_ANNONCES[1] - PADDING_TOP_ANNONCE

INVENTAIRE = "inventaire" # répété plusieurs fois dans le code --> une constante globale évite les erreurs
TITRE_INVENTAIRE = "Inventaire : "
HAUTEUR_INVENTAIRE = POINT_AFFICHAGE_INVENTAIRE[1] - ZONE_PLAN_MINI[1]
LARGEUR_INVENTAIRE = POINT_AFFICHAGE_ANNONCES[1] - POINT_AFFICHAGE_INVENTAIRE[0]
PAS_INVENTAIRE = 35 # espacement avant chaque ligne de l'inventaire

# correspondance entre valeur de la case et sa signification
COULOIR = 0
MUR = 1  
PORTE = 3
OBJET = 4
ARRIVEE = 2

# différents messages
MESSAGE_PORTE_FERMEE = "Cette porte est fermée."
MESSAGE_PORTE_OUVERTE = "La porte s'ouvre."
TITRE_FENETRE_QUESTION = "Question"
MESSAGE_ARRIVEE = "Bravo ! Vous avez gagné !"
MESSAGE_ECHEC = "Mauvaise réponse."
MESSAGE_OBJET = "Vous avez trouvé : "

# Police et tailles d'écriture
COULEUR_ECRITURE = 'black'
POLICE = "Comic Sans MS"
TAILLE_TITRE_INVENTAIRE = 12
TAILLE_OBJET_INVENTAIRE = 10
TAILLE_ANNONCE = 11
TEMPS_OUVERTURE_PORTE = 0.6 # temps de latence entre l'ouverture de la porte et le déplacement du joueur
TEMPS_AVANT_ARRET_PROGRAMME = 3



# ----------- ---------------------- DEFINITION DES FONCTIONS -----------------------------------------

#Niveau 1 : Construction et affichage du plan du château (6 fonctions)

def lire_matrice(fichier_encodage):
    """entrée : fichier du plan à tracer - sortie : matrice du plan"""
    with open(fichier_encodage, encoding='utf-8') as fichier_in:
        return [[int(colonne) for colonne in ligne.split()] for ligne in fichier_in]
    
def calculer_pas(matrice):
    """calcule la dimension à donner aux cases"""
    pas1 = (ZONE_PLAN_MAXI[0]-ZONE_PLAN_MINI[0])/len(matrice[0]) # en largeur
    pas2 = (ZONE_PLAN_MAXI[1]-ZONE_PLAN_MINI[1])/len(matrice)    # en hauteur
    if pas1 < pas2:                                              # on retient la plus petite valeur des 2
        return pas1
    else:
        return pas2

def coordonnees(case, pas):
    """calcule les coordonnées en pixels turtle du coin inférieur gauche d’une case (l, c)"""
    abscisse = ZONE_PLAN_MINI[0] + case[1] * pas          
    ordonnee = ZONE_PLAN_MAXI[1] - (case[0]+1) * pas                               
    return (abscisse, ordonnee)

def tracer_carre(dimension):
    """Trace un carre de dimension donnée"""
    turtle.down()
    for i in range(4):
        turtle.forward(dimension)
        turtle.left(90)
        
def tracer_case(case, couleur, pas):
    """trace une case
    Entrée : case (l, c), couleur de remplissage et pas : dimension d'un côté"""
    turtle.tracer(0)         # vitesse de traçage rapide
    turtle.hideturtle()
    turtle.up()
    turtle.goto(coordonnees(case, pas))
    turtle.color(COULEUR_CASES, couleur)
    turtle.begin_fill()
    tracer_carre(pas)
    turtle.end_fill()

def afficher_plan(matrice):
    """trace un plan selon une matrice donnée"""
    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            tracer_case((i,j), COULEURS[matrice[i][j]], mon_pas)
    

# Niveau 2 : Gestion des déplacements du personnage (6 fonctions)

def tracer_perso(position, pas):
    """trace le personnage à la position (ligne, colonne) entrée en argument"""
    # abscisse et ordonnée du centre du disque (personnage)
    abscisse = coordonnees(position, pas)[0] + 0.5 * pas
    ordonnée = coordonnees(position, pas)[1] + 0.5 * pas
    turtle.hideturtle()
    turtle.up()
    turtle.goto(abscisse, ordonnée)
    turtle.down()
    turtle.dot(pas * RATIO_PERSONNAGE , COULEUR_PERSONNAGE) #diamètre, couleur
    turtle.up()
             
def deplacer_gauche():
    """ fonction appelée lorsque le joueur appuie sur la flèche de gauche du clavier"""
    # Les fonctions associées à onkeypress ne peuvent pas accepter de paramètres
    turtle.onkeypress(None, "Left")   # Désactive la touche Left
    deplacer(GAUCHE) # appel de la fonction "deplacer" avec en paramètre le mouvement désiré
    turtle.onkeypress(deplacer_gauche, "Left")   # Réassocie la touche Left à la fonction deplacer_gauche

def deplacer_droite():
    """ fonction appelée lorsque le joueur appuie sur la flèche de droite"""
    turtle.onkeypress(None, "Right") 
    deplacer(DROITE)
    turtle.onkeypress(deplacer_droite, "Right")

def deplacer_haut():
    """ fonction appelée lorsque le joueur appuie sur la flèche du haut"""
    turtle.onkeypress(None, "Up") 
    deplacer(HAUT)
    turtle.onkeypress(deplacer_haut, "Up")

def deplacer_bas():
    """ fonction appelée lorsque le joueur appuie sur la flèche du bas """
    turtle.onkeypress(None, "Down") 
    deplacer(BAS)
    turtle.onkeypress(deplacer_bas, "Down")
    
def deplacer(mouvement):
    """ fonction de contrôle du mouvement du joueur"""
    # si la fonction doit modifier la valeur de variables globales,
    # alors il faut les redéclarer en les précédant du mot-clé global
    global ma_position, ma_matrice
    # on efface la zone d'annonces à chaque volonté de déplacement
    effacer_zone(ANNONCES)
    # on détermine la nouvelle position du perso à partir de la position actuelle et du mouvement souhaité
    nouvelle_position = (ma_position[0] + mouvement[0], ma_position[1] + mouvement[1])
    # on effectue le déplacement si la nouvelle position est dans les limites du plan
    if 0 <= nouvelle_position[0] < len(ma_matrice) and 0 <= nouvelle_position[1] < len(ma_matrice[0]):
        # ET si la nouvelle position ne correspond pas à une case mur (1) ni à une porte (3)
        valeur_case = ma_matrice[nouvelle_position[0]][nouvelle_position[1]]
        if  valeur_case != MUR and valeur_case != PORTE:
            # DEPLACEMENT
            tracer_case(ma_position, COULEUR_VUE, mon_pas) # tracer une case colorée sur la position actuelle du perso
            ma_position = nouvelle_position  # nouvelle_position est valable donc on peut l'affecter à ma_position
            tracer_case(ma_position, COULEUR_VUE, mon_pas) # tracer une case colorée sur la nouvelle position du perso
            tracer_perso(ma_position, mon_pas)   # tracer perso sur la nouvelle position
            if valeur_case == OBJET: # case objet
                ramasser_objet(ma_position)
                #remplacer la valeur de la case dans la matrice par 0 (couloir) pour qu'on ne puisse pas ramasser plusieurs fois le même objet
                ma_matrice[ma_position[0]][ma_position[1]] = COULOIR
            if valeur_case == ARRIVEE : # case arrivée
                afficher_annonce(MESSAGE_ARRIVEE)
                time.sleep(TEMPS_AVANT_ARRET_PROGRAMME)
                exit()
        elif valeur_case == PORTE: # case porte
            poser_question(ma_matrice, nouvelle_position, mouvement)
            
                
# Niveau 3 : Collecte d'objets dans le labyrinthe (5 fonctions)

def creer_dictionnaire(fichier_des_objets):
    """crée un dictionnaire à partir d'un fichier qui contient sur chaque ligne
    une clé : case (l, c) et une valeur : objet """
    d = {}
    with open(fichier_des_objets, encoding='utf-8') as fichier_in:
        for ligne in fichier_in:
            cle, valeur = eval(ligne) 
            d[cle] = valeur
    return d

def ramasser_objet(position):
    """ fonction appelée lorsque le joueur ramasse un objet"""
    # ajouter l'objet à l'inventaire
    objet = dico_objets[position]
    inventaire.append(objet)
    # afficher l'inventaire à droite du plan
    afficher_inventaire()
    # afficher l'objet trouvé dans le cadre d'annonces
    afficher_annonce(MESSAGE_OBJET + objet)
    
def afficher_inventaire():
    """ affiche l'inventaire dans la zone dédiée"""
    effacer_zone(INVENTAIRE) #effacer la zone d'affichage de l'inventaire
    coordonnees = (POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1] - PAS_INVENTAIRE)
    turtle.up()
    turtle.goto(coordonnees)
    turtle.color(COULEUR_ECRITURE)
    turtle.down()
    turtle.write(TITRE_INVENTAIRE, font=(POLICE, TAILLE_TITRE_INVENTAIRE))
    turtle.up()
    for objet in inventaire:
        coordonnees = (coordonnees[0], coordonnees[1] - PAS_INVENTAIRE)
        turtle.goto(coordonnees)
        turtle.down()
        turtle.write(objet, font=(POLICE, TAILLE_OBJET_INVENTAIRE))
        turtle.up()
    
def afficher_annonce(annonce):
    """ affiche une annonce dans la zone dédiée """
    coordonnees = COORDONNEES_DEPART_ANNONCE
    turtle.up()
    turtle.color(COULEUR_ECRITURE)
    turtle.goto(coordonnees)
    turtle.down()
    turtle.write(annonce, font=(POLICE, TAILLE_ANNONCE))
    turtle.up()
    
def effacer_zone(zone):
    """ dessine un rectangle blanc sur la zone (str) entrée en paramètre pour l'effacer"""
    turtle.up()
    if zone == ANNONCES:
        turtle.goto(POINT_AFFICHAGE_ANNONCES)
        largeur = LARGEUR_ZONE_ANNONCES
        hauteur = HAUTEUR_ZONE_ANNONCES
    elif zone == INVENTAIRE:
        turtle.goto(POINT_AFFICHAGE_INVENTAIRE)
        largeur = LARGEUR_INVENTAIRE
        hauteur = HAUTEUR_INVENTAIRE
    turtle.color(COULEUR_EXTERIEUR)
    turtle.down()
    turtle.begin_fill()
    for i in range(2):
        turtle.forward(largeur)
        turtle.right(90)
        turtle.forward(hauteur)
        turtle.right(90)
    turtle.end_fill()
    turtle.up()
    
# Niveau 4 : Le jeu escape game complet avec questions-réponses (1 fonction)

def poser_question(matrice, case, mouvement) :
    """ pose une question au joueur selon la case porte rencontrée"""
    # afficher dans le cadre d'annonces
    afficher_annonce(MESSAGE_PORTE_FERMEE)
    # poser la question qui correspond à la case
    question = dico_questions[case][0]
    reponse = turtle.textinput(TITRE_FENETRE_QUESTION, question) # fonction qui lance son propre turtle.listen() mais annule celui déjà ouvert
    turtle.listen() # c'est pourquoi on relance cette méthode ici
    if reponse == dico_questions[case][1]: # bonne réponse
        effacer_zone(ANNONCES)
        afficher_annonce(MESSAGE_PORTE_OUVERTE)
        time.sleep(TEMPS_OUVERTURE_PORTE) # petit temps d'attente avant d'effectuer la fonction deplacer (car elle efface la zone d'annonces)
        matrice[case[0]][case[1]] = 0
        deplacer(mouvement)
    elif reponse is None : # pas de réponse
        effacer_zone(ANNONCES)
    else : # mauvaise réponse
        effacer_zone(ANNONCES)
        afficher_annonce(MESSAGE_ECHEC)
    


# ***********  PARTIE TRAITEMENT DU PROGRAMME **************************************

# variables
ma_matrice = lire_matrice(fichier_plan)
mon_pas = calculer_pas(ma_matrice)
dico_objets = creer_dictionnaire(fichier_objets)
dico_questions = creer_dictionnaire(fichier_questions)
inventaire = []
ma_position = POSITION_DEPART

# instructions

afficher_plan(ma_matrice)
afficher_inventaire()  
tracer_perso(ma_position, mon_pas)

turtle.listen()    # Déclenche l’écoute du clavier
turtle.onkeypress(deplacer_gauche, "Left")   # Associe à la touche Left une fonction appelée deplacer_gauche
turtle.onkeypress(deplacer_droite, "Right")
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")
turtle.mainloop()    # Place le programme en position d’attente d’une action du joueur
