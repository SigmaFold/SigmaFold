import numpy as np 
import matplotlib.pyplot as plt
from copy import deepcopy
import cv2
from settings import * 
global img 
global imgtk
global root


class QShape():
    def __init__(self, shape: np.ndarray, rat=(0,0)):
        """
        rat : represent the current position of the agent
        shape: the maze shape
        """
        
        self._shape = shape
        self.free_cells = np.argwhere(self._shape == 1.0)
        
        if not rat in self.free_cells:
            raise ValueError("Start position is not in free cells - check the input shape") # will be removed when algorithm starts deciding start position
        
        self.reset(shape, rat)
        

    def reset(self, shape, rat):
        self.rat = rat
        self._shape = np.copy(shape)
        self.state = (rat[0], rat[1], 'start')
        row, col = self.rat
        self.min_reward = -1
        self.visited = set() #keeps track of cells visited
        self.total_reward = 0

    def update_state(self, action):
        nrow, ncol, nmode = rat_row, rat_col, _ = self.state
        if self._shape[rat_row, rat_col] > 0.0 and nmode != "start":
            self.visited.add((rat_row, rat_col))

        valid_actions = self.valid_actions()
        moving = [NOTHING_LEFT, NOTHING_RIGHT, NOTHING_UP, NOTHING_DOWN]
        placing = [LEFT, UP, RIGHT, DOWN]

        actions = {LEFT: (rat_row, rat_col - 1),
                    UP: (rat_row - 1, rat_col),
                    RIGHT: (rat_row, rat_col + 1),
                    DOWN: (rat_row + 1, rat_col),
                    NOTHING_LEFT : (rat_row, rat_col - 1),
                    NOTHING_RIGHT : (rat_row, rat_col + 1),
                    NOTHING_UP : (rat_row - 1, rat_col),
                    NOTHING_DOWN : (rat_row + 1, rat_col)
                }
        if not valid_actions:
            nmode = 'blocked' 
        
        elif action in valid_actions and action in placing:
            nmode = 'valid'
            nrow, ncol = actions[action]
            self._shape[nrow, ncol] = 0.0
            if self.is_going_to_be_blocked():
                print("blocked")
                nmode = "blocked"
        
        elif action in valid_actions and action in moving:
            nmode = "start"
            nrow, ncol = actions[action]

        else:                  # invalid action, no change in rat position
            nmode = 'invalid'

        # new state
        self.state = (nrow, ncol, nmode)
    def check_win(self):
        """
        In our implementation of the maze the AI wins if its successully painted all the maze
        """
        return "win" if np.all(self._shape == 0.0) else False
    
    def get_reward(self):
        _, _, mode = self.state

        rewards = {
            'start': 0,
            'blocked': -1,
            'invalid': -1,
            'valid': 0.125,
            "win": 1
        }

        return rewards[mode]

    def is_going_to_be_blocked(self):
        """Uses connected component labelling to figure out whether a move will get the rat to isolate a part of the maze. If so, will make the rat fail early."""
        # get the number of connected components
        num_labels, _ = cv2.connectedComponents(self._shape.astype(np.uint8))
        # if there is only one connected component then the rat is blocked
        if num_labels == 2:
            return False # only 2 components, the background and the shape
        else:
            return True
        
        
    def valid_actions(self, cell=None):
        if cell is None:
            cell = self.state
        
        # get the current mode 
        rat_row, rat_col, mode = cell
        valid = []
        nrows, ncols = self._shape.shape
        # Check edges, but also check if the cell is a wall, it is a wall if it is 0 in that case it is not a valid action. Also check if the cell is already visited
        if rat_row > 0 and self._shape[rat_row - 1, rat_col] > 0.0 and (rat_row - 1, rat_col) not in self.visited:
            valid.append(UP)
            if mode == 'start':
                valid.append(NOTHING_UP)
        if rat_row < nrows - 1 and self._shape[rat_row + 1, rat_col] > 0.0 and (rat_row + 1, rat_col) not in self.visited:
            valid.append(DOWN)
            if mode == 'start':
                valid.append(NOTHING_DOWN)

        if rat_col > 0 and self._shape[rat_row, rat_col - 1] > 0.0 and (rat_row, rat_col - 1) not in self.visited:
            valid.append(LEFT)
            if mode == 'start':
                valid.append(NOTHING_LEFT)

        if rat_col < ncols - 1 and self._shape[rat_row, rat_col + 1] > 0.0 and (rat_row, rat_col + 1) not in self.visited:
            valid.append(RIGHT)
            if mode == 'start':
                valid.append(NOTHING_RIGHT)
        
        return valid
    
    def act(self, action):
        self.update_state(action)
        reward = self.get_reward()
        self.total_reward += reward
        envstate = self.observe()
        status = self.status()
        print(" Status:", status)


        return envstate, reward, status
    
    def observe(self):
        canvas = self.get_canvas()
        envstate = canvas.reshape((1, -1))
        print(envstate)
        return envstate
    
    
    def get_canvas(self):
        """ This function returns a version of the array that you can call imshow on."""
        canvas = np.copy(self._shape)
        return canvas

    def status(self):
        print("Total Reward", self.total_reward)
        print("Minimum Reward", self.min_reward)
        if self.check_win():
            print("Game won!")
            return 'win'
        elif self.total_reward < self.min_reward:
            return 'lose'
        #print("Total Reward", self.total_reward)
        return 'not_over'

    def show(self):
        canvas = self.get_canvas()
        # plot as matlotlib animation 
        plt.imshow(canvas, interpolation='none', cmap='gray')
        plt.xticks([])
        plt.yticks([])
        plt.show()
        



if __name__ == "__main__":
    shape = QShape(np.array([
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]))
    # Change to float
    shape._shape = shape._shape.astype(float)
    shape.show()
    print("valid_actions", shape.valid_actions())
    shape.act(NOTHING_RIGHT)
    print("Curent postion", shape.state)
    shape.show()
    shape.act(RIGHT)
    shape.show()
    shape.act(LEFT)
    print("Curent postion", shape.state)
    shape.show()

    

        



            

        
    