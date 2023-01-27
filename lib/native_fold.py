# The fold will take paths at a previous n and attempt to add the next element in the sequence to the end of the path. If the path is valid, it will be added to the list of paths. 
# If the path is invalid, it will be discarded. 
# This will continue until the sequence is exhausted. 
# The energy of each path will be calculated and the path with the lowest energy will be returned.
import matplotlib.pyplot as plt
import rapidjson
import heapq
import cProfile, pstats, io



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
    try:
        with open('data/paths.json') as json_file:
            old_paths = rapidjson.loads(json_file)
            # Convert every path to a list of tuples
            if len(old_paths[0]) <= n:
                old_paths = [[tuple(point) for point in path] for path in old_paths]
            else:
                old_paths = [] # the info stored is too big - start from scratch

    except:
        old_paths = []

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    paths = [] # new paths to be generated

    def generate_paths(x, y, visited, path):
        if len(path) == n:
            paths.append(path)
            return
        else:
            for dir in dirs:
                new_x = x + dir[0]
                new_y = y + dir[1]
                if (new_x, new_y) not in visited:
                    visited.add((new_x, new_y))
                    generate_paths(new_x, new_y, visited, path + [(new_x, new_y)])
                    visited.remove((new_x, new_y))

        
    # If the input path is empty start from scratch
    if not old_paths:
        generate_paths(0, 1, set([(0, 0), (0,1)]), [(0, 0), (0, 1)]) # start at (0, 1) to avoid double counting
        old_paths = paths
    else:
        for idx, path in enumerate(old_paths):
            last_point = path[-1]
            # Reassign that path to the new paths generated
            # print(path)
            generate_paths(last_point[0], last_point[1], set(tuple(path)), path)
            del old_paths[idx]
            old_paths.extend(paths)
            paths = []
    
    # print("old paths:", old_paths)
    # Json serialize the path and save the file to the data folder
    with open('data/paths.json', 'w') as outfile:
        rapidjson.dumps(old_paths)
        
    return old_paths

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
    
    

    

        


if __name__ == "__main__":
    for i in range(5,20):
        print("n = ", i)
        native_fold(i)

        