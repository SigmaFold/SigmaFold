import gym
import numpy as np
from gym import spaces
import os
import sys
import pygame
import time
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from library.db_query_templates import get_random_shape, get_all_sequences_for_shape
from library.shape_helper import path_to_shape_numbered, deserialize_path


class Placing(gym.Env):
    """
    Placing environment for the Folding@AmongUs project.
    """

    def __init__(self, length, render_mode=None) -> None:
        super().__init__()

        # Static attributes
        self.length = length
        self.target_shape = np.array((25, 25))
        self.path_shape = np.array((25, 25))
        self.correctHPassignments = np.array((25, 25))
        self.render_mode = render_mode # activates or deativates the UI. Activated if set to "human"

        # Dynamic attributes
        self.HPassignments = np.ndarray(shape=(25, 25))
        self.num_actions = 0
        # self.starting_pos = np.ndarray(shape=(2,))
        # self.cuurent_pos = tuple()
        # self.folding_onehot = np.ndarray(shape=(4, length)) # one-hot encoding of the SAW
        # self.folding_matrix = np.ndarray(shape=(25, 25)) # as a visual matrix
        # self.curr_length = int()

        # Spaces
        observation_dict = {
            'target': spaces.Box(0, 1, shape=(25, 25), dtype=np.uint8),
            'path': spaces.Box(0, self.length, shape=(25, 25), dtype=np.uint8),
            'HPassignments': spaces.Box(0, 2, shape=(25, 25), dtype=np.uint8),
        }

        action_dict = {
            'select_position': spaces.Box(0, 25, shape=(2,)),
            'assign': spaces.Discrete(2),
        }

        self.action_space = spaces.Dict(action_dict)
        self.observation_space = spaces.Dict(observation_dict)

    def generate_path(self, shape_id):
        # get all sequences for the target shape
        sequences = get_all_sequences_for_shape(shape_id)
        # sort sequences by degeneracy in an ascending order and save the first one's sequence and path
        sequences = sequences.sort_values(by=["degeneracy"], ascending=True)
        best_sequence = sequences.iloc[0]
        sequence = best_sequence["sequence"]
        path = best_sequence["path"]
        path = deserialize_path(path)   # convert path string into list of tuples
        path_mat, HP_mat, _ = path_to_shape_numbered(path, sequence)    # convert path into a numbered matrix
        return path_mat, HP_mat, sequence

    def reset(self, options=None, seed=None):
        self.target_shape, shape_id = get_random_shape(self.length)
        self.path_shape, self.correctHPassignments, _ = self.generate_path(shape_id)
        self.HPassignments = np.zeros((25, 25))

        if self.render_mode == "human":
            pygame.init()
            self.screen_size = (500, 500)
            self.screen = pygame.display.set_mode(self.screen_size)
            pygame.display.set_caption('HP Visualization')
            self.cell_size = 20
            # Draw the target shape
            self.shape_surface = pygame.Surface(self.screen_size)
            self.shape_surface.fill((0,0,0))
            for i in range(25):
                for j in range(25):
                    if self.target_shape[i, j] == 1:
                        pygame.draw.rect(self.shape_surface, (255,0,0), (j*self.cell_size, i*self.cell_size, self.cell_size, self.cell_size))

            pygame.display.flip()
            self.screen.blit(self.shape_surface, (0,0))
        return self._get_obs()

    def step(self, action):
        self.num_actions += 1
        pos_action = action['select_position']
        assign_action = action['assign']
        pos_action = math.floor(pos_action[0]), math.floor(pos_action[1])
        self.HPassignments[pos_action[0], pos_action[1]] = assign_action + 1
        obs = self._get_obs()
        self.render(pos_action, assign_action)
        reward, done = self.compute_reward(pos_action)
        return obs, reward, done, {}

    def render(self, pos_action, assign_action):
        """
        Render the environment to the screen.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # render the current pos as a green square overwriting the target shape
        if assign_action == 0:
            pygame.draw.circle(self.shape_surface, (0,255,0), (pos_action[0]*self.cell_size, pos_action[1]*self.cell_size), radius=self.cell_size/2)
        else:
            pygame.draw.circle(self.shape_surface, (0,0,255), (pos_action[0]*self.cell_size, pos_action[1]*self.cell_size), radius=self.cell_size/2)
        
        self.screen.blit(self.shape_surface, (0,0))      
        time.sleep(2)
        pygame.display.flip()

    def _get_obs(self):
        """
        Get the observation of the environment.
        """
        # IMPORTANT, SET THE DATATYPE TO BE CORRECT HERE !
        obs = {
            'target': self.target_shape.astype(np.uint8),
            'path': self.path_shape.astype(np.uint8),
            'HPassignments': self.HPassignments.astype(np.uint8),#
            #TODO temporarily removed the starting pos from the observation in case its not relevant. add and compare results
            #TODO: Shoild we add the folding matrix to the observation?
        }
        print("obs", obs)
        return obs
        
        
        obs = {
            'target': self.target_shape,
            'path': self.path_shape,
            'HPassignments': self.HPassignments,
        }
        return obs

    def compute_reward(self, pos_action):
        """
        If the folding matrix is the same as the target shape, then reward is 1.
        Else, reward is 0.
        """
        reward = 0
        done = False
        diff_matrix  = self.correctHPassignments - self.HPassignments
        
        # sum absolute values of all the elements in diff_matrix and normalise it
        sum = np.sum(abs(diff_matrix)) / self.length
        
        # fail immediately if out of bounds
        if self.correctHPassignments[pos_action[0], pos_action[1]] == 0:
            reward = -1
            done = True
        
        # if any element is equal to -1 then something was placed out of bounds 
        if self.num_actions == self.length:
            reward = ((1-sum)-0.5)*2
            done = True
        return reward, done
    

if __name__ == "__main__":
    mat = np.array([[-1, 2, 3], [-4, 5, 6], [7, 8, 9]])
    sum = np.sum(abs(mat))
    print(sum)

    x = [1.1, 2, 3.7]
    print(math.floor(x))

