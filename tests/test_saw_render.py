import time
import os
import sys
import pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from placing_algorithm.saw_new.envs.baseline import RANDSAW, SAW


def test_render():
    env = SAW(length=10, render_mode=None)
    actions = [0, 2, 1, 3]
    obs = env.reset()
    # env.render()

    done = False
    step_count = 0
    running = False

    for action in actions:
        obs, reward, done, info = env.step(action)
        # env.render()
        step_count += 1
        print(f"Step {step_count}: Action = {action}, Reward = {reward}, Done = {done}")

    print("Test completed.")

if __name__ == "__main__":
    test_render()
