""""
Generates every possible combination of H and Ps within a matrix of size 2n where n is the size of the input sequence.
"""

# Take a list of H and Ps as input
input_sequence = list(input("Enter the input sequence: "))
print(input_sequence)
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

visited = set()

# generate every possible path of length n going through coordinates x,y
paths  = []

def generate_paths(x, y, visited, path):
    if len(path) < len(input_sequence):
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


# plot all points in path
import matplotlib.pyplot as plt


for path in paths[:10]:
    x = [p[0] for p in path]
    y = [p[1] for p in path]
    plt.scatter(x, y)
    plt.plot(x, y)
    plt.show()
    print(path)






