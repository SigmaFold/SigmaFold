import numpy as np


def remove_duplicates(path_list):
    """Removes rotations and reflections from a list of paths"""
    filtered_paths = path_list.copy()

    # we will be performing path list dot product with rotation_matrix/reflection matrix.
    # Hence, the rotation matrices have already been transposed
    rotation_90_anticlockwise = np.array([[0, 1], [-1, 0]])
    rotation_180_anticlockwise = np.array([[-1, 0], [0, -1]])
    rotation_270_anticlockwise = np.array([[0, -1], [1, 0]])

    # Remove reflections
    for i in range(len(path_list)):
        path_array = np.array(path_list[i])
        for other_path in path_list[i + 1:]:
            other_path_array = np.array(other_path)
            rot_90 = np.dot(other_path_array, rotation_90_anticlockwise)  # 90 degree anticlockwise rot of other_path
            rot_180 = np.dot(other_path_array, rotation_180_anticlockwise)  # 180 degree anticlockwise rot of other_path
            rot_270 = np.dot(other_path_array, rotation_270_anticlockwise)  # 270 degree anticlockwise rot of other_path
            if ((np.all(rot_90 == path_array)) or (np.all(rot_180 == path_array)) or (np.all(rot_270 == path_array))) and other_path in filtered_paths:
                filtered_paths.remove(other_path)

    return filtered_paths


rotation_270_anticlockwise1 = np.array([[0, -1], [1, 0]])
pt = (0, 1)
pt_list = [(0, 0), (0, 1), (0, 2), (0, 3)]
path_list1 = [[(0, 0), (0, 1), (1, 1), (1, 0)],
              [(0, 0), (0, 1), (-1, 1), (-1, 0)],
              [(0, 0), (1, 0), (1, 1), (0, 1)],
              [(0, 0), (1, 0), (1, -1), (0, -1)],
              [(0, 0), (0, -1), (1, -1), (1, 0)],
              [(0, 0), (0, -1), (-1, -1), (-1, 0)],
              [(0, 0), (-1, 0), (-1, 1), (0, 1)],
              [(0, 0), (-1, 0), (-1, -1), (0, -1)],
              [(0, 0), (-1, 0), (-1, -1), (0, -2)]]

print(remove_duplicates(path_list1))

# np_pt = np.array(path_list)
# print(np_pt)
#
# rotated_list = np.dot(path_list, rotation_270_anticlockwise)
# print('rotated list is')
# print(rotated_list)
