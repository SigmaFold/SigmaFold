import gym
import numpy as np
from gym import spaces

class RootInverse(gym.Env):
    def __init__(self, base_num=2, seq_length=15) -> None:
        super().__init__()

        # Static attributes
        self.seq_length = seq_length
        self.base_num = base_num    # number of bases (H or P)

        # Dynamic attributes
        # self.sequence = np.array((2, seq_length))
        self.target = np.array((25, 25))    # target shape

        # Environment attributes
        low = np.array([0, 0, 0], dtype=np.float64)
        high = np.array([10000, 10000, 100], dtype=np.float64)

        self.action_space = spaces.Discrete(self.base_num*self.seq_length)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float64)

        # Reward related attributes
        # self.divergence = 10 # number of different bases
