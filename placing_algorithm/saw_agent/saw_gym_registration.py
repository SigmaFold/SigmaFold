import gym
from envs.saw import SAW


gym.register(
    id="SAW-v0",
    entry_point="placing_algorithm.saw_agent.envs.saw:SAW",
)

gym.register(
    id="RAND-v0",
    entry_point="placing_algorithm.saw_agent.envs.baseline:RANDSAW",
)


gym.register(
    id="SAWValidation-v0",
    entry_point="placing_algorithm.saw_agent.envs.saw_validation_env:SAWValidation",
)
