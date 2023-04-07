import gym

class DummyTest(gym.Env):
    def __init__(self) -> None:
        super().__init__()

    def step(self, action):
        return super().step(action)
    
    def reset(self, *, seed= None, options = None):
        return super().reset(seed=seed, options=options)
    
    def render(self):
        return super().render()
    
