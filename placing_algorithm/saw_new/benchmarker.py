import gym
import envs
from stable_baselines3 import DQN
import matplotlib

# To test Gym registration
# from gym import envs
# print(envs.registry.keys())

def benchmark(model, baseline='RAND', episodes_nb=100_000, metrics='default'):
    """
    Function that plots the learning curve of a tested model against a baseline
    model (by default, the RAND model). 
    """

    # Setup of the models
    benchmarked_env = gym.make(model, 
                                 max_episode_steps=50_000,
                                 apply_api_compatibility=True,
                                 disable_env_checker=False)
    benchmarked_env.reset()
    
    baseline_env = gym.make(baseline,
                                max_episode_steps=50_000,
                                apply_api_compatibility=True,
                                disable_env_checker=False)
    baseline_env.reset()

    benchmarked_model = DQN('MultiInputPolicy', benchmarked_env,
                             learning_rate=1e-5, verbose=1, 
                             tensorboard_log="./log/")
    baseline_model = DQN('MultiInputPolicy', baseline_env,
                             learning_rate=1e-5, verbose=1,
                             tensorboard_log="./log/")

    benchmarked_model.learn(total_timesteps=episodes_nb)
    baseline_model.learn(total_timesteps=episodes_nb)

benchmark(model='??')