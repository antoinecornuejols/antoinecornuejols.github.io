# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 11:04:14 2026

@author: ChM
"""

import matplotlib.pyplot as plt
import random as rd

plt.ion()
fig, ax = plt.subplots()

episodes = 100
rewards = []

for ep in range(episodes):

    total_reward = 0

    for _ in range(100):  
        reward = rd.randint(0,1)
        total_reward += reward

    rewards.append(total_reward)

    ax.clear()
    ax.plot(rewards)
    ax.set_title(f"Episode {ep}")
    ax.set_xlabel("Episodes")
    ax.set_ylabel("Reward")

    plt.pause(0.1)

plt.ioff()
plt.show()