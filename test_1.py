# Using a dictionary to store variables with counters
variable_dict = {}

# Adding variables with counters
for i in range(1, 6):
    variable_name = f"variable_{i}"
    variable_dict[variable_name] = i * 10

# Accessing the variables
for name, value in variable_dict.items():
    print(f"{name}: {value}")
