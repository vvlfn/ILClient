# Creating two dictionaries
sample_dict = {'a': 1, 'b': 2, 'c': 3}
empty_dict = {}

# Converting keys to sets
sample_keys_set = set(sample_dict.keys())
empty_keys_set = set(empty_dict.keys())

# Checking if dictionaries are empty
is_sample_dict_empty = not sample_dict
is_empty_dict_empty = not empty_dict

# Printing results
print(f"Sample dictionary keys set: {sample_keys_set}")
print(f"Empty dictionary keys set: {empty_keys_set}")
print(f"Is sample dictionary empty? {is_sample_dict_empty}")
print(f"Is empty dictionary empty? {is_empty_dict_empty}")
