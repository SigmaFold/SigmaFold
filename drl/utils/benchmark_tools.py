from stable_baselines3.common.callbacks import BaseCallback
import numpy as np

class MetricsAccessCallback(BaseCallback):
    """
    Custom callback used when benchmarking models.
    It enables access to the reward at each steps and other useful metrics like
    degeneracy and energy difference.
    """

    def __init__(self, training_length, verbose= 0):
        super().__init__(verbose)
        self.reward_hist = np.zeros((1, training_length))
        self.degen_hist = np.zeros((1, training_length))
        self.energy_dist_hist = np.zeros((1, training_length))
        

    def _on_step(self) -> bool:
        return super()._on_step()