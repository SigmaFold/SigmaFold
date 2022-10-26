input_sequence = "HPH"
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


generate_paths(origin[0], origin[1], visited, [])
print(paths)
print(len(paths))