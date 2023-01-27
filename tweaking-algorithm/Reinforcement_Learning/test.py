import gym
import rl_env

env = gym.make('rl_env/InverseFoldingEnv-v0', chain_length=10)
env.step(2)

