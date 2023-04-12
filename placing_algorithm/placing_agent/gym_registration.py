import gym
from envs.placing import Placing


gym.register(
    id="Placing-v0",
    entry_point="placing_algorithm.placing_agent.envs.placing:Placing",
)

