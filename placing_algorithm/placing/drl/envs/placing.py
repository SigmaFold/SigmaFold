import gym
import numpy as np
from gym import spaces
import os
import sys
import pygame
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from library.db_query_templates import get_all_random_shapes
from library.shape_helper import deserialize_path, deserialize_shape


class Placing(gym.Env):
    """
    Placing environment for the Folding@AmongUs project.
    """

    def __init__(self, length, max_attempts=1, render_mode=None) -> None:
        super().__init__()

        # get the initial shape
        self.shapes = get_all_random_shapes(length)
        sample = self.shapes.sample(1)
        self.shape_id = sample.shape_id.iloc[0]
        self.correct_sequence = sample.best_sequence.iloc[0]
        self.path = deserialize_path(sample.optimal_path.iloc[0])
        self.curr_pos = self.path[0]

        self.curr_sequence = []  # where we will be storing hp assignments

        # Static attributes
        self.length = length
        self.max_attempts = max_attempts
        # activates or deactivates the UI. Activated if set to "human"
        self.render_mode = render_mode
        self.num_actions = 0

        # Dynamic attributes
        self.attempts = 0
        self.cleared = False
        self.HP_matrix = deserialize_shape(self.shape_id)

        self.action_space = spaces.MultiBinary(1)  # 2 HP assignments
        self.observation_space = spaces.MultiBinary(10)  # 4 neighbours + 2 HP assignments

    def reset(self, options=None, seed=None):
        if self.shapes.empty:
            self.reset = self.dummy_reset
            self.step = self.dummy_step
        elif self.attempts >= self.max_attempts or self.cleared:
            sample = self.shapes.sample(1)
            self.shape_id = sample.shape_id.iloc[0]
            self.correct_sequence = sample.best_sequence.iloc[0]
            self.path = deserialize_path(sample.optimal_path.iloc[0])
            self.attempts = 0
            self.cleared = False
        else:
            self.attempts += 1

        self.HP_matrix = deserialize_shape(self.shape_id)
        self.curr_pos = self.path[0]
        self.curr_sequence = []
        self.num_actions = 0
        self.last_action = np.zeros((2, 1))

        if self.render_mode == "human":
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
        return self._get_obs()

    def step(self, action):
        # updating the current sequence with the action`
        action = action[0]
        actions_dict = {0: "H", 1: "P"}
        self.last_action = np.zeros((2, 1), dtype=int)
        self.last_action[action] = 1    # H is 10, P is 01
        residue = actions_dict[action]
        self.curr_sequence.append(residue)

        # updating the HP matrix according to action
        pos_action_col, pos_action_row = self.curr_pos
        assign_dict = {"H": 2, "P": 3}
        self.HP_matrix[pos_action_row, pos_action_col] = assign_dict[residue]

        # updating the current position
        self.num_actions += 1
        self.curr_pos = self.path[self.num_actions]

        # render
        if self.render_mode == "human":
            self.render(pos_action_row, pos_action_col, residue)

        # check reward
        reward, done = self.compute_reward()
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
        
        # render the current pos as a green square overwriting the target shape
        if residue == "H":
            pygame.draw.circle(self.shape_surface, (0, 255, 0), (
                pos_action_col*self.cell_size, pos_action_row*self.cell_size), radius=self.cell_size/3)
        else:
            pygame.draw.circle(self.shape_surface, (0, 0, 255), (
                pos_action_col*self.cell_size, pos_action_row*self.cell_size), radius=self.cell_size/3)
        time.sleep(3)
        self.screen.blit(self.shape_surface, (0, 0))
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

        reward = 0.1
        done = False

        # agent is allowed to assign all residues before ending. No premature end for wrong assignment
        # penalise at every step
        if self.curr_sequence[self.num_actions - 1] != self.correct_sequence[self.num_actions - 1]:
            reward = -2

        if self.num_actions >= self.length - 1:
            if "".join(self.curr_sequence) == self.correct_sequence:
                reward = 10
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
        neighbour_vector = np.zeros((8, 1), dtype=int)

        
        # up, right, down and left dirs in matrix [m, n]. Diagonals do not matter.
        dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        x, y = self.curr_pos
        neighbours = [(y+a, x+b) for a, b in dirs]
        print(neighbours)
        print(self.HP_matrix)
        for idx, neighbour in enumerate(neighbours):
            # check HP matrix for residues
            H_or_P = self.HP_matrix[neighbour[0], neighbour[1]]
            if H_or_P == 2:
                print(f"My neighbour {neighbour} is H")
                neighbour_vector[2*idx] = 1
                neighbour_vector[2*idx + 1] = 0
            elif H_or_P == 3:
                print(f"My neighbour {neighbour} is P")
                neighbour_vector[2*idx] = 1
                neighbour_vector[2*idx + 1] = 1
            elif H_or_P == 0:
                print(f"My neighbour {neighbour} is a boundary")
                neighbour_vector[2*idx] = 0
                neighbour_vector[2*idx + 1] = 0
            elif H_or_P == 1:
                print(f"My neighbour {neighbour} is empty")
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

                print(f"Neighbour {neighbour} is not connectable") 

        print(neighbour_vector)

        return neighbour_vector


if __name__ == "__main__":
    env = Placing(16)
    env.reset()

