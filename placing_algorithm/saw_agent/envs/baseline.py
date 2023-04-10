import gym
import numpy as np
from gym import spaces
import os, sys
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from placing_algorithm.saw_agent.envs.saw import SAW


class RANDSAW(SAW):
    def __init__(self, length=None, render_mode=None, max_attempts=1, depth_field=1, shapes=None) -> None:
        super().__init__(length, render_mode, max_attempts, depth_field, shapes)

    def step(self, *args):
        # to avoid bias due to the multibinary action space, sample from 01, 10
        choices = [np.array([0, 1]), np.array([1, 0])]
        action = choices[random.randint(0, 1)]  # Choose a random action
        
        return super().step(action)