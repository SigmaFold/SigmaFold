import path_generator
import permutation_generator


def create_graph_db(length, base):
    """Creates a dictionary that relates each sequence with its native fold in graph form"""
    # Initialize the dictionary
    seq_dict = {}
    # Create a list of all the possible sequence for given length and base
    perm_list = permutation_generator.perm_gen(length, base)
    # Creating the dictionary
    for seq in perm_list:
        num_degen, paths = path_generator.handle_sequence(seq)  # Finding all the paths for a sequence
        filtered_paths = path_generator.remove_duplicates(paths)    # Filtering the duplicate paths
        seq_graph = []  # List to store the graphed paths for each sequence
        # Creates graphed path for each native path and stores it in seq_graph
        for path in filtered_paths:
            graph = path_generator.find_graph(seq, path)
            if graph not in seq_graph:  # Does not add paths that create the same shape
                seq_graph.append(graph)
        # For each sequence key, the value is the list of graphs
        seq_dict[seq] = seq_graph
    return seq_dict


if __name__ == '__main__':
    graph_dict = create_graph_db(3,2)
    print(graph_dict)