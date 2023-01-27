class Sequence():
	"""
	Class that implements the sequence datastructure (add more info!)
	"""

	default_hp = {
		'0': 'H',
		'1': 'P'
	}

	def __init__(self, sequence: list, transfer_dict: dict=default_hp) -> None:
		self.list_seq = [str(x) for x in sequence] 
		# list of str(int), each corresponding to a A.A.
		self.transfer_dict = transfer_dict

	def __str__(self) -> str:
		return self.get_fold_format()

	def set_amino(self, index: int, code: str) -> list:
		self.list_seq[index] = code # Code is str(int) so '1' for example
		return self.list_seq

	def get_fold_format(self) -> str:
		print(self.list_seq)
		temp_seq = ''.join(self.list_seq)
		print(temp_seq)
		for key in self.transfer_dict.keys():
			temp_seq = temp_seq.replace(key, self.transfer_dict[key])
		return ''.join(temp_seq)

