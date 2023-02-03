import numpy as np
import random as rnd
import scipy as sc

def generate_shape(seq_len=int(10)):

    # maximum dimension
    half_len = int(round(seq_len/2))

    # compute triangle constraint
    bounds = np.tril(np.ones([half_len, half_len], dtype=int), 0) # boundary for reference
    shape = np.zeros([half_len, half_len], dtype=int) # shape for output
    bounds = np.pad(bounds, 1) # padding to account for void
    shape = np.pad(shape, 1)
    
    # possible moves
    dirs = ((0,1), (0, -1), (1, 0), (-1, 0))

    # initialising
    shape[-2, 1] = 1 # bottom left of triangle
    shape[-2, 2] = 1 # first move is definitely right
    i, j = half_len, 2 # i = row, j = col
    path_len = np.count_nonzero(shape)# initial path length
    monke_stupid_index = 0 # how stupid monke is

    while (path_len) < seq_len:
        cur_dir = rnd.choice(dirs) # chooses a random move (monke thinks)
        i, j = i + cur_dir[0], j + cur_dir[1] # update coordinates (monke's proposed move)

        # check if move viable (monke checks)
        dirs2 = [(0,1), (0, -1), (1, 0), (-1, 0)] # temporary list for remaking decisions
        while (bounds[i, j] == 0) or (shape[i, j] == 1): # if steps into void or path already taken, monke stupid
            i, j = i-cur_dir[0], j-cur_dir[1] # monke forgets
            dirs2.remove(cur_dir) # monke learns

            if len(dirs2) == 0: # moves have run out
                monke_stupid_index += 1
                i,j = half_len, 2 # resetting coordinate to beginning
                shape = np.pad(np.zeros([half_len, half_len], dtype=int), 1) # resetting shape & path length
                shape[-2, 1] = 1
                shape[-2, 2] = 1
                path_len = np.count_nonzero(shape)
                break

            else: # still have available moves
                cur_dir = rnd.choice(dirs2)# pick another move
                i, j = i + cur_dir[0], j + cur_dir[1]

        # move viable
        shape[i, j] = 1 # monke moves
        path_len = np.count_nonzero(shape)

    # print(f"monke got stuck {monke_stupid_index} times")
    return shape

def primitive_fold(sequence):

    input_sequence = sequence
    print(input_sequence)

    origin = (0, 0)
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    visited = set()

    # generate every possible path of length n going through coordinates x,y
    paths = []
    n = len(input_sequence)


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

        return energy/2 # divide by 2 to avoid double counting


    # add energies to paths
    paths = [(get_energy(path), path) for path in paths]
    # print("Paths with energies ====> ", paths)

    # isolate all paths with minimum energy
    min_energy = min([path[0] for path in paths])
    # print("Minimum energy is ====> ", min_energy)
    min_energy_paths = [path for path in paths if path[0] == min_energy]

    return min_energy, min_energy_paths

def get_reward(sequence, target, log=0):
	"""Function that gets a sequence as a string and ouputs the corresponding score
	Log: 0 to hide everthing, 1 to show everything, 2 to only show final result
	"""

	# Fold the input sequence
	_, opt_path = primitive_fold(sequence)
	degeneracy = len(opt_path)
	prim_fold = opt_path[0][1]

	# print(prim_fold)	

	# Analyse target shape
	n, m = np.shape(target)

	# Convert fold to matrix for further analysis
	template = np.zeros((n,m))
	yoffset = round(n/2)-1
	xoffset = round(m/2)-1

	for base in prim_fold:
		full_coord = base[0]

		template[full_coord[0]+yoffset, full_coord[1]+xoffset] = 1

	template = template.astype(int)

	if log == 1:
		print("Template:")
		print(template)
		print()
		print("Target:")
		print(target)
		print(f'\nDegeneracy is {degeneracy}')

	# Clunky implementation of Kullback-Leiber divergence but why not
	divergence = 0
	A = np.sum(target)
	B = np.sum(template)
	for i in range(n):
		for j in range(m):
			divergence += target[i,j]*(np.log10((template[i,j]+10)/(target[i,j]+10)))

	# Reward: low degeneracy and low divergence are rewarded
	reward = 1/degeneracy*1/divergence

	if log == 1:
		print(f'Divergence from target shape: {divergence}\n')

	if log > 0:
		print(f'Final Reward: {reward}\n')

	a = sc.signal.convolve(template, target)
	print(a)
	print(np.mean(a))

    
	return reward, deviation, degen

if __name__ == '__main__':
    print(generate_shape())