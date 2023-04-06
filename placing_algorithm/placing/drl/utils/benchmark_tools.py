from stable_baselines3.common.callbacks import BaseCallback
import numpy as np

class MetricsAccessCallback(BaseCallback):
    """
    Custom callback used when benchmarking models.
    It enables access to the reward at each steps and other useful metrics like
    degeneracy and energy difference.

    Deprecated because switch to Tensorboard
    """

    def __init__(self, training_length, verbose= 0):
        super().__init__(verbose)
        self.reward_hist = np.zeros((1, training_length))
        self.degen_hist = np.zeros((1, training_length))
        self.energy_dist_hist = np.zeros((1, training_length))


    def _on_step(self) -> bool:
        self.degen_hist[self.num_timesteps] = self.model.degen
        self.energy_dist_hist[self.num_timesteps] = self.model.energy_dist
        self.degen_hist[self.num_timesteps] = self.model.degen
        return super()._on_step()