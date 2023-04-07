# Works... Need to change this to your own folder path
import sys
sys.path.append('c:/Users/ec_pe/OneDrive - Imperial College London/DAPP3/SigmaFold/')

import gym
from stable_baselines3 import DQN
from invenv.inv_env import register

# To test Gym registration
# from gym import envs
# print(envs.registry.keys())

def comparative_benchmark(model, baseline='sigma_env/RAND', episodes_nb=100_000, metrics='default'):
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

def standard_benchmark(
        benchmarked_env,
        agent,
        net_arch,
        net_params,
        training_length=100_000,
        name='auto'
        ):
    env = gym.make(id=benchmarked_env)
    model = agent(net_arch, env, **net_params, tensorboard_log=f"./logs/{name}")
    model.learn(training_length)

if __name__ == '__main__':
    # env = gym.make('sigma_env/TweakWorld-v0')
    default_params = {
        "learning_rate": 1e-5,
        "verbose": 1,
    }
    standard_benchmark('sigma_env/TweakWorld-v0', DQN, 'MultiInputPolicy', default_params, )
    
