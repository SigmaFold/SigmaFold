# The fold will take paths at a previous n and attempt to add the next element in the sequence to the end of the path. If the path is valid, it will be added to the list of paths. 
# If the path is invalid, it will be discarded. 
# This will continue until the sequence is exhausted. 
# The energy of each path will be calculated and the path with the lowest energy will be returned.
import matplotlib.pyplot as plt
import rapidjson
import heapq
import cProfile, pstats, io
import networkx as nx
from math import ceil, floor
import numpy as np
def profile(fnc):
    
    """A decorator that uses cProfile to profile a function"""
    def inner(*args, **kwargs):
        
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner
def step_function(x):
    """Returns 1 if x > 0, 0 otherwise"""
    return 1 if x > 0 else 0

@profile
def native_fold(n):
    """Takes the previous n's path as input and attempts to add the next element in the sequence to the end of the path"""

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
    paths = [] # new paths to be generated
    cap_x = ceil(n/2) -1 

    #TODO: Optimise using numpy arrays for the visited set potentially
    def generate_paths(path, visited):
        """Generate all possible paths of length n starting at (0, 0)"""
        if len(path) == n:
            paths.append(path)
            return

        for dir in dirs:
            new_x = path[-1][0] + dir[0]
            new_y = path[-1][1] + dir[1]
            cap_y = ceil((n/(abs(new_x)+1)) - 1) if abs(new_x) > 0 else cap_x

            if  abs(new_y) > cap_y or abs(new_x) > cap_x:
                continue
            
            elif (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                generate_paths(path + [(new_x, new_y)], visited)
                visited.remove((new_x, new_y))

    generate_paths([(0, 0), (0, 1)], set([(0,1), (0,0)])) # start at (0, 1) to avoid double counting
    
    return paths

def get_neighbours(coord):
    # iterate over dirs and return list of neighbours
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbours = set()
    for dir in dirs:
        neighbours.add((coord[0] + dir[0], coord[1] + dir[1]))
    return neighbours

sequence ="PHPPHPPHP"

@profile
def compute_energy(paths, sequence):
    """ Match the sequence to each paths and compute the energy. Return all minimum energy structures. Stores paths in a heap.
        H-H bond = -1
        P-P bond = 0
    """

    # Create a heap to store the paths
    heap = []
    for path in paths:
        H_coords = []
        energy = 0
        j = -1 # tracks the last time we saw an H along the chain
        for i in range(n):
            if sequence[i] == 'H':
                # Compute the energy of interaction with any Hs before it
                curr_x, curr_y = path[i]
                if i == j+1: # that means that the last time we encountered an H, it was adjacent to the current H
                    for coord in H_coords[:-1]: # skip last element
                        distance = (curr_x - coord[0])**2 + (curr_y - coord[1])**2
                        if distance == 1:
                            energy -= 1
                        
                else:
                    for coord in H_coords:
                        distance = (curr_x - coord[0])**2 + (curr_y - coord[1])**2
                        if distance == 1:
                            energy -= 1
                H_coords.append((curr_x, curr_y))
                j = i
                
                       
    
        heapq.heappush(heap, (energy, path))

    return heap



def generateWalks(n):
    """Generates a graph of all possible walks of length n starting at (0,0). numbers te entire grid"""
    G = nx.DiGraph()
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
# travel to every node in the graph and add every neighbour and direction
    for x in range(-n, n):
        for y in range(-n+ abs(x), n- abs(x)):
            for dir in dirs:
                if (x + dir[0] < n and y + dir[1] < n):
                    G.add_edge((x, y), (x + dir[0], y + dir[1]), dir=dir)
                    # add edge between neighbours
    # add edge between (0,0) and (0,1)
    
    #nx.draw(G, with_labels=True)
    #plt.show()
    
    return G


    

        


if __name__ == "__main__":
    x = 0
    y = 0
    # G = generateWalks(n)
    sequence ="PHPPHPPH"
    n = len(sequence)
    paths = native_fold(n)
    heap = compute_energy(paths, sequence)
    # pop from heap until energy changes
    energy = heap[0][0]
    print(n)
    while heap[0][0] == energy:
        path = heapq.heappop(heap)
        # plot the path 
        x = [coord[0] for coord in path[1]]
        y = [coord[1] for coord in path[1]]
        # print h and p on graph
        for i in range(n):
            if sequence[i] == 'H':
                plt.text(x[i], y[i], 'H')
            else:
                plt.text(x[i], y[i], 'P')
        plt.plot(x, y, 'ro')
        plt.plot(x, y)
        plt.show()




        