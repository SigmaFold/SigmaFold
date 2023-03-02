List of modifications made to the venv libraries to enforce compatibility:

### Stable Baseline 3

common > monitor.py: added "termination/truncation" feature that is then combined into "done" boolean

common > vec_env > dummy_vec.py: added the obs/info decoupling on line 111-112

### Gym

Added time_limit.py "temp" print statement (see wrappers folder)