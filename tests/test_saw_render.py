import time
import os
import sys
import pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from placing_algorithm.saw_new.envs.baseline import RANDSAW


def test_render():
    env = RANDSAW(length=10, render_mode="human")
    actions = [0, 1, 2, 3]
    obs = env.reset()
    env.render()

    done = False
    step_count = 0
    running = False

    for action in actions:
        obs, reward, done, info = env.step(action)
        env.render()
        step_count += 1
        print(f"Step {step_count}: Action = {action}, Reward = {reward}, Done = {done}")
        time.sleep(0.5)

    print("Test completed.")

if __name__ == "__main__":
    test_render()
