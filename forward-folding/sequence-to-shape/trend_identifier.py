import matplotlib.pyplot as plt
import numpy as np

n = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10])
stable_paths = np.array([1, 2, 1, 2, 1, 1, 1, 1, 1])
opt_sequences = np.array([4, 8, 4, 12, 7, 10, 7, 6, 6])

plt.subplot(211)
plt.plot(n, stable_paths)
plt.title('The lowest no. of stable configurations for each sequence length')
plt.xlabel('Sequence length')
plt.ylabel('Lowest no. of stable configurations')
plt.grid()

plt.subplot(212)
plt.plot(n, opt_sequences)
plt.title('No. of seq with lowest no. of stable configurations for each sequence length')
plt.xlabel('Sequence length')
plt.ylabel('No. of seq with lowest no. of stable configurations')
plt.grid()

plt.suptitle('Trends in the folding of HP-model proteins')
plt.show()
