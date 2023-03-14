List of modifications made to the venv libraries to enforce compatibility:

### Stable Baseline 3

common > monitor.py: added "termination/truncation" feature that is then combined into "done" boolean

common > vec_env > dummy_vec_env.py: added the obs/info decoupling on line 111-112

-> new _save_obs():
```py
    def _save_obs(self, env_idx: int, obs: VecEnvObs) -> None:
        if len(obs) == 2:
            obs = obs[0]
        for key in self.keys:
            if key is None:
                self.buf_obs[key][env_idx] = obs
            else:
                self.buf_obs[key][env_idx] = obs[key]
```

-> new step() in monitoring
```py
    def step(self, action: Union[np.ndarray, int]) -> GymStepReturn:
        """
        Step the environment with the given action

        :param action: the action
        :return: observation, reward, done, information
        """
        if self.needs_reset:
            raise RuntimeError("Tried to step environment that needs reset")
        observation, reward, terminated, truncated, info = self.env.step(action)
        done = terminated or truncated
        self.rewards.append(reward)
        if done:
            self.needs_reset = True
            ep_rew = sum(self.rewards)
            ep_len = len(self.rewards)
            ep_info = {"r": round(ep_rew, 6), "l": ep_len, "t": round(time.time() - self.t_start, 6)}
            for key in self.info_keywords:
                ep_info[key] = info[key]
            self.episode_returns.append(ep_rew)
            self.episode_lengths.append(ep_len)
            self.episode_times.append(time.time() - self.t_start)
            ep_info.update(self.current_reset_info)
            if self.results_writer:
                self.results_writer.write_row(ep_info)
            info["episode"] = ep_info
        self.total_steps += 1
        return observation, reward, done, info
````

### Gym

Added time_limit.py "temp" print statement (see wrappers folder)