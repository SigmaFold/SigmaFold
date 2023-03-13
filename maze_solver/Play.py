from Qshape import QShape
import numpy as np
import os, sys, time, datetime, json, random
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD , Adam, RMSprop
from keras.layers import PReLU
import matplotlib.pyplot as plt
from Experience import Experience
import signal
from copy import deepcopy
import time 
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Exploration factor
epsilon = 0.6

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

# Actions dictionary
actions_dict = {
    LEFT: 'left',
    UP: 'up',
    RIGHT: 'right',
    DOWN: 'down',
}

num_actions = len(actions_dict)

class Play:
    def __init__(self, maze, rat=(0,0), model=None):
        self.maze = maze
        self.qshape = QShape(maze, rat)
        self.rat = rat
        self.model = model
        # self.qshape.learn()

    def play(self):
        self.qshape.reset(self.rat)
        while True:
            prev_envstate = envstate
            # get next action
            q = self.model.predict(prev_envstate)
            action = np.argmax(q[0])

            # apply action, get rewards and new state
            envstate, reward, game_status = self.qshape.act(action)
            if game_status == 'win':
                return True
            elif game_status == 'lose':
                return False

def qtrain(model, maze, **opt):
    # TODO this has "maze" thingies
    global epsilon
    n_epoch = opt.get('n_epoch', 20)
    max_memory = opt.get('max_memory', 1000)
    data_size = opt.get('data_size', 50)
    weights_file = opt.get('weights_file', "")
    name = opt.get('name', 'model')
    start_time = datetime.datetime.now()

    # If you want to continue training from a previous model,
    # just supply the h5 file name to weights_file option
    if weights_file:
        print("loading weights from file: %s" % (weights_file,))
        model.load_weights(weights_file)
        time.sleep(1)
    # Construct environment/game from numpy array: maze (see above)
    # deepcopy maze to avoid mutating it 
    maze_input = deepcopy(maze)
    qmaze = QShape(maze_input)

    # Initialize experience replay object
    experience = Experience(model, max_memory=max_memory)

    win_history = []   # history of win/lose game
    n_free_cells = len(qmaze.free_cells)
    hsize = qmaze._shape.size//2   # history window size
    win_rate = 0.0
    imctr = 1

    for epoch in range(n_epoch):
        
        loss = 0.0
        rat_cell = (0,0)
        maze_input = deepcopy(maze)
        qmaze.reset(maze_input, rat_cell)
        game_over = False
        # get initial envstate (1d flattened canvas)
        envstate = qmaze.observe()
        n_episodes = 0
        while not game_over:
            valid_actions = qmaze.valid_actions()
            print("valid_actions: ", valid_actions)
            qmaze.show()
            if not valid_actions: break
            prev_envstate = envstate
            # Get next action
            if np.random.rand() < epsilon:
                action = random.choice(valid_actions)
                print("random action: ", action)
            else:
                action = np.argmax(experience.predict(prev_envstate))
                print("predicted action: ", action)

            # Apply action, get reward and new envstate
            envstate, reward, game_status = qmaze.act(action)
            if game_status == 'win':
                win_history.append(1)
                game_over = True
            elif game_status == 'lose':
                win_history.append(0)
                game_over = True
            else:
                game_over = False

            # Store episode (experience)
            episode = [prev_envstate, action, reward, envstate, game_over]
            experience.remember(episode)
            n_episodes += 1

            # Train neural network model
            inputs, targets = experience.get_data(data_size=data_size)
            h = model.fit(
                inputs,
                targets,
                epochs=8,
                batch_size=16,
                verbose=0,
            )
            loss = model.evaluate(inputs, targets, verbose=0)

        # if there has been at least one win, stop training
        if sum(win_history) > 0:
            break

        t = datetime.datetime.now() - start_time
        t = format_time(t.total_seconds())
        win_rate = 0


        template = "Epoch: {:03d}/{:d} | Loss: {:.4f} | Episodes: {:d} | Win count: {:d} | Win rate: {:.3f} | time: {}"
        print(template.format(epoch, n_epoch-1, loss, n_episodes, sum(win_history), win_rate, t))
        

    # Save trained model weights and architecture, this will be used by the visualization code
    h5file = name + ".h5"
    json_file = name + ".json"
    model.save_weights(h5file, overwrite=True)
    with open(json_file, "w") as outfile:
        json.dump(model.to_json(), outfile)
    end_time = datetime.datetime.now()
    dt = datetime.datetime.now() - start_time
    seconds = dt.total_seconds()
    t = format_time(seconds)
    print('files: %s, %s' % (h5file, json_file))
    print("n_epoch: %d, max_mem: %d, data: %d, time: %s" % (epoch, max_memory, data_size, t))
    return seconds

# This is a small utility for printing readable time strings:
def format_time(seconds):
    if seconds < 400:
        s = float(seconds)
        return "%.1f seconds" % (s,)
    elif seconds < 4000:
        m = seconds / 60.0
        return "%.2f minutes" % (m,)
    else:
        h = seconds / 3600.0
        return "%.2f hours" % (h,)
    
def build_model(maze, lr=0.001):
    model = Sequential()
    model.add(Dense(maze.size, input_shape=(maze.size,)))
    model.add(PReLU())
    model.add(Dense(maze.size))
    model.add(PReLU())
    model.add(Dense(num_actions))
    model.compile(optimizer='adam', loss='mse')
    return model

if __name__ ==  "__main__":
    shape = np.array([
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    # change to float
    shape = shape.astype(float)

    qshape = QShape(shape)
    # show(qshape)
    model = build_model(shape)
    player = Play(shape, (0,0), model)
    qtrain(model, shape, epochs=10, max_memory=8*shape.size, data_size=32, weights_file="model.h5", json_file="model.json")