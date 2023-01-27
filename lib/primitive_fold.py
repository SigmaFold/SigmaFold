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
    input_sequence = "ukacbdbv"
    print(input_sequence)

    origin = (0, 0)
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    visited = set()

    # generate every possible path of length n going through coordinates x,y
    paths = []

    def generate_paths(x, y, visited, path):
        if len(path) < n:
            if origin not in path:
                path.append(origin)

            visited.add(origin)
            for dir in dirs:
                new_x = x + dir[0]
                new_y = y + dir[1]
                if (new_x, new_y) not in visited:
                    visited.add((new_x, new_y))
                    generate_paths(new_x, new_y, visited, path + [(new_x, new_y)])
                    visited.remove((new_x, new_y))
        else:
            paths.append(path)

    generate_paths(0, 0, visited, [])
    # print("Total Possible Paths ====  > ", len(paths))

    # map each element in each path to the corresponding element in the input sequence
    paths = [list(zip(path, input_sequence)) for path in paths]

    # Define densitu as the number of neighbours between points within a path. sum 1 for each neighbour
    def get_neighbours(x, y):
        neighbours = []
        # create list of directions with diagonals
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        for dir in dirs:
            new_x = x + dir[0]
            new_y = y + dir[1]
            neighbours.append((new_x, new_y))
        return neighbours

    # sum all neighbours where second element of tuple is H
    def get_energy(path):
        energy = 0
        for idx, point in enumerate(path):
            if point[1] == 'H':
                for neighbour in get_neighbours(point[0][0], point[0][1]):
                    index = path.index((neighbour, 'H')) if (neighbour, 'H') in path else -1
                    if index != -1 and index not in range(idx - 1, idx + 2):
                        energy -= 1

        return energy / 2  # divide by 2 to avoid double counting

    # add energies to paths
    # paths = [(get_energy(path), path) for path in paths]
    # print("Paths with energies ====> ", paths)

    # isolate all paths with minimum energy
    # min_energy = min([path[0] for path in paths])
    # print("Minimum energy is ====> ", min_energy)
    # min_energy_paths = [path for path in paths if path[0] == min_energy]
    return paths

for i in range(5, 20):
    print("N = ", i)
    native_fold(i)

