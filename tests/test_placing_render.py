import time
import os
import sys
import pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from placing_algorithm.placing.drl.envs.baseline import RANDHP, Placing


def test_render():
    env = Placing(length=10, render_mode="human")
    actions = [{'select_position': [13,13], 'assign': 1}, 
               {'select_position': [12,13], 'assign': 0}, 
               {'select_position': [12,12], 'assign': 1}, 
               {'select_position': [13,12], 'assign': 0}]
    obs = env.reset()
    env.render(actions[0]['select_position'], actions[0]['assign'])

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
