from gym.envs.registration import register

register(
    id="sigma_env/PrimWorld-v0",
    entry_point="inv_env.envs:PrimitiveInverseEnv",
)

register(
    id="sigma_env/TweakWorld-v0",
    entry_point="inv_env.envs:TweakingInverse",
)

register(
    id="sigma_env/RankTweakWorld-v0",
    entry_point="inv_env.envs:RankingReward",
)

register(
    id="sigma_env/SAW-v0",
    entry_point="inv_env.envs:SAW"
)