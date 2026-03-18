import numpy as np
import random as rd #sera utile pour la fonction epsilon_greedy
import tkinter as tk

class GridWorld:
    def __init__(self):
        """
        Constructeur de la classe GridWorld
        Permet de créer une grille dans une configuration précise : taille,
        position de l'objectif, des pièges, position initiale de l'agent, 
        état de l'agent

        Returns
        -------
        La grille
        
        """
        self.size = 5       # taille de la grille carrée
        self.start = (0,0)  # position de démarrage de l'agent
        self.goal = (4,4)   # potision de l'objectif à atteindre 
        self.traps = [(1,1),(2,3),(3,1)]    #positions des pièges
        self.reset()        # appel à la fonction d'initialisation de l'état de l'agent

    def reset(self):
        """
        Fonction permettant d'initialiser l'état de l'agent
        C'est-à-dire à la valeur de l'attribut start de la grille

        Returns
        -------
        L'état initial de l'agent 

        """
        self.state = self.start
        return self.state

    def step(self, action):
        """
        Fonction permettant de faire évoluer l'état de l'agent en fonction 
        de l'action qu'il réalise

        Parameters
        ----------
        action : entier
            Représente la direction qu'il veut prendre haut, bas, gauche, droite

        Returns
        -------
        list
            la nouvelle position de l'agent. Attention il ne doit pas sortir de la grille
        int
            ce qui lui rapporte cette action
        bool
            s'il a atteint ou non l'objectif

        """
        # TODO: à compléter
        return self.state, 0, False


def epsilon_greedy(Q, state, epsilon):
    """
    Fonction permettant de retourner l'action à réaliser étant donné :
        * l'état de l'agent
        * l'état actuel des q_valeurs
        * la valeur de epsilon qui règle la probabilité de choisir aléatoirement

    Parameters
    ----------
    Q : ndarray
        table à trois dimensions qui stocke les q_valeurs
    state : liste de deux valeurs entières
        position de l'agent dans la grille
    epsilon : float
        représente la probabilité de choisir aléatoirement l'action à mener

    Returns
    -------
    int : entier représentant l'action à réaliser'

    """
    # TODO: à compléter
    #return action # à définir dans la partie à compléter
    pass


def train():
    """
    Fonction permettant de réaliser l'apprentissage de l'agent dans la grille définie

    Returns
    -------
    Q : ndarray
        table à trois dimensions qui contient les q_valeurs à la fin des épisodes
        réalisés

    """
    env = GridWorld() #sera utilisé dans la partie à compléter
    Q = np.zeros((5,5,4))

    # TODO: à compléter

    return Q

# =====================
# GUI
# =====================
CELL_SIZE = 60

class GridGUI:
    def __init__(self, env, Q):
        """
        Constructeur d'une instance de représentation graphique de l'environnement
        tel que descrit ci-dessus et représenté par env
        Q représente la table à 3 dimensions des q_valeurs après entrainement
        """
        self.env = env
        self.Q = Q

        self.root = tk.Tk()
        self.root.title("GridWorld RL")

        self.canvas = tk.Canvas(
            self.root,
            width=env.size * CELL_SIZE,
            height=env.size * CELL_SIZE
        )
        self.canvas.pack()

        self.draw_grid()
        self.root.after(500, self.update)
        self.root.mainloop()

    def draw_grid(self):
        """
        Fonction permettant de dessiner les éléments de la grille 
        """
        self.canvas.delete("all")

        for i in range(self.env.size):
            for j in range(self.env.size):
                x0 = j * CELL_SIZE
                y0 = i * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE

                color = "white"

                if (i, j) == self.env.goal:
                    color = "green"
                elif (i, j) in self.env.traps:
                    color = "red"

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

        # draw agent
        x, y = self.env.state
        self.canvas.create_oval(
            y * CELL_SIZE + 10,
            x * CELL_SIZE + 10,
            y * CELL_SIZE + CELL_SIZE - 10,
            x * CELL_SIZE + CELL_SIZE - 10,
            fill="blue"
        )

    def update(self):
        """
        Fonction permettant de mettre à jour l'affichage après une itération 
        à partir de l'état courant 
        on choisit la meilleure action suivant Q
        on met à jour l'état courant

        Returns
        -------
        None.

        """
        done = False
        #TODO : à compléter pour déterminer l'action à mener à cette étape en fonction de la politique de l'agent
        # et en déduire le nouvel état de l'agent
        

        self.draw_grid()

        if not done: #done représente le fait d'avoir atteint ou l'objectif
            self.root.after(300, self.update)

if __name__ == "__main__":
    train()
