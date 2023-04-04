"""
1. Gets all sequence data for a given n. Saves it locally for later use, in case the database is not available.
Save as pickle file.
2. Iterate through all elements. Every type a new shape_mapping is encountered, create the node and add it to the graph.
3. for every sequence, and an edge between all the shappe_mappings that it maps to.
4. Save the graph as a pickle file.
"""
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pickle
