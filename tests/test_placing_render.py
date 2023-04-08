import time
import os
import sys
import pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from placing_algorithm.placing.drl.envs.baseline import RANDHP, Placing


def test_render():
    env = Placing(length=10, render_mode="human")
    actions = [[338, 1], [337, 0], [312, 1], [313, 0]]
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
