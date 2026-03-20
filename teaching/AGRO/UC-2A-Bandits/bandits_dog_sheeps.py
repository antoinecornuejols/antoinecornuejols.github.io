# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 17:18:48 2026

@author: ChM
"""

from random import randint, shuffle, choice
import numpy as np
import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle as pkl

###############################################################################    

class Animal(object):
    """
    Classe permettant de représenter un animal évoluant sur un environnement
    """
        
    def __init__(self, _env, _x, _y, _id, _color):
        """
        Constructeur de la classe Animal qui étant donné
        _env représentant un environnement (par exemple )
        _x et _y position dans l'environnement
        _id représente l'identifiant de l'animal que l'on veut créer
        _color représente sa couleur sous forme de chaîne de caractères
        """
        
        self.id = _id
        self.init_x = _x #sauvegarde de la position initiale pour le replacement au début de chaque épisode
        self.init_y = _y #sauvegarde de la position initiale pour le replacement au début de chaque épisode
        self.x = _x
        self.y = _y
        self.env = _env
        self.case = _env.cases[_x][_y] #l'animal retient la case sur laquelle il est placé
        _env.cases[_x][_y].contain.append(self) #la case correspondante enregistre la présence de l'animal
        self.cases_possibles = [] #permettra de déterminer les déplacements possibles de l'animal
        self.color = _color
        
        # un animal peut se déplacer dans toutes les directions 
        # et les actions sur les coordonnées sont enregistrées dans un dictionnaire
        self.directions = {}
        self.directions["N"] = [[0,-1], [-1,-1], [1,-1]]
        self.directions["S"] = [[0,1], [1,1], [-1,1]]
        
        self.directions["E"] = [[1,0], [1,1], [1,-1]]
        self.directions["O"] = [[-1,0], [-1,-1], [-1,1]]

        self.directions["NE"] = [[1, -1],[0, -1], [1, 0]] 
        self.directions["NO"] = [[-1,-1], [0,-1], [-1,0]]
        
        self.directions["SE"] = [[1,1], [0,1], [1,0]]
        self.directions["SO"] = [[-1,1], [0,1], [-1,0]]
        
    def __str__(self):
        """
        Méthode permettant de transformer l'objet sous forme de chaîne de caractères
        ici on considère uniquement l'identifiant'
        """
        return str(self.id)
        
    def __repr__(self):
        """
        Méthode permettant de transformer l'objet sous forme de chaîne de caractères
        ici on considère uniquement l'identifiant'
        """
        return str(self.id)
    
    def move_alea (self) :
        """
        Fonction permettant de déterminer un nouvelle position aléatoire pour l'animal
        """
        if self.peut_bouger() :
            choose_case = choice(self.cases_possibles)
            choose_case.contain.append(self)
            self.env.cases[self.x][self.y].contain.remove(self)
            self.x = choose_case.ind_ligne
            self.y = choose_case.ind_colonne
            self.case = choose_case
        
    def peut_bouger(self):
        """
        Fonction permettant de déterminer si l'animal peut bouger
        Renvoie True si des cases vides lui sont accessibles et False dans le cas contraire
        """
        self.cases_possibles = []
        res = False
        for une_case in self.case.voisines :
            if une_case.is_empty() :
                self.cases_possibles.append(une_case)
                res = True
        return res

###############################################################################        

class Mouton(Animal):
    """
    Classe permettant de représenter un mouton
    Classe qui hérite de la classe Animal
    """
    def __init__(self, _env, _x, _y, _id, _color) :
        """
        Constructeur de la classe Mouton qui étant donné
        _env représentant un environnement (par exemple )
        _x et _y position dans l'environnement
        _id représente l'identifiant de l'animal que l'on veut créer
        _color représente sa couleur sous forme de chaîne de caractères
        """
        
        super().__init__(_env, _x, _y, _id, _color) # On récupère toutes les propriétés d'un Animal
        self.in_pen = False # attribut pour stocker si le mouton est dans l'enclos ou non  

    def get_mean_sheeps(self):
        """
        Fonction permettant de déterminer étant donné une instance de mouton 
        la position (x,y) du centre de gravité des autres moutons
        ou None s'il n'y a pas d'autres moutons
        """
        if self in self.env.sheeps :
            if len(self.env.sheeps) > 1 :
                x_mean = sum ([animal.x for animal in self.env.sheeps if animal != self])/(len(self.env.sheeps)-1)
                y_mean = sum ([animal.y for animal in self.env.sheeps if animal != self])/(len(self.env.sheeps)-1)
            else :
                x_mean = self.env.sheeps[0].x
                y_mean = self.env.sheeps[0].y
            return x_mean, y_mean
        else :
            return None


    def one_step_move_dog(self) :
        """
        Fonction permettant de réaliser si possible un mouvement élémentaire de fuite du mouton devant le chien
        """
        log_file.write("dans one_step_move_dog\n")
        if self.peut_bouger() :
            self.env.canvas.itemconfigure(self.case.rect, fill=self.case.color)
            x_chien = self.env.chien.x
            y_chien = self.env.chien.y

            direction = None
            if x_chien > self.x :
                if y_chien > self.y :
                    direction = "NO"
                elif y_chien == self.y :
                    direction = "O"
                else :
                    direction = "SO"
            elif x_chien == self.x :
                if y_chien > self.y :
                    direction = "N"
                else :
                    direction = "S"
            else :
                if y_chien > self.y :
                    direction = "NE"
                elif y_chien == self.y :
                    direction = "E"
                else :
                    direction = "SE"
                
            #On recherche les au plus 3 cases qui vont dans la bonne direction 
            log_file.write("position du chien : {} {}\n".format(x_chien, y_chien))
            log_file.write("position du mouton : {} {}\n".format(self.x, self.y))
            log_file.write("direction à suivre : {}\n".format(direction))
            log_file.flush()

            new_pos_possible = [[self.x+x_pos, self.y+y_pos] for [x_pos, y_pos] in self.directions[direction] if self.env.position_valide(self.x+x_pos, self.y+y_pos)]
              
            shuffle(new_pos_possible) # on les mélange pour ne pas toujours choisir exactement la même 
            log_file.write("nouvelles positions possibles : {} \n".format(new_pos_possible))

            new_pos_valide = None
            
            i = 0
            while i < len (new_pos_possible) and new_pos_valide is None :
                log_file.write("position testée : {}, {} \n".format(new_pos_possible[i][0], new_pos_possible[i][1]))
                if self.env.position_vide(new_pos_possible[i][0], new_pos_possible[i][1]) and self.env.cases[new_pos_possible[i][0]][new_pos_possible[i][1]] in self.case.voisines :
                    #si la position est valide on la retient et on termine la boucle
                    new_pos_valide = new_pos_possible[i]
                i += 1
            log_file.write("position choisie : {} \n".format(new_pos_valide))                
                 
            if new_pos_valide != None :
                
                self.env.cases[self.x][self.y].contain.remove(self) 
                self.x = new_pos_valide[0]
                self.y = new_pos_valide[1]
                
                log_file.write("nouvelle position du mouton : {}, {} \n".format(self.x, self.y))   
                
                self.env.cases[self.x][self.y].contain.append(self)
                self.case = self.env.cases[self.x][self.y]
                if self.case.type == 'enclos' :
                    self.in_pen = True
                else : 
                    self.in_pen = False
            else :
                pass 
                #on pourrait envisager ici de bouger aléatoirement suivant une certaine proba
                
            self.env.canvas.itemconfigure(self.case.rect, fill=self.color)

    def one_step_move_mean(self) :
        """
        Fonction permettant de réaliser si possible un mouvement élémentaire de rapprochement vers le troupeau
        """        
        log_file.write("dans one_step_move_mean pour le mouton {}\n".format(self.id))
        if self.peut_bouger() :
            if len(self.env.sheeps) > 1 :
                self.env.canvas.itemconfigure(self.case.rect, fill=self.case.color)
                x_mean, y_mean = self.get_mean_sheeps()
                
                log_file.write("position moyenne des moutons :{},{}\n".format(x_mean, y_mean))
                log_file.flush()

                # Move towards the center of gravity of other sheeps
                direction = None
                if x_mean > self.x :
                    if y_mean > self.y :
                        direction = "SE"
                    elif y_mean == self.y :
                        direction = "E"
                    else :
                        direction = "NE"
                elif x_mean == self.x :
                    if y_mean > self.y :
                        direction = "S"
                    else :
                        direction = "N"
                else :
                    if y_mean > self.y :
                        direction = "SO"
                    elif y_mean == self.y :
                        direction = "O"
                    else :
                        direction = "NO"
                    
                #On recherche les au plus 3 cases qui vont dans la bonne direction 
                log_file.write("position du centre : {} {}\n".format(x_mean, y_mean))
                log_file.write("position du mouton : {} {}\n".format(self.x, self.y))
                log_file.write("direction à suivre : {}\n".format(direction))
                log_file.flush()  
                
                new_pos_possible = [[self.x+x_pos, self.y+y_pos] for [x_pos, y_pos] in self.directions[direction] if self.env.position_valide(self.x+x_pos, self.y+y_pos)]
                  
                shuffle(new_pos_possible) # on les mélange pour ne pas toujours choisir exactement la même 
                log_file.write("nouvelles positions possibles : {} \n".format(new_pos_possible))
                
                new_pos_valide = None
                i = 0
                while i < len (new_pos_possible) and new_pos_valide is None :
                    log_file.write("position testée : {}, {} \n".format(new_pos_possible[i][0], new_pos_possible[i][1]))
                    if self.env.position_vide(new_pos_possible[i][0], new_pos_possible[i][1]) and self.env.cases[new_pos_possible[i][0]][new_pos_possible[i][1]] in self.case.voisines :
                        #si la position est valide on la retient et on termine la boucle
                        new_pos_valide = new_pos_possible[i]
                    i += 1
                log_file.write("position choisie : {} \n".format(new_pos_valide))                
                                  
                if new_pos_valide != None :
                    self.env.cases[self.x][self.y].contain.remove(self) 
                    self.x = new_pos_valide[0]
                    self.y = new_pos_valide[1]
                    
                    log_file.write("nouvelle position du mouton : {}, {} \n".format(self.x, self.y))   
                    
                    self.env.cases[self.x][self.y].contain.append(self)
                    self.case = self.env.cases[self.x][self.y]
                    if self.case.type == 'enclos' :
                        self.in_pen = True
                    else : 
                        self.in_pen = False
                else :
                    pass 
                    #on pourrait envisager ici de bouger aléatoirement suivant une certaine proba
                    
                self.env.canvas.itemconfigure(self.case.rect, fill=self.color)
                    
            
    def move_far_dog(self) : 
        """
        Fonction permettant de gérer la réponse du mouton à l'action du chien :
            nouvelle position ou aboiement
        """
        # Move in response of the dog
        if self.peut_bouger() :
            multiply_by = 0
            if self.distance_dog() < 6 :
                if self.env.chien.barking :
                    multiply_by = 3
                elif self.distance_dog() < 3 :
                    multiply_by = 1

            i = 0
            while i < multiply_by :
                self.one_step_move_dog()
                i += 1

   
    def distance_dog(self):
        """
        Fonction permettant de calculer la distance du mouton considéré au chien

        Returns
        -------
        res : float
            La distance du mouton au chien

        """
        res = math.sqrt ((self.x-self.env.chien.x)**2+(self.y-self.env.chien.y)**2)
        return res    

###############################################################################

class Chien(Animal):
    """
    Classe permettant de représenter un chien
    Classe qui hérite de la classe Animal
    """

    def __init__(self, _env, _x, _y, _id, _color, alpha=0.1, gamma=0.95, epsilon=1) : 
        """
        Constructeur de la classe Chien qui étant donné
        _env représentant un environnement (par exemple )
        _x et _y position dans l'environnement
        _id représente l'identifiant de l'animal que l'on veut créer
        _color représente sa couleur sous forme de chaîne de caractères
        alpha, gamma et epsilon : permettant de gérer ses caractéristiques d'apprentissage
        """
        super().__init__(_env, _x, _y, _id, _color)
        self.nb_actions = 4      # number of actions for the dog (4 directions of move + barking)
        self.nb_distances = 4
        self.nb_radius = 5
        self.actions = range(self.nb_actions)
        dimensions_table = (self.nb_distances, self.nb_distances, self.nb_radius, self.nb_actions)
        self.q_value = np.zeros(dimensions_table)    # Initialization of the q_value table
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.i_episode = 0  
        self.state_chien = [0, 0, 0]
        self.barking = False
        self.i_epsilon = epsilon # so that the exploration rate evolves with time
        self.epsilon_end = 0

    
    def sheeps_distance(self):
        """
        Fonction permettant de déterminer la distance discrétisée du chien 
        au centre des moutons dans l'herbe

        Returns
        -------
        res : int

        """
        log_file.write("dans sheeps_distance \n")
        
        distance_max = 10 #obtenue sur ce cas particulier .... à adapter ....
        #on récupère le centre de gravité des moutons encore dans l'herbe
        x_mean_sheeps, y_mean_sheeps = self.get_mean_sheeps_grass()
        res = 0

        if x_mean_sheeps != None :
            distance = math.sqrt((x_mean_sheeps - self.x)**2 + (y_mean_sheeps - self.y)**2)
            log_file.write("distance du chien au centre du troupeau : {} \n".format(distance))
            if distance_max / 4 > distance :
                res = 0
            elif distance_max / 2 > distance :
                res = 1
            elif distance_max * 3 / 4 > distance :
                res = 2   
            else :
                res = 3

        log_file.write("distance discrete du chien au centre du troupeau : {} \n".format(res))
        return res
        

    def get_mean_sheeps_grass(self):
        """
        Fonction permettant de déterminer si possible le centre de gravité 
        des moutons dans l'herbe et None sinon

        Returns
        -------
        float,float s'il reste des moutons dans l'herbe
        None dans le cas contraire

        """
        sheeps_to_consider = []
        for sheep in self.env.sheeps :
            if sheep.case.type == 'grass' :
                sheeps_to_consider.append(sheep)
        if sheeps_to_consider != []:           
            x_mean = sum ([animal.x for animal in sheeps_to_consider])/(len(sheeps_to_consider))
            y_mean = sum ([animal.y for animal in sheeps_to_consider])/(len(sheeps_to_consider))
            return x_mean, y_mean    
        else : 
            return None, None            
         

    def move_to_sheeps(self):
        """
        S'il le peut le chien se déplace vers le centre de gravité des moutons dans l'herbe
        """
        
        new_x = self.x
        new_y = self.y 

        if self.peut_bouger() :

            x_mean, y_mean = self.get_mean_sheeps_grass()
            if x_mean is None :
                #on va vers la porte 
                x_mean = self.door[0].ind_ligne
                y_mean = self.door[0].ind_colonne
                
            new_x = self.x
            new_y = self.y
            # Move towards the center of gravity of the sheeps
            if x_mean > self.x :
                new_x = self.x + 1
            elif x_mean < self.x : 
                new_x = self.x - 1
            if y_mean > self.y :
                new_y = self.y + 1
            elif y_mean < self.y : 
                new_y = self.y - 1
          
        return new_x, new_y
        

    
    def get_dir_sheeps(self):
        """
        Fonction permettant de déterminer la direction du chien au centre des moutons
        dans l'herbe
        """
        log_file.write("dans get_dir_sheeps :\n")
        x_mean_sheeps, y_mean_sheeps = self.get_mean_sheeps_grass()
        
        if x_mean_sheeps == None : # s'il n'y a plus de moutons dans l'herbe
            #on va vers la porte 
            x_mean_sheeps = self.door[0].ind_ligne
            y_mean_sheeps = self.door[0].ind_colonne
            
        vect_dog_sheeps = [x_mean_sheeps-self.x, y_mean_sheeps-self.y]
        log_file.write("vecteur chien-moutons : {}\n".format(vect_dog_sheeps))
        
        norme_vect_dog_sheeps = math.sqrt(vect_dog_sheeps[0]**2+vect_dog_sheeps[1]**2)
        log_file.write("norme chien-moutons : {}\n".format(norme_vect_dog_sheeps))
        if norme_vect_dog_sheeps : 
            vect_dog_sheeps = [vect_dog_sheeps[0]/norme_vect_dog_sheeps, vect_dog_sheeps[1]/norme_vect_dog_sheeps]
            
        log_file.write("vecteur normé chien-moutons : {}\n".format(vect_dog_sheeps))
        log_file.flush()
        
        return vect_dog_sheeps, norme_vect_dog_sheeps
    
    
    def get_dir_around_sheeps_right(self) :
        """
        Fonction permettant de déterminer la direction perpendiculaire à l'axe chien - centre des moutons
        dans l'herbe et vers la droite
        """
        vect_dog_sheeps, norme_vect_dog_sheeps = self.get_dir_sheeps()
        vect_ortho_right = [-vect_dog_sheeps[1], vect_dog_sheeps[0]]

        return vect_ortho_right     
    
    def get_dir_around_sheeps_left(self) :
        """
        Fonction permettant de déterminer la direction perpendiculaire à l'axe chien - centre des moutons
        dans l'herbe et vers la gauche
        """
        vect_dog_sheeps, norme_vect_dog_sheeps = self.get_dir_sheeps()
        vect_ortho_left = [vect_dog_sheeps[1], -vect_dog_sheeps[0]]

        return vect_ortho_left       
    
    def move_dir (self, direction, coeff) :
        """
        Fonction permettant de déterminer les nouvelles coordonnées en suivant la direction direction 
        et un nombre de pas égal à 1 ou 2 
        pour d'autres valeurs la position sera inchangée
        """
        new_x = self.x
        new_y = self.y
        
        if coeff == 1 :

            if direction[0]>0.5 :
                new_x += 1
            elif direction[0]<-0.5 :
                new_x -= 1
            if direction[1]>0.5 :
                new_y += 1
            elif direction[1]<-0.5 :
                new_y -= 1
        elif coeff == 2 :
            direction = [coord*coeff for coord in direction]
            if direction[0]>1.5 :
                new_x += 2
            elif direction[0]>0.5 :
                new_x += 1
            elif direction[0]<-1.5 :
                new_x -= 2
            elif direction[0]<-0.5 :
                new_x -= 1
                
            if direction[1]>1.5 :
                new_y += 2
            elif direction[1]>0.5 :
                new_y += 1
            elif direction[1]<-1.5 :
                new_y -= 2                
            elif direction[1]<-0.5 :
                new_y -= 1

        return new_x, new_y  
        
    def around_sheeps_right(self):
        """
        Aller dans la direction perpendiculaire à la direction du centre de gravité des moutons vers la droite.

        Returns
        -------
        int, int : nouvelle position 

        """
        vect_ortho_right = self.get_dir_around_sheeps_right()
        new_x, new_y = self.move_dir(vect_ortho_right, 1)
        
        return new_x, new_y
    
    def around_sheeps_left(self):
        """
        Aller dans la direction perpendiculaire à la direction du centre de gravité des moutons vers la gauche.

        Returns
        -------
        int, int : nouvelle position 

        """
        vect_ortho_left = self.get_dir_around_sheeps_left()
        new_x, new_y = self.move_dir(vect_ortho_left, 1)
        
        return new_x, new_y
    
    def peut_bouger(self):
        """
        Fonction permettant de déterminer si le chien peut bouger ou non 
        sachant qu'il doit rester dans l'herbe
        """
        self.cases_possibles = []
        res = False
        for une_case in self.case.voisines :
            if une_case.is_empty() and une_case.type =='grass' :
                self.cases_possibles.append(une_case)
                res = True
        return res

    def choose_action(self, perceived_state) :
        """
        Fonction permettant de déterminer l'action à mener étant donné un état perçu 
        et les q_valeurs
        """

        self.i_episode += 1

        if np.random.rand() < self.i_epsilon : 
            # Exploration: random choice of action
            action = np.random.choice(self.actions)
        else:
            list_q_values = []
            for act in self.actions :
                list_q_values.append(self.q_value[perceived_state[0]][perceived_state[1]][perceived_state[2]][act]) 

            action = self.actions[np.argmax(list_q_values)]
           
        return action





    def make_action(self, action) :    
        """ 
        Fonction permettant de réaliser une action donnée si cela est possible
        """
        self.color = 'black'
        self.barking = False
        new_x = self.x
        new_y = self.y
        match action :

            case 0 :            # se rapprocher du centre du troupeau
                log_file.write('le chien se déplace vers le troupeau\n')

                new_x, new_y = self.move_to_sheeps()
            case 1 :            # contourner par la droite
                log_file.write('le chien contourne par la droite\n')

                new_x, new_y = self.around_sheeps_right()                            
            case 2 :            # contourner par la gauche
                log_file.write('le chien contourne par la gauche\n')

                new_x, new_y = self.around_sheeps_left()  
             
            case 3 :            # dog barks
                log_file.write('le chien aboie\n')

                self.barking = True
                self.color = 'red'     
                 

        if new_x != self.x or new_y != self.y : # si le chien essaie de bouger
            # Réalise le mouvement sur le plateau  (changer de couleur si aboie (e.g. rouge))
            if self.env.position_vide(new_x, new_y) and self.env.cases[new_x][new_y] in self.case.voisines and self.env.cases[new_x][new_y].type =='grass' :
                self.env.canvas.itemconfigure(self.case.rect, fill=self.case.color)
                self.env.cases[self.x][self.y].contain.remove(self) 
                self.x = new_x
                self.y = new_y
                
                self.env.cases[self.x][self.y].contain.append(self)
                self.case = self.env.cases[self.x][self.y]
                
                self.env.canvas.itemconfigure(self.case.rect, fill=self.color)
            else : 
                action = None
        self.env.canvas.itemconfigure(self.case.rect, fill=self.color)
        return action   


            
    def update_Q(self, state, action, next_state, next_action):
        '''
        updates the action-value function estimate using the most recent time step.
        Qsa + (alpha * (reward + (gamma * Qsa_next) - Qsa))
        Params
        ======
        - state, next_state : list  (e.g. [6, 1, 2] : 6 sheeps left, quadran mouton, quadran door)
        - action: an integer in [0, ..., 4]
                direction of the move  (between 0 and 3) (North, East, South, West)
                barking or not (if barking, no change of position) : action = 4
        '''
        if action != None :
            Qsa = self.q_value[state[0]][state[1]][state[2]][action]
            Qsa_next = self.q_value[next_state[0]][next_state[1]][next_state[2]][next_action]
            self.q_value[state[0]][state[1]][state[2]][action] = Qsa + (self.alpha * (self.env.reward + (self.gamma * Qsa_next) - Qsa))

###############################################################################


class Case (object) :
    """
    Classe permettant de gérer les spécificités et les comportements des 'cases'
    de l'environnement considéré'
    """
    def __init__(self,_size, _ind_ligne , _ind_colonne, _color = 'green', _type = 'grass') :
        """
        Constructeur de la classe Case

        Parameters
        ----------
        _size : entier
            représente la taille en pixel d'une case'
        _ind_ligne : int
            position dans le grille à l'horizontale '
        _ind_colonne : int
            position de la grille à la verticale descendante
        _color : string, optional
            chaine de caractères représentant la couleur de la case. The default is 'green'.
        _type : string, optional
            chaine de caractères représentant la nature de la case. The default is 'grass'.

        Returns
        -------
        Une nouvelle instance de Case

        """
        self.voisines = [] # liste des cases atteignables 
        self.contain = [] # contenu de la case
        self.size = _size
        self.ind_ligne = _ind_ligne
        self.ind_colonne = _ind_colonne
        self.color = _color
        self.type = _type
        
    def __str__(self) :
        """
        Fonction de conversion en chaîne de caractères d'une instance de Case
        """
        return str(self.ind_ligne)+','+str(self.ind_colonne)+','+str(self.contain)
    
    def __repr__(self) : 
        """
        Fonction de conversion en chaîne de caractères d'une instance de Case
        """
        return str(self.ind_ligne)+','+str(self.ind_colonne)+','+str(self.contain)
    
    def is_empty(self) :
        """
        Fonction permettant de tester si une case est vide ou non
        """
        return not bool(self.contain)

###############################################################################

class Environnement (object) :
    """
    Classe permettant de représenter un environnement dans lequel vont évoluer 
    le chien et les moutons
    """
    def __init__(self, _nb_trains, _taille_grille, _nb_sheeps, _case_size = 20, _freq = 200) : 
        """
        Constructeur de la classe Environnement 
        _nb_trains : nombre d'éposides d'apprentissage
        _taille_grille : nombre de lignes et de colonne de la grille considérée
        _nb_sheeps : nombre de moutons
        _case_size = 20 : taille en pixel des cases
        _freq = 200 : fréquence d'execution des pas d'apprentissage
        """
        self.case_size = _case_size
        self.nb_lignes = _taille_grille[0]
        self.nb_colonnes = _taille_grille[1]
        self.nb_sheeps = _nb_sheeps
        self.nb_not_in_pen = _nb_sheeps
        self.nb_not_in_pen_before = _nb_sheeps   # after the action of chien and before the moves of the moutons

        self.door = []
        
        self.current_perceived_state = [0, 0, 0]
        
        self.restart = False
        self.nb_steps = 0
        self.nb_trains = _nb_trains
        self.nb_trains_effectues = 1
        
        self.nb_steps = 0 #nombre de pas réalisés dans un épisode
        self.list_nb_steps = [] #liste des nombres de pas réalisés sur les différents épisodes
        
        self.frequence = _freq
        
        self.reward = 0 # récompense d'une action
        self.episode_reward = 0 # récompense cumulée sur un épisode
        self.rewards = [] #liste des récompenses cumulées sur les épisodes

        
        self.pkl_file_q = 'Q_trained.pkl' # nom du fichier de sauvegarde des q_valeurs
        
        self.init_window()

        
    def init_window(self) :
        """
        Fonction permettant d'initialiser la fenêtre graphique'
        """
        # éléments relatifs à la fenêtre graphique
        self.fenetre = tk.Tk()
        self.frame_root = tk.Frame(self.fenetre)
        self.frame_root.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.frame_env = tk.Frame(self.frame_root)
        self.frame_env.pack(side=tk.LEFT)
        self.canvas = tk.Canvas(self.frame_env)
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=10, pady=10) 
        
        self.button = tk.Button(self.frame_env, text="Utiliser les q_valeurs d'un entrainement précédent", command = self.load_q_values)
        self.button.pack()#expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.button = tk.Button(self.frame_env, text="Initialiser la grille", command = self.restart_grid)
        self.button.pack()#expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.button = tk.Button(self.frame_env, text="Lancer l'apprentissage", command = self.one_step)
        self.button.pack()#expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Figure matplotlib pour les recompenses cumulées
        self.fig1, self.ax1 = plt.subplots(figsize=(5, 4))
        self.ax1.set_xlim(-1, self.nb_trains+1)
        self.line_ax1, = self.ax1.plot(0)
        plt.title("Récompenses cumulées au cours d'un épisode")

        self.frame_graph1 = tk.Frame(self.frame_root)
        self.frame_graph1.pack()
       
        self.canvas_graph1 = FigureCanvasTkAgg(self.fig1, master=self.frame_graph1)
        self.canvas_graph1.get_tk_widget().pack(fill="both", expand=True)
        
        # Figure matplotlib pour les nombres de pas nécessaires avant d'atteindre l'objectif
        self.fig2, self.ax2 = plt.subplots(figsize=(5, 4))
        self.ax2.set_xlim(-1, self.nb_trains+1)
        self.line_ax2, = self.ax2.plot(0)
        self.line_lissee_ax2, = self.ax2.plot(0)
        plt.title("Nombre des pas nécessaires pour atteindre l'objectif")

        self.frame_graph2 = tk.Frame(self.frame_root)
        self.frame_graph2.pack()

        self.canvas_graph2 = FigureCanvasTkAgg(self.fig2, master=self.frame_graph2)
        self.canvas_graph2.get_tk_widget().pack(fill="both", expand=True)
        
        self.init_cases()
        self.init_sheeps()
        self.init_dog(0,0) 
        

    def restart_grid(self) : 
        """
        Fonction permettant de repositionner le chien et les moutons pour un nouvel épisode
        """
        self.reward = 0 
        self.current_perceived_state = [0, 0, 0]
        self.restart = False
        self.nb_steps = 0
        self.nb_trains_effectues = 1
        self.list_nb_steps = []
        self.rewards = []
        self.episode_reward = 0
        
        self.canvas.delete("all")
        self.init_cases()
        self.init_dog(0,0) 
        self.init_sheeps()
        
        

    def load_q_values(self):
        """
        Fonction permettant de charger des q_valeurs enregistrées lors d'un entraînement précédent
        """
        # Reading the q_values back from the file
        with open(self.pkl_file_q, "rb") as file:
            loaded_q = pkl.load(file)
            self.chien.q_value = loaded_q
        
        print(f"Deserialized q_values: {loaded_q}")           

    def update_plot_rewards(self):
        """
        Fonction de mise à jour du graphique des récompenses cumulées
        """
        new_x = range(len(self.rewards))
        self.line_ax1.set_data(new_x, self.rewards)
        self.ax1.relim()
        self.ax1.autoscale_view()
        self.canvas_graph1.draw_idle()

    def update_plot_steps(self):
        """
        Fonction de mise à jour du graphique des nombres de pas par épisode
        """
        new_x = range(len(self.list_nb_steps))
        self.line_ax2.set_data(new_x, self.list_nb_steps)
        
        list_nb_steps_lissee_x, list_nb_steps_lissee_y = self.lissage_nb_steps(10)
        self.line_lissee_ax2.set_data(list_nb_steps_lissee_x, list_nb_steps_lissee_y)
        
        self.ax2.relim()
        self.ax2.autoscale_view()
        self.canvas_graph2.draw_idle()
        
        

    def get_mean_sheeps(self):
        """
        Fonction permettant de retourner la position moyenne des moutons quel 
        que soit leur position

        Returns
        -------
        x_mean : float
        y_mean : float
        """
        x_mean = sum ([animal.x for animal in self.sheeps])/(len(self.sheeps))
        y_mean = sum ([animal.y for animal in self.sheeps])/(len(self.sheeps))
        return x_mean, y_mean

    def get_sheeps_door_distance(self):
        """
        Fonction permettant de déterminer la distance "discrète" des moutons 
        dans l'herbe à la porte'

        Returns
        -------
        res : int
        """
        log_file.write("\ndans get_sheeps_door_distance\n")
        log_file.flush()
        distance_max = 10 #obtenue sur ce cas particulier .... à adapter ....
        x_mean, y_mean = self.chien.get_mean_sheeps_grass()
        
        res = 0
        if x_mean != None :
            distance = math.sqrt((self.door[0].ind_ligne - x_mean)**2 + (self.door[0].ind_colonne - y_mean)**2)
            log_file.write("distance mouton - porte : {}\n".format(distance))
            log_file.flush()
            if distance_max / 4 > distance :
                res = 0
            elif distance_max / 2 > distance :
                res = 1
            elif distance_max * 3 / 4 > distance :
                res = 2   
            else :
                res = 3
            log_file.write("distance mouton - porte discrete: {}\n".format(res))
            log_file.flush()
        return res
    
    
    def get_nb_not_in_pen(self):
        """
        Fonction permettant de déterminer le nombre de moutons qui ne sont pas 
        dans l'enclos'
        """
        res = 0
        for sheep in self.sheeps : 
            if sheep.case.type == 'grass' :
                res += 1
        self.nb_not_in_pen = res
        
        
    def init_dog(self, _x, _y) :
        """
        Fonction permettant d'initialiser le chien à la position _x, _y'
        """
        # Create the dog, place it at (0, 0) and color it   
        self.chien = Chien(self, _x, _y, self.nb_sheeps+1, 'black')
        self.canvas.itemconfigure(self.chien.case.rect, fill=self.chien.color)
        self.chien.door = self.door

        
    def create_enclos_case(self, _position):
        """
        Fonction permettant de créer une case d'enclos à la position _position
        """        
        self.cases[_position[0]][_position[1]].color = 'grey'
        self.cases[_position[0]][_position[1]].type = 'enclos'

        
    def create_pen(self):
        """
        Fonction permettant de créer l'enclos avec sa porte
        """
        for i in range(3):
            for j in range (3):
                self.create_enclos_case([self.nb_lignes-1-i,j])
        self.cases[self.nb_lignes-1-2][2].color = 'yellow'
        self.cases[self.nb_lignes-1-2][2].type = 'door'
        self.door.append(self.cases[self.nb_lignes-1-2][2])


    def get_perceived_state(self):    
        """
        Fonction permettant de déterminer l'état perçu par le chien'

        Returns
        -------
        distance_sheeps_door : int
            Distance du centre de gravité des moutons encore dans l'herbe à la porte
        distance_sheeps_dog : int
            Distance du chien au centre de gravité des moutons encore dans l'herbe
        angle_troupeau : int
            Position relative porte - moutons - chien

        """
        #calcul de l'état perçu par la chien
        distance_sheeps_door = self.get_sheeps_door_distance()
               
        #recupérer la distance entre le chien et le troupeau
        distance_sheeps_dog = self.chien.sheeps_distance()
        
        #récupérer l'angle 'dicret' entre les vecteurs chien-porte et chien-centre_du_troupeau
        angle_troupeau = self.get_angle_troupeau()
        
        return distance_sheeps_door, distance_sheeps_dog, angle_troupeau
    
    
    def get_angle_troupeau(self) :
        """
        Fonction permettant de définir des positions relatives du chien, du centre de gravité des moutons dans l'herbe
        et de la porte
        """
        log_file.write("\ndans get_angle_troupeau\n")
        log_file.flush()
        
        res = 0
        
        x_mean_sheeps, y_mean_sheeps = self.get_mean_sheeps()
        
        if x_mean_sheeps != None : # s'il reste des moutons dans l'herbe
            
            #On calcule l'angle entre le vecteur chien - centre du troupeau
            vect_dog_sheeps, norme_vect_dog_sheeps = self.chien.get_dir_sheeps()
            log_file.write("vecteur du chien aux moutons : {} et norme {}\n".format(vect_dog_sheeps, norme_vect_dog_sheeps))
            log_file.flush()

            # on calcule le vecteur du chien à la porte
            vect_dog_door = [self.chien.door[0].ind_ligne-self.chien.x, self.chien.door[0].ind_colonne-self.chien.y]   
            
            norme_vect_dog_door = math.sqrt(vect_dog_door[0]**2+vect_dog_door[1]**2)
            if norme_vect_dog_door : 
                vect_dog_door = [vect_dog_door[0]/norme_vect_dog_door, vect_dog_door[1]/norme_vect_dog_door]
                
            log_file.write("vecteur du chien à la porte : {} et norme {}\n".format(vect_dog_door, norme_vect_dog_door))
            log_file.flush()                
    
            #on calcule le produit scalaire 
            produit_scalaire = vect_dog_sheeps[0]*vect_dog_door[0]+vect_dog_sheeps[1]*vect_dog_door[1]
            
            #on calcule le produit vectoriel
            produit_vectoriel = vect_dog_sheeps[0]*vect_dog_door[1]-vect_dog_sheeps[1]*vect_dog_door[0]
            
            #print("angle :", produit_scalaire, "norme chien-porte", norme_vect_dog_door, "norme chien-troupeau", norme_vect_dog_sheeps)
            log_file.write("produit scalaire : {}, norme chien-porte : {}, norme chien-troupeau {}\n".format(produit_scalaire, norme_vect_dog_door, norme_vect_dog_sheeps))
            log_file.flush()   
            

            res = 4
                
            if produit_scalaire > 0.8 :
                if norme_vect_dog_door > norme_vect_dog_sheeps :
                    res = 0
                else :
                    res = 3
            elif produit_scalaire < 0 :
                res = 4
            elif produit_vectoriel > 0 : 
                res = 1
            elif produit_vectoriel < 0 :
                res = 2   

            log_file.write("valeur discrète de l'angle : {}\n".format(res))
            log_file.flush()   
        return res

    def one_step(self):
        """
        Fonction permettant de gérer un pas d'apprentissage
        """
        # For the dog. Computes the components of its perceived state
        # and then choose an action and performs it.
        log_file.write("-----------------dans one_step-----------------------\n")
        log_file.flush()          
     
       
        
        log_file.write("position du chien : {}, {}\n".format(self.chien.x, self.chien.y))
        for sheep in self.sheeps :
            log_file.write("position du mouton numero {} : {}, {}\n".format(sheep.id, sheep.x, sheep.y))
        log_file.flush()
        
        #récupérer le nombre de moutons qu'il reste à ranger
        self.get_nb_not_in_pen()

        log_file.write("nombre de moutons en dehors de l'enclos : {}\n".format(self.nb_not_in_pen))
        log_file.flush()  
        
        self.current_perceived_state = self.get_perceived_state()
        
        log_file.write('état perçu par le chien : {}\n'.format(self.current_perceived_state))
        log_file.flush()
        
        #en fonction de l'état perçu on choisit l'action à réaliser pour maximiser ses gains
        action = self.chien.choose_action(self.current_perceived_state)  # changes the state of environment 
        log_file.write('action choisie par le chien : {}\n'.format(action))
        log_file.flush()

        
        #On tente de réaliser l'action
        action = self.chien.make_action(action)
        log_file.write('action réalisée par le chien : {}\n'.format(action))
        log_file.flush()

    
        # Then sheeps react to the new state
        #les moutons réagissent 
        
        shuffle(self.sheeps)               # Ordre aléatoire des moutons
        for sheep in self.sheeps :         # faire d'abord fuir tous les moutons ...
            # print(animal.id)
            sheep.move_far_dog()
            
        shuffle(self.sheeps)               # Ordre aléatoire des moutons
        for sheep in self.sheeps :         # puis les faire se regrouper ...
            sheep.one_step_move_mean()      
        
        # If the dog can make the action compute the new perceived state for dog
        
        #logger la nouvelle position des moutons
        for sheep in self.sheeps :
            log_file.write("position du mouton numero {} : {}, {}\n".format(sheep.id, sheep.x, sheep.y))
        log_file.flush()
        
        
        if action != None :
            
            self.nb_not_in_pen_before = self.nb_not_in_pen
            #récupérer le nombre de moutons qu'il reste à ranger après l'action menée
            self.get_nb_not_in_pen()

            log_file.write("nombre de moutons encore dans l'herbe après l'action du chien : {}".format(self.nb_not_in_pen))
            log_file.flush()
            
            self.new_perceived_state = self.get_perceived_state()
            log_file.write('nouvel état perçu par le chien : {}\n'.format(self.new_perceived_state))
            log_file.flush()            

            # Then compute reward for the dog
            self.reward = 0
            if self.nb_not_in_pen <= 0 :  # end of game
                self.reward = 20
                self.restart = True
            else : 
                if (self.nb_not_in_pen_before > self.nb_not_in_pen) : 
                    self.reward = 2 * (self.nb_not_in_pen_before - self.nb_not_in_pen)  
                # reward augmented of the number of sheeps gone through door at this time step
                if self.new_perceived_state[0] < self.current_perceived_state[0] :
                    self.reward += 1
                if self.new_perceived_state[2]==0 and self.new_perceived_state[2]==0 < self.current_perceived_state[2]  :
                    self.reward += 5
                if (self.new_perceived_state[2]==1 or self.new_perceived_state[2]==2) and (self.current_perceived_state[2]==3 or self.current_perceived_state[2]==4)  :
                    self.reward += 3
                    
                if (self.nb_not_in_pen_before <= self.nb_not_in_pen) : 
                    self.reward += -1
                if self.new_perceived_state[0] >= self.current_perceived_state[0] :
                    self.reward += -1
                if self.new_perceived_state[2] >= self.current_perceived_state[2] :
                    self.reward += -1
                    
            self.episode_reward += self.reward
                    

            log_file.write("recompense accordée au chien : {}\n".format(self.reward))
            log_file.flush()
            
            list_q_values = []
            new_state = self.new_perceived_state
            for act in self.chien.actions :
                list_q_values.append(self.chien.q_value[new_state[0]][new_state[1]][new_state[2]][act])
    
            next_action = self.chien.actions[np.argmax(list_q_values)] 
    
            self.chien.update_Q(self.current_perceived_state, action, self.new_perceived_state, next_action) 
        
            self.nb_steps += 1
            
            
        if not self.restart :
            #pass
            self.fenetre.after(self.frequence, self.one_step)
        else :
            
            print("train number : ", self.nb_trains_effectues, '--> nb_steps : ', self.nb_steps)

            self.list_nb_steps.append(self.nb_steps)
            self.rewards.append(self.episode_reward)
            
            self.episode_reward = 0
            
            self.r = np.maximum (((self.nb_trains - self.nb_trains_effectues)/self.nb_trains),0)
            self.chien.i_epsilon = (self.chien.epsilon- self.chien.epsilon_end) * self.r + self.chien.epsilon_end
            log_file.write("valeur de i_epsilon : {}\n".format(self.chien.i_epsilon))
            print("i_epsilon", self.chien.i_epsilon)
            
            if self.nb_trains_effectues < self.nb_trains :
                self.restart = False
                self.nb_trains_effectues += 1
                self.nb_steps = 0
                # on réinitialise les positions de tout le monde
                
                self.canvas.itemconfigure(self.chien.case.rect, fill=self.chien.case.color)
                self.cases[self.chien.x][self.chien.y].contain.remove(self.chien) 

                
                self.chien.x = self.chien.init_x
                self.chien.y = self.chien.init_y
                
                
                self.cases[self.chien.x][self.chien.y].contain.append(self.chien)
                self.chien.case = self.cases[self.chien.x][self.chien.y]
                self.canvas.itemconfigure(self.chien.case.rect, fill=self.chien.color) 
                
                for sheep in self.sheeps :
                    self.canvas.itemconfigure(sheep.case.rect, fill=sheep.case.color)
                    self.cases[sheep.x][sheep.y].contain.remove(sheep) 
                    
                    sheep.x = sheep.init_x
                    sheep.y = sheep.init_y
                    
                    
                    self.cases[sheep.x][sheep.y].contain.append(sheep)
                    sheep.case = self.cases[sheep.x][sheep.y]
                    self.canvas.itemconfigure(sheep.case.rect, fill=sheep.color) 
                    
                #puis on relance
                self.nb_steps = 0
                self.update_plot_rewards()
                self.update_plot_steps()
                self.fenetre.after(self.frequence, self.one_step)
                
            else :
                print("on a terminé l'entrainement on trace le graphe")
                print("q_value", self.chien.q_value)

                list_nb_steps_lissee_x, list_nb_steps_lissee_y = self.lissage_nb_steps(10)

                
                # Writing the q_values to a file using pickle
                with open(self.pkl_file_q, 'wb') as file:
                    pkl.dump(self.chien.q_value, file)
                    print(f'Object successfully saved to "{self.pkl_file_q}"')
                    
                    
                 
        
    def lissage_nb_steps(self, taille):
        """
        Fonction permettant de lisser la courbe des nombres de pas nécessaires suivant une taille de fenetre donnée
        """
        res_x = []
        res_y = []
        i = taille
        for nb_steps in self.list_nb_steps[taille:-taille+1]:
            res_y.append(sum(self.list_nb_steps[i-taille:i+taille+1])/len(self.list_nb_steps[i-taille:i+taille+1]))
            res_x.append(i)
            i+=1
        return res_x, res_y
    
    
    def __str__(self) : 
        """
        Fonction de conversion des cases en chaîne de caractères
        Représentation de la grille sous forme textuelle
        """
        res = ''
        for ligne_cases in self.cases :
            for case in ligne_cases :
                res += str(case) + '\t'
            res += '\n'
        return res
    
    def position_valide(self, _x, _y) :
        """
        Fonction permettant de tester si une position est valide ou non par rapport à la taille de la grille
        Parameters
        ----------
        _x : int
            valeur de ligne
        _y : int
            valeur de colonne

        Returns
        -------
        res : bool
            True si la case existe et False sinon

        """
        res = True
        if _x < 0 or _x >= self.nb_lignes or _y < 0 or _y >= self.nb_colonnes: 
            res = False
        return res
    
    def position_vide(self, _x, _y) :
        """
        Fonction permettant de tester si une position est vide ou non
        Parameters
        ----------
        _x : int
            valeur de ligne
        _y : int
            valeur de colonne

        Returns
        -------
        res : bool
            True si la case est vide et False sinon

        """        
        res = True
        if _x < 0 or _x >= self.nb_lignes or _y < 0 or _y >= self.nb_colonnes or self.cases[_x][_y].contain !=[] : 
            res = False
        return res   
    
    
    def init_voisines(self):
        """
        Fonction d'initialisation des cases voisines d'une case donnée
        C'est à dire des cases adjacentes vides du bon type
        """
        i = 0
        while i < len(self.cases):
            j = 0
            while j < len(self.cases[i]) :
                for val_i in [i-1,i,i+1]:
                    for val_j in [j-1,j,j+1]:
                        if [i,j] != [val_i,val_j] and self.position_valide(val_i, val_j) and (self.cases[i][j].type == 'door' or (self.cases[val_i][val_j].type == 'door' and self.cases[i][j].type == 'grass') or self.cases[i][j].type == self.cases[val_i][val_j].type):
                            self.cases[i][j].voisines.append(self.cases[val_i][val_j])
                j += 1
            i += 1


    def init_cases(self):
        """
        Fonction permettant d'initialiser la grille avec ses cases'
        """
        self.cases = []
        # Construct the board and its geometry (init_voisines)
        i = 0
        while i < self.nb_lignes :
            self.cases.append([])
            j = 0
            while j < self.nb_colonnes : 
                self.cases[-1].append(Case(self.case_size,i, j))
                j += 1
            i += 1
            
        self.create_pen()
            
        self.init_voisines()
        
        # Draw background
        for ligne_cases in self.cases :
            for une_case in ligne_cases :
                une_case.rect = self.canvas.create_rectangle(une_case.ind_ligne * une_case.size, une_case.ind_colonne * une_case.size, une_case.ind_ligne * une_case.size + une_case.size, une_case.ind_colonne * une_case.size+ une_case.size, fill=une_case.color)
    
    def init_sheeps(self):
        """
        Fonction permettant d'initialiser le troupeau de mouton dans l'herbe à
        des positions aléatoires

        """
        self.sheeps = []
        # Initialize the positions of the k sheeps
        
        k = 0
        while k < self.nb_sheeps : 
            ind_ligne = randint(0, self.nb_lignes-1)
            ind_colonne = randint(0, self.nb_colonnes-1)
            if (self.position_vide(ind_ligne, ind_colonne) and self.cases[ind_ligne][ind_colonne].type == 'grass') :
                self.sheeps.append(Mouton(self, ind_ligne,ind_colonne, k, 'white'))
                k += 1
         
        # Color the sheeps    
        for animal in self.sheeps :
            self.canvas.itemconfigure(animal.case.rect, fill=animal.color)
         

    

# =====================
# MAIN
# =====================
if __name__ == "__main__":
    nb_episodes = 2
    taille_grille = (10,10)
    nb_sheeps = 5
    freq = 2
    log_file = open("log_sheeps.txt", "w")
    
    print("Simulation avec", nb_episodes,"épisodes, une grille de taille", taille_grille, "et", nb_sheeps, "moutons")
    log_file.write ("Simulation avec {} épisodes, une grille de taille {} et {} moutons\n\n".format(nb_episodes,taille_grille,nb_sheeps))
    log_file.flush()
    
    env = Environnement(nb_episodes,taille_grille,nb_sheeps, _freq=freq)
     
    env.fenetre.mainloop()
    
    log_file.close()