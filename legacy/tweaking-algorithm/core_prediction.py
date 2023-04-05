import gym
from  invenv.inv_env import register
from stable_baselines3 import PPO
import numpy as np

models_dir = "saved_weights"

env = gym.make('inv_fold/TweakWorld-v0')
env.reset()

model_path = f"{models_dir}/250000.zip"
model = PPO.load(model_path, env=env)

episodes = 5
target = np.array([[1, 1, 1], 
                   [2, 3, 4],
                   [1, 2, 3]])

for ep in range(episodes):
    _ = env.reset() # change this
    env.target_shape = target
    obs = env._get_obs()

    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        env.render()
        print(rewards)
    print(f'Final Sequence is: {env._seq_str}')