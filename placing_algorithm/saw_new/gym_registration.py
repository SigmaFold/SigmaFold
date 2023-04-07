import gym
from envs.saw import SAW


gym.register(
    id="SAW-v0",
    entry_point="placing_algorithm.saw_new.envs.saw:SAW",
)

