from gym.envs.registration import register

register(
    id='rl_env/InverseFoldingEnv-v0',
    entry_point='rl_env.envs:InverseFoldingEnv',
    max_episode_steps=300,
)