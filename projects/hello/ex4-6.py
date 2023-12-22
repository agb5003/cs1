def set_to_zero_vector(vec, n_elements):
    # Change value by passing pointer instead of the value
    vec[:] = [0] * n_elements

x = []
set_to_zero_vector(x, 3)
assert x == [0, 0, 0]

y = [10, 20]
set_to_zero_vector(y, 5)
assert y == [0, 0, 0, 0, 0]