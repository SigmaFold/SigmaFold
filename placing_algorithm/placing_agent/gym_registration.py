import gym
from envs.placing import Placing


gym.register(
    id="Placing-v0",
    entry_point="placing_algorithm.placing_agent.envs.placing:Placing",
)

gym.register(
    id="RANDHP-v0",
    entry_point="placing_algorithm.placing_agent.envs.baseline:RANDHP",
)


gym.register(
    id="PlacingValidation-v0",
    entry_point="placing_algorithm.placing_agent.envs.placing_validation_env:PlacingValidation",
)
