import gym
import numpy as np
from gym import spaces
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from placing_algorithm.saw_new.envs.saw import SAW
# Add your imports and paths here as needed

class RANDSAW(SAW):
    def __init__(self, length, render_mode=None) -> None:
        super().__init__(length, render_mode)

    def step(self, *args):
        action = self.action_space.sample()  # Choose a random action
        return super().step(action)