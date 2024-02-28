# Example list of nested lists
nested_lists = [
    [1, 2, 3],
    [1, 2, 4],
    [7, 8, 9],
    [1, 2, 5],
    [10, 11, 12],
]

# Pattern to be removed
pattern_to_remove = [1, 2]
print('pattern_to_remove', pattern_to_remove)
print('len(pattern_to_remove)', len(pattern_to_remove))

# Filter out nested lists with the specified pattern
filtered_lists = [nested_list for nested_list in nested_lists if nested_list[:2] != pattern_to_remove]

print(filtered_lists)
