import time
import os
import sys
import numpy as np
import pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from placing_algorithm.placing_agent.drl.envs.baseline import RANDHP, Placing


def test_render():
    env = Placing(length=16, render_mode="human")
    # generate 16 random actions as numpy array containing a 1 or 0
    actions = np.random.randint(2, size=(16, 1))

    obs = env.reset()

    done = False
    step_count = 0
    running = False

    for action in actions:
        obs, reward, done, info = env.step(action)
        step_count += 1
        print(f"Step {step_count}: Action = {action}, Reward = {reward}, Done = {done}")

    print("Test completed.")

if __name__ == "__main__":
    test_render()
