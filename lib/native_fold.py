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

@profile
def native_fold(n):
    """Takes the previous n's path as input and attempts to add the next element in the sequence to the end of the path"""
    # load paths json if it exists 
    # try:
    #     with open('data/paths.json') as json_file:
    #         old_paths = rapidjson.loads(json_file)
    #         # Convert every path to a list of tuples
    #         if len(old_paths[0]) <= n:
    #             old_paths = [[tuple(point) for point in path] for path in old_paths]
    #         else:
    #             old_paths = [] # the info stored is too big - start from scratch

    # except:
    #     old_paths = []

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
    paths = [] # new paths to be generated
    cap_x = ceil(n/2) -1 
    def generate_paths(visited, path, idx=1):
        """Generate all possible paths of length n starting at (0, 0)"""
        if len(path) == n:
            paths.append(path)
            return

        for dir in dirs:
            new_x = path[-1][0] + dir[0]
            new_y = path[-1][1] + dir[1]
            cap_y = ceil((n/(abs(new_x)+1)) - 1) if abs(new_x) > 0 else cap_x
            #print("y", new_y)
           # print("cap_x", cap_x)
            if  abs(new_y) > cap_y or abs(new_x) > cap_x:
               # print("exit")
                continue
            elif (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                generate_paths(visited, path + [(new_x, new_y)], idx+1)
                visited.remove((new_x, new_y))

    generate_paths(set([(0, 0), (0,1)]), [(0, 0), (0, 1)], 2) # start at (0, 1) to avoid double counting
    
    # Plot the paths

    # for path in paths:
    #     x, y = zip(*path)
    #     plt.scatter(x, y)
    # plt.show()

# If the input path is empty start from scratch
    # if not old_paths:
    #     # generate_paths(set([(0, 0), (0,1)]), [(0, 0), (0, 1)]) # start at (0, 1) to avoid double counting
    #     old_paths = paths
    # else:
        # for idx, path in enumerate(old_paths):
            # Reassign that path to the new paths generated
            # print(path)
          #   generate_paths(set(tuple(path)), path)
            # del old_paths[idx]
            # old_paths.extend(paths)
            # paths = []
    
    # print("old paths:", old_paths)
    # Json serialize the path and save the file to the data folder
    # with open('data/paths.json', 'w') as outfile:
        # rapidjson.dumps(old_paths)
        
    return paths

def compute_energy(paths, sequence):
    """ Match the sequence to each paths and compute the energy. Return all minimum energy structures. Stores paths in a heap.
        H-H bond = -1
        P-P bond = 0
    """
    if len(paths) == 0:
        return False 
    if len(paths[0] != len(sequence)):
        return False

    # Create a heap to store the paths
    heap = []

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
    n = 25
    x = 0
    y = 0
    # G = generateWalks(n)
    
    paths = native_fold(n)
    print(len(paths))



        