import re
import primitive_fold as pf
import numpy as np 
import scipy as sc

def get_reward(sequence, target, log=0):
	"""Function that gets a sequence as a string and ouputs the corresponding score
	Log: 0 to hide everthing, 1 to show everything, 2 to only show final result
	"""

	# Fold the input sequence
	_, opt_path = pf.primitive_fold(sequence)
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

	print(sc.signal.convolve(template, target))


	return reward

def find_max_correlation(m1, m2):
	corr_list = []
	n, m = np.shape(m1)
	for i in range(n+1):
		for j in range(m+1):
			sliced_m1 = m1[n-i:,:j]
			sliced_m2 = m2[:i, m-j:]
			print(sliced_m1)
			print(sliced_m2)
			print()
			corr = np.sum(np.multiply(sliced_m1, sliced_m2))
			# print(corr)
			corr_list.append(corr)
	return max(corr_list)

if __name__ == "__main__":

	target = np.matrix("0 0 0 0 0; 0 0 0 0 0; 0 1 0 1 0; 0 1 1 1 0; 0 1 1 0 0")

	sequence = "HPPHPPHH" 
	get_reward(sequence, target, 1)

	sequence = "HHHHHHHH" 	
	get_reward(sequence, target, 1)

