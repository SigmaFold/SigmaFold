import sys
sys.path.append('c:\\users\\ec_pe\\onedrive - imperial college london\\dapp 3\\sigmafold')
print()
import gym
from stable_baselines3 import DQN
import matplotlib
# from invenv import register
# To test Gym registration:
from gym import envs
print(envs.registry.keys())

# def comparative_benchmark(model, baseline='sigma_env/RAND', episodes_nb=100_000, metrics='default'):
#     """
#     Function that plots the learning curve of a tested model against a baseline
#     model (by default, the RAND model). 
#     """

#     # Setup of the models
#     benchmarked_env = gym.make(model, 
#                                  max_episode_steps=50_000,
#                                  apply_api_compatibility=True,
#                                  disable_env_checker=False)
#     benchmarked_env.reset()
    
#     baseline_env = gym.make(baseline,
#                                 max_episode_steps=50_000,
#                                 apply_api_compatibility=True,
#                                 disable_env_checker=False)
#     baseline_env.reset()

#     benchmarked_model = DQN('MultiInputPolicy', benchmarked_env,
#                              learning_rate=1e-5, verbose=1, 
#                              tensorboard_log="./log/")
#     baseline_model = DQN('MultiInputPolicy', baseline_env,
#                              learning_rate=1e-5, verbose=1,
#                              tensorboard_log="./log/")

#     benchmarked_model.learn(total_timesteps=episodes_nb)
#     baseline_model.learn(total_timesteps=episodes_nb)

# def solo_benchmark(agent, env, net_arch, episodes_nb):
#     bm_env = gym.make(env, max_episode_steps=50_000, 
#                       apply_api_compatibility=True, disable_env_checker=False)
#     bm_env.reset()

#     bm_model = agent(net_arch, bm_env, 
#                      learning_rate=1e-5, verbose=1, tensorboard_log="./log")
    
#     bm_model.learn(total_timsteps=episodes_nb)

# if __name__=='__main__':
#     # solo_benchmark(DQN, 'sigma_env/Tweaking-v1', 'MultiInputPolicy', 100_000)
#     env = gym.make("sigma_env/Tweaking-v1")