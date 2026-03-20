import numpy as np
import random
import matplotlib.pyplot as plt
import tkinter as tk
import time
import pickle as pkl



# =====================
# ENVIRONMENT
# =====================
class GridWorld:
    def __init__(self, size=5):
        self.size = size
        self.start = (0, 0)
        self.goal = (4, 4)
        self.traps = [(1,1), (2,3), (3,1)]
        self.reset()

    def reset(self):
        self.state = self.start
        return self.state

    def step(self, action):
        x, y = self.state

        if action == 0:  # up
            x -= 1
        elif action == 1:  # down
            x += 1
        elif action == 2:  # left
            y -= 1
        elif action == 3:  # right
            y += 1

        x = max(0, min(self.size-1, x))
        y = max(0, min(self.size-1, y))

        new_state = (x, y)

        if new_state == self.goal:
            reward = 10
            done = True
        elif new_state in self.traps:
            reward = -10
            done = True
        else:
            reward = -1
            done = False

        self.state = new_state
        return new_state, reward, done


# =====================
# GUI
# =====================
CELL_SIZE = 60

class GridGUI:
    def __init__(self, env, Q):
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
        action = np.argmax(self.Q[self.env.state[0], self.env.state[1]])
        _, _, done = self.env.step(action)

        self.draw_grid()

        if not done:
            self.root.after(300, self.update)


# =====================
# MAIN
# =====================
if __name__ == "__main__":
    with open('toto.pkl', 'rb') as file:
        Q = pkl.load(file)
        print('Object successfully load')

    # on observe ses actions après apprentissage
    env = GridWorld()
    GridGUI(env, Q)
