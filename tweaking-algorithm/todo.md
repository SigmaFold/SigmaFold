Todo list:
- Build new env (file tweak_env already created) with following feature:
    1) better reward function
    2) new observation space with target_shape instead of target_sequence
    3) maybe redefine actions so that it cannot do 0 -> 0 (useless action) but that's probably more on the reward function side
    4) Change prediction file (should not be reset but instead target shape)

- Understand Deep RL policy and find/design a potentially better one than the default one we use (the 'MlpPolicy' one)

- Understand Deep RL agent and find a better one (A2C? PPO?). Check stable baseline docs cause we have to find an agent that is compatible with gym.spaces.Box and gym.spaces.Discrete at least (there is a table in the docs for that)

- Once all of this is done, we have to actually train the agent and test its performance (maybe use Tensorboard)


Improvement (maybe):
- to generate shapes, use pivot algo


Cool sites:

https://pythonprogramming.net/saving-and-loading-reinforcement-learning-stable-baselines-3-tutorial/

https://www.youtube.com/watch?v=dLP-2Y6yu70

