def set_to_zero_vector(vec, n_elements):
    for i in range(len(vec)):
        vec[i] = 0
    print(vec)

# Example usage
x = [1, 2, 3]
set_to_zero_vector(x, 3)
print(x)  # Output: [0, 0, 0]
