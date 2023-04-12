import gym
import numpy as np
from gym import spaces
import os
import sys
import pygame
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from library.db_query_templates import get_training_dataset
from library.shape_helper import deserialize_path, deserialize_shape


class Placing(gym.Env):
    """
    Placing environment for the Folding@AmongUs project.
    """

    def __init__(self, length=None, render_mode=None, max_attempts=1, depth_field=1, shapes=None) -> None:
        super().__init__()
        if shapes is None:
            self.shapes = get_training_dataset(length) # if length is None, the dataset will be of variable lengths
        else:
            self.shapes = shapes
        # get the initial shape
        self.shapes = get_training_dataset(length) # new function that excludes validation shapes

        sample = self.shapes.sample(1)
        self.shape_id = sample.shape_id.iloc[0]
        self.correct_sequence = sample.best_sequence.iloc[0]
        self.path = deserialize_path(sample.optimal_path.iloc[0])
        self.curr_pos = self.path[0]
        self.curr_sequence = []  # where we will be storing hp assignments
        self.length = len(self.path) # path is now dynamic


        self.max_attempts = max_attempts
        # activates or deactivates the UI. Activated if set to "human"
        self.render_mode = render_mode
        self.num_actions = 0

        # Dynamic attributes
        self.attempts = 0
        self.cleared = False
        self.HP_matrix = deserialize_shape(self.shape_id)

        # this is to update the "field of view" of the agent - the number of neighbours it can see
        self.fov_area = (2*depth_field+1)**2
        print(f"FOV area: {self.fov_area}")
        self.dirs = self.generate_fov_vector(depth=depth_field, fov_area=self.fov_area) 
        
        # update actions pace size and observation space size
        self.action_space = spaces.MultiBinary(1)  # 2 HP assignments
        self.observation_space = spaces.MultiBinary((self.fov_area- 1)*2+2)  # fov_area neighbours with 2 HP assignment positions per neighbour + 2 positions for action space
        self.cleared_all = False

    def reset(self, options=None, seed=None):
        if self.cleared: # shape was cleared entirely correctly, remove it frol the training dataset.
            # drop and reset indexing
            print(f"Shape cleared, shapes remaining: {len(self.shapes)}")
            self.shapes = self.shapes.drop(self.shape_index)
            self.shapes = self.shapes.reset_index(drop=True)  
            if self.shapes.empty:
                # let it run on the previous shape to avoid errors but set the flag to true so that the training can stop after this episode
                self.cleared_all = True
                self.attempts = 0
            else:
                # resample a new shape
                self.sample_shape()
                self.attempts = 0
                
        elif self.attempts >= self.max_attempts:
            # get a new shape, unsuccessful clear
            self.sample_shape()
            self.attempts = 0
        
        else:
            # keep trying on current shape
            self.attempts += 1

        # resets HP matrix, current pos etc.
        self.reset_properties()

        # display target shaê
        if self.render_mode == "human":
            self.render_init()
        return self._get_obs()

    def step(self, action):
        # updating the current sequence with the action`
        action = int(action[0])
        actions_dict = {0: "H", 1: "P"}
        self.last_action = np.zeros((2, 1), dtype=int)
        self.last_action[action] = 1    # H is 10, P is 01
        residue = actions_dict[action]
        self.curr_sequence.append(residue)

        # updating the HP matrix according to action
        pos_action_col, pos_action_row = self.curr_pos
        assign_dict = {"H": 2, "P": 3}
        self.HP_matrix[pos_action_row, pos_action_col] = assign_dict[residue]
        

        # check reward
        reward, done = self.compute_reward()

        # render
        if self.render_mode == "human":
            self.render(pos_action_row, pos_action_col, residue)
            time.sleep(2)


        if not done:
            self.num_actions += 1
            self.curr_pos = self.path[self.num_actions]
        # get observation space
        obs = self._get_obs()
        return obs, reward, done, {}


    def render(self, pos_action_row, pos_action_col, residue):
        """
        Render the environment to the screen.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Create a new surface with transparency for the depth visualization
        depth_surface = pygame.Surface(self.shape_surface.get_size(), pygame.SRCALPHA)
        depth_surface.fill((0, 0, 0, 0))
        # Show the depth area around the agent in blue with 0.1 alpha
        for i in range(len(self.dirs)):
            pos_neighbour_col, pos_neighbour_row = self.curr_pos[0] + self.dirs[i][0], self.curr_pos[1] + self.dirs[i][1]
            pygame.draw.rect(depth_surface, (0, 0, 255, 100), (pos_neighbour_col*self.cell_size, pos_neighbour_row*self.cell_size, self.cell_size, self.cell_size))

        # Render the current pos as a green square overwriting the target shape
        if residue == "H":
            pygame.draw.circle(self.shape_surface, (0, 255, 0), (pos_action_col*self.cell_size, pos_action_row*self.cell_size), radius=self.cell_size/3)
        else:
            pygame.draw.circle(self.shape_surface, (0, 0, 255), (pos_action_col*self.cell_size, pos_action_row*self.cell_size), radius=self.cell_size/3)

        # Render the depth surface on top of the main surface
        self.screen.blit(depth_surface, (0, 0))
        pygame.display.flip()

    def _get_obs(self):
        """
        Get the observation of the environment.
        """
        neighbour_vector = self.find_neighbours()
        obs = np.vstack([self.last_action, neighbour_vector])

        return obs.flatten()


    def compute_reward(self):
        """
        If the current sequence is the same as the correct sequence then maximum reward.
        For every wrong residue, it is penalised -2.
        For every correct residue it is rewarded 0.1.
        For entirely correct sequence, it is rewardede 10
        olding matrix is the same as the target shape, then reward is 1.
        Else, reward is 0.
        """

        reward = 1/self.length
        done = False

        # agent is allowed to assign all residues before ending. No premature end for wrong assignment
        # penalise at every step
        if self.curr_sequence[self.num_actions - 1] != self.correct_sequence[self.num_actions - 1]:
            reward = -1/self.length

        if len(self.curr_sequence) == self.length:
            if "".join(self.curr_sequence) == self.correct_sequence:
                # reward = reward * 5
                # TODO: should I add a reward at the end? it'll make the graph less nice.
                print("Correct sequence found: ", self.curr_sequence)
                self.cleared = True
                done = True
            else:
                done = True

        return reward, done


    def find_neighbours(self):
        """
        Look at neighbours of the current position.
        00 - not connectable (either on the chain or a boundary)
        01 - conenctable and empty
        10 - H
        11  - P
        """
        # up, right, down and left dirs in matrix [m, n]. Diagonals do not matter.
        dirs = self.dirs
        neighbour_vector = np.zeros((len(dirs)*2, 1))
        x, y = self.curr_pos
        neighbours = [(y+a, x+b) for a, b in dirs]
        for idx, neighbour in enumerate(neighbours):
            # check HP matrix for residues
            H_or_P = self.HP_matrix[neighbour[0], neighbour[1]]
            if H_or_P == 2:
                #print(f"My neighbour {neighbour} is H")
                neighbour_vector[2*idx] = 1
                neighbour_vector[2*idx + 1] = 0
            elif H_or_P == 3:
                #print(f"My neighbour {neighbour} is P")
                neighbour_vector[2*idx] = 1
                neighbour_vector[2*idx + 1] = 1
            elif H_or_P == 0:
                #print(f"My neighbour {neighbour} is a boundary")
                neighbour_vector[2*idx] = 0
                neighbour_vector[2*idx + 1] = 0
            elif H_or_P == 1:
                #print(f"My neighbour {neighbour} is empty")
                neighbour_vector[2*idx] = 0
                neighbour_vector[2*idx + 1] = 1
            else:
                raise ValueError("Something went wrong lol cos this cant happen my guy")
            
        # get a window of 2 of the self.path around the self.num_actions
        lower  = max(0, self.num_actions - 1)
        upper = min(self.length - 1, self.num_actions + 1)
        window = self.path[lower:upper]

        for idx, neighbour in enumerate(neighbours):
            if neighbour in window:
                neighbour_vector[2*idx] = 0
                neighbour_vector[2*idx + 1] = 0 

                #print(f"Neighbour {neighbour} is not connectable") 

        #print(neighbour_vector)

        return neighbour_vector
    
    def sample_shape(self):
        """
        Sample a shape from the dataset.
        """
        sample = self.shapes.sample(1)
        self.shape_id = sample.shape_id.iloc[0]
        self.correct_sequence = sample.best_sequence.iloc[0]
        self.path = deserialize_path(sample.optimal_path.iloc[0])
        self.length = len(self.path)

    def reset_properties(self):
        """
        Reset the properties of the environment.
        """
        self.HP_matrix = deserialize_shape(self.shape_id)
        self.curr_pos = self.path[0]
        self.curr_sequence = []
        self.num_actions = 0
        self.last_action = np.zeros((2, 1))

    def render_init(self):
        pygame.init()
        self.screen_size = (500, 500)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('HP Visualization')
        self.cell_size = 20
        # Draw the target shape
        self.shape_surface = pygame.Surface(self.screen_size)
        self.shape_surface.fill((0, 0, 0))
        for i in range(25):
            for j in range(25):
                if self.HP_matrix[i, j] in [1, 2, 3]:
                    pygame.draw.rect(self.shape_surface, (255, 0, 0), (
                        j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.flip()
        self.screen.blit(self.shape_surface, (0, 0))

    @staticmethod
    def generate_fov_vector(depth, fov_area):
        """Method that generates the vector with all the relevant vision 
        directions depending on the depth_field attribute"""
        size = fov_area
        dirs = np.zeros((size, 2), dtype=int)
        counter = 0
        dirs_list = []

        for i in range(-depth, depth+1):
            for j in range(-depth, depth+1):
                dirs_list.append((i,j))
        
        dirs_list.remove((0,0))
        dirs = np.array(dirs_list)
        return dirs
    
if __name__ == "__main__":
    env = Placing(16)
    env.reset()

