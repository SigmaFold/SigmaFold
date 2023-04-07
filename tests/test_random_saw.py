import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from placing_algorithm.saw_new.envs.baseline import RANDSAW
import matplotlib.pyplot as plt

def test_run_random_agent_episodes():
    env = RANDSAW(length=10)
    num_episodes = 1

    for episode in range(num_episodes):
        obs = env.reset()
        done = False
        total_reward = 0
        num_steps = 0

        while not done:
            action = env.action_space.sample()  # Sample a random action
            obs, reward, done, info = env.step(action)
            print("Observation:", obs)

            total_reward += reward
            num_steps += 1

        print(f"Episode {episode + 1}: Total reward = {total_reward}, Steps = {num_steps}")


if __name__ == "__main__":
    test_run_random_agent_episodes()
