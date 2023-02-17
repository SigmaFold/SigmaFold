import gym
from  invenv.inv_env import register
from stable_baselines3 import PPO

models_dir = "saved_weights"

env = gym.make('inv_fold/TweakWorld-v0')
env.reset()

model_path = f"{models_dir}/250000.zip"
model = PPO.load(model_path, env=env)

episodes = 5

for ep in range(episodes):
    obs = env.reset() # change this
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        env.render()
        print(rewards)