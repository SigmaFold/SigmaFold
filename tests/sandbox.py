import numpy as np

def generate_fov_vector(depth):
    """Method that generates the vector with all the relevant vision 
    directions depending on the depth_field attribute"""
    size = (2*depth+1)**2
    dirs = np.zeros((size, 2))
    counter = 0
    for i in range(-depth, depth+1):
        for j in range(-depth, depth+1):
            dirs[counter] = [i, j]
            counter += 1
    print(dirs)
    return dir

if __name__ == '__main__':
    generate_fov_vector(2)