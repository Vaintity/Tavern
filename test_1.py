my_list = [1, 2, 3, 4, 5]

element_to_remove = 8

try:
    my_list.remove(element_to_remove)
    print(f"Element {element_to_remove} removed from the list")
    print("Updated list:", my_list)
except ValueError:
    print(f"Element {element_to_remove} not found in the list")
