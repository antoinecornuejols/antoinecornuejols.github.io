import numpy as np
import random
import matplotlib.pyplot as plt
import tkinter as tk
import time

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
# POLICY
# =====================
def epsilon_greedy(Q, state, epsilon):
    if random.uniform(0,1) < epsilon:
        return random.randint(0,3)
    return np.argmax(Q[state[0], state[1]])


# =====================
# TRAINING (LIVE PLOT)
# =====================
def train():
    env = GridWorld()
    Q = np.zeros((5, 5, 4)) #grille de taille 5x5 et 4 actions considérées

    alpha = 0.1
    gamma = 0.9
    epsilon = 0.1

    episodes = 300
    rewards = []

    plt.ion()
    fig, ax = plt.subplots()

    for ep in range(episodes):
        state = env.reset()
        total_reward = 0

        for _ in range(100):  #il fait 100 actions et on comptabilise combien il a gagné et s'il a atteint son but
            action = epsilon_greedy(Q, state, epsilon)
            next_state, reward, done = env.step(action)

            x, y = state
            nx, ny = next_state

            Q[x, y, action] += alpha * (
                reward + gamma * np.max(Q[nx, ny]) - Q[x, y, action]
            )

            state = next_state
            total_reward += reward

            if done:
                break

        rewards.append(total_reward)

        ax.clear()
        ax.plot(rewards)
        ax.set_title(f"Episode {ep}")
        ax.set_xlabel("Episodes")
        ax.set_ylabel("Reward")

        plt.pause(0.01)

    plt.ioff()
    plt.show()

    return Q, rewards


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
    Q, rewards = train()

    env = GridWorld()
    GridGUI(env, Q)
