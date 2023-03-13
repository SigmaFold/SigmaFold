import numpy as np 
import matplotlib.pyplot as plt

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


class QShape():
    def __init__(self, shape: np.ndarray, rat=(0,0)):
        """
        rat : represent the current position of the agent
        shape: the maze shape
        """
        
        self._shape = shape
        self.free_cells = np.argwhere(self._shape == 1.0)
        
        print(rat)
        
        if not rat in self.free_cells:
            raise ValueError("Start position is not in free cells - check the input shape") # will be removed when algorithm starts deciding start position
        
        self.reset(shape, rat)


    def reset(self, shape, rat):
        self.rat = rat
        self._shape = np.copy(shape)
        self.state = (rat[0], rat[1], 'start')
        row, col = self.rat
        self.min_reward = -1
        print("minimum reward:", self.min_reward)
        self.visited = set() #keeps track of cells visited
        # add starting postion 
        self.visited.add((row, col))
        self.total_reward = 0
        self._shape[row, col] = 0.0

    def update_state(self, action):
        nrow, ncol, nmode = rat_row, rat_col, mode = self.state
        if self._shape[rat_row, rat_col] > 0.0:
            self.visited.add((rat_row, rat_col))

        valid_actions = self.valid_actions()
                
        if not valid_actions:
            nmode = 'blocked' 
        elif action in valid_actions:
            nmode = 'valid'
            if action == LEFT:
                ncol -= 1
            elif action == UP:
                nrow -= 1
            if action == RIGHT:
                ncol += 1
            elif action == DOWN:
                nrow += 1
            self._shape[nrow, ncol] = 0.0

        else:                  # invalid action, no change in rat position
            nmode = 'invalid'

        # new state
        self.state = (nrow, ncol, nmode)
        print(self.state)
    def check_win(self):
        """
        In our implementation of the maze the AI wins if its successully painted all the maze
        """
        return np.all(self._shape == 0.0)
    
    def get_reward(self):
        rat_row, rat_col, mode = self.state
        nrows, ncols = self._shape.shape
        # if win, reward is 1
        if self.check_win():
            return - self.min_reward + 1
        if mode == 'blocked':
            return self.min_reward - 1
        if mode == 'invalid':
            return self.min_reward - 1
        if mode == 'valid':
            return 0.125
    
    def valid_actions(self, cell=None):
        if cell is None:
            cell = self.state
        valid = []
        nrows, ncols = self._shape.shape
        rat_row, rat_col, _ = cell
        print("rat_row:", rat_row, "rat_col:", rat_col)
        # Check edges, but also check if the cell is a wall, it is a wall if it is 0 in that case it is not a valid action. Also check if the cell is already visited
        if rat_row > 0 and self._shape[rat_row - 1, rat_col] > 0.0 and (rat_row - 1, rat_col) not in self.visited:
            valid.append(UP)
        if rat_row < nrows - 1 and self._shape[rat_row + 1, rat_col] > 0.0 and (rat_row + 1, rat_col) not in self.visited:
            valid.append(DOWN)
        if rat_col > 0 and self._shape[rat_row, rat_col - 1] > 0.0 and (rat_row, rat_col - 1) not in self.visited:
            valid.append(LEFT)
        if rat_col < ncols - 1 and self._shape[rat_row, rat_col + 1] > 0.0 and (rat_row, rat_col + 1) not in self.visited:
            valid.append(RIGHT)
        
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
        pass
        canvas = self.get_canvas()
        # Change to float
        #canvas = canvas.astype(float)
        # make visted cells 0.6
        #for row, col in self.visited:
            #canvas[row, col] = 0.6
        # make current cell 0.9
        #canvas[self.rat[0], self.rat[1]] = 0.9
        plt.imshow(canvas, interpolation='none', cmap='gray')
        plt.xticks([]), plt.yticks([])
        plt.show(block=False)
        plt.pause(0.1)
        plt.close()


if __name__ == "__main__":
    shape = QShape(np.array([
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    shape.act(RIGHT)
    shape.show()
    shape.act(RIGHT)
    shape.show()

    

        



            

        
    