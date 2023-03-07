from gym.envs.registration import register

register(
    id="inv_fold/PrimWorld-v0",
    entry_point="inv_env.envs:PrimitiveInverseEnv",
)

register(
    id="inv_fold/TweakWorld-v0",
    entry_point="inv_env.envs:TweakingInverse",
)
