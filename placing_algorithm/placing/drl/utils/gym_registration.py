import gym
from envs.placing import Placing


gym.register(
    id="Placing-v0",
    entry_point="placing_algorithm.placing.drl.envs.placing:Placing",
)

