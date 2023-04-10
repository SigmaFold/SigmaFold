import gym
from collections import defaultdict

class InfoCollectorWrapper(gym.Wrapper):

    def __init__(self, env: gym.Env) -> None:
        super().__init__(env)
        self.failure_modes = {
            'out_of_bound': 0,
            'self_cross': 0,
        }
        self.degen_counter = defaultdict(0)

    def step(self, action):
        obs, reward, terminated, info = self.env.step(action)
        if terminated:
            if info["termination_info"] == "self_cross": # failed
                self.failure_modes["self_cross"] += 1
            elif info["termination_info"] == "out_of_bound": # failed
                self.failure_modes["out_of_bound"] += 1
            else: # success
                self.degen_counter[info["termination_info"]] += 1
        
        return obs, reward, terminated, info

