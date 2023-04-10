import gym
from sb3_contrib import RecurrentPPO
from stable_baselines3.common.evaluation import evaluate_policy


def validate_saw(filename):
    model = RecurrentPPO.load(f'./logs/{filename}')
    mean_reward, std_reward = evaluate_policy(RecurrentPPO, env, n_eval_episodes=10)


