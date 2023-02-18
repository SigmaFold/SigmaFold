from db.supabase_setup import SupabaseDB
import json
import pandas as pd 
import tabulate
import numpy as np
import matplotlib.pyplot as plt


def sequence_to_integer(sequence):
    """Converts a sequence string to a 32 bit unsigned integer"""
    binary = sequence.replace("H", "1").replace("P", "0")
    if len(binary) > 32:
        raise ValueError("Sequence too long")
    if len(binary) < 32:
        binary = binary.zfill(32)
    return int(binary, 2)


    
def get_data_from_json(n):
    """ Gets data from the database and returns lists of dicts"""
    # read the sequence json 
    with open(f"data/seq_{n}.json", "r") as f:
        seq_list = json.load(f)
        print("Parsed seq_list")
    # read the shape json
    # Interpret H as 1 and V as 0
    # for each sequence string in the list, interpret as a 32 bit unsigned integer
    # H is 1 P is 0 
    # place in new column in the dict
    
        

    # convert the list of dicts to a pandas dataframe
    seq_df = pd.DataFrame(seq_list)

    # Create a new column in the dataframe with the sequence as an integer
    seq_df["sequence_int"] = seq_df["sequence"].apply(sequence_to_integer)



    # sort df by lowest degeneracy and then by lowest sequence
    seq_df = seq_df.sort_values(by=["degeneracy", "sequence_int"])


    # get rid of all rows where degeneracy is more than 4
    seq_df = seq_df[seq_df["degeneracy"] <= 2]

    # print the dataframe
    # print(tabulate.tabulate(seq_df, headers='keys', tablefmt='psql'))

    # calculate the difference between two sequence entries in the dataframe
    # this is the number of bits that are different
    seq_df["diff"] = seq_df["sequence_int"].diff()
    # print the dataframe

    # print a histogram of the differences
    #plt.hist(seq_df["diff"], bins=100)
    #plt.show()

    # get all the sequence
    seqs = seq_df["sequence"].to_list()

    # check for presence of H or P at each index and count, plot on histogram
    h_count_list = []
    for i in range(len(seqs[0])):
        h_count = 0
        p_count = 0
        for seq in seqs:
            if seq[i] == "H":
                h_count += 1
            
        h_count_list.append(h_count)
        print(f"Index {i}: H: {h_count}")

    
    # plot H_count list on a histogram with x axis as their indices in the H_count list
    # remove non integer bins from the x axis
    x_axis = np.arange(len(h_count_list))
    # plt.bar(x_axis, h_count_list)
    # plt.xticks(x_axis)

    # put the total number of sequences on the plot as a dotted line
    # plt.axhline(y=len(seqs), color='r', linestyle='--')
    # plt.show()

    # add an extra column. Compute the center of mass of the sequence
    # this is the average of the indices of the H's
    # this is the center of mass of the sequence
    def center_of_mass(sequence):
        # find mean of indices of H's
        mean_H_indices = sum([i for i, letter in enumerate(sequence) if letter == "H"])/sequence.count("H")
        # calculate the distance of each H from the center of mass
        # sum the distances
        # divide by the number of H's
        # this is the standard deviation
        std = sum([abs(i - mean_H_indices) for i, letter in enumerate(sequence) if letter == "H"])/sequence.count("H")
        return std

    seq_df["center_of_mass"] = seq_df["sequence"].apply(lambda x: center_of_mass(x))
    print(tabulate.tabulate(seq_df, headers='keys', tablefmt='psql'))

    # draw out the pdf of the center of mass
    plt.hist(seq_df["center_of_mass"], bins=100, density=True)
    # set title
    plt.title(f"Center of Mass for n={n} Sequences")

    plt.show()

    # try to fit a gaussian to the center of mass
    from scipy.optimize import curve_fit
    from scipy.stats import norm

    # the histogram of the data
    n, bins, patches = plt.hist(seq_df["center_of_mass"], bins=100, density=True, alpha=0.75)

    # add a 'best fit' line
    (mu, sigma) = norm.fit(seq_df["center_of_mass"])
    y = norm.pdf(bins, mu, sigma)
    l = plt.plot(bins, y, 'r--', linewidth=2)

    # plot
    plt.xlabel('Center of Mass')
    plt.ylabel('Probability')
    plt.title(f"Center of Mass for n=12 Sequences")
    plt.show()

    # print goodness of fit
    print(f"mu: {mu}, sigma: {sigma}")

    # do a normality test
    from scipy import stats
    
    # test whether the data is normally distributed print the p value and a boolean 
    # for whether the null hypothesis is rejected
    print(stats.normaltest(seq_df["center_of_mass"]))
    # print the skewness and kurtosis
    print(stats.skew(seq_df["center_of_mass"]))
    print(stats.kurtosis(seq_df["center_of_mass"]))
    # print the mean and standard deviation
    print(np.mean(seq_df["center_of_mass"]))
    print(np.std(seq_df["center_of_mass"]))

    







    


  







    

    
    
    
if __name__ == '__main__':
    n = 14
    print("Getting data for length: ", n)
    get_data_from_json(n)



