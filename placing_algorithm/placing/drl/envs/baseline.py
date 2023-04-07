import gym
import numpy as np
from gym import spaces
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from placing_algorithm.placing.drl.envs.placing import Placing
# Add your imports and paths here as needed

class RANDHP(Placing):
    def __init__(self, length, render_mode=None) -> None:
        super().__init__(length, render_mode)

    def step(self, *args):
        pos_action = self.action_space['select_position'].sample()  # Choose a random position
        assign_action = self.action_space['assign'].sample()  # Choose a random assignment
        action = {'select_position': pos_action, 'assign': assign_action}
        return super().step(action)

    # You can override other methods as needed