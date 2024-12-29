import numpy as np


def describe_array(my_array):
    print(f"Shape: {my_array.shape}")
    print(f"Size: {my_array.size}")
    print(f"Type: {my_array.dtype}")
    print(f"Data:\n{my_array}")


# A 1x3 1D array
my_array = np.array([1, 2, 3])
describe_array(my_array)

# A 2x3 2D array
my_array = np.array([[1, 2, 3], [4, 5, 6]])
describe_array(my_array)


# Initialise 1x4 to 0 as floats
my_array = np.zeros(4)
describe_array(my_array)

# Initialise 2x3 to 0 as int
my_array = np.zeros((2, 3), dtype=np.int32)
describe_array(my_array)

# Initialise 2x3 to 9
my_array = np.full((2, 3), fill_value=9, dtype=np.int16)
describe_array(my_array)

# Initialise 2x3 to 9
my_array = np.full((2, 3, 4), fill_value=False, dtype=np.bool)
describe_array(my_array)

# Initialise with a range
my_array = np.arange(25, 50, 5)
describe_array(my_array)

# Create a keypad
keypad = np.arange(1, 10).reshape(3, 3)
print(keypad)

# Create linearly spaced values
my_array = np.linspace(50, 100, 5)
describe_array(my_array)

# random array
my_array = np.random.rand(2, 4)
describe_array(my_array)

# Create an array based on another array
my_array = np.asarray([[2, 3, 4], [5, 6, 7]])
print(my_array)
new_array = np.zeros_like(my_array)
print(new_array)


np.array([[2, 3, 4], [5, 6, 7]])  # Makes a copy of the input
np.asarray(
    [[2, 3, 4], [5, 6, 7]]
)  # Does not make a copy of the input (original reflects changes)

import numpy as np

original_array = np.array(list(range(5)))

print("Creating with np.array()...")
with_array = np.array(original_array)
print(with_array)

print("Creating with np.asarray()...")
with_as_array = np.asarray(original_array)
print(with_as_array)

print("Updating the original array...")
original_array[2] = 0
print(f"original_array: {original_array}")
print(f"with_array: {with_array}")
print(f"with_as_array: {with_as_array}")


# Read a text file
# doesn't work
data = np.loadtxt("grid.txt", dtype="U1", comments=None, delimiter=1)


# Obtaining the corners
my_array = np.asarray([["tl", "tm", "tr"], ["ml", "mm", "mr"], ["bl", "bm", "br"]])
print(my_array)
row_index = np.array([[0, 0], [-1, -1]])  # top,  top,   bottom, bottom
col_index = np.array([[0, -1], [0, -1]])  # left, right, left,   right
print(
    f"Obtaining the corners with:\n{np.array([row_index, col_index])}...\n"
    + f"{my_array[row_index, col_index]}"
)


# Rolling
my_array = np.asarray(([5, 10, 15, 20, 5], [20, 25, 30, 30, 30]))

print(f"Starting array:\n{my_array}")

# If we roll without specifying an axis, then the array is flattened before shifting.
# The resulting array has the same shape as the original
print("\nRolling the whole array...")
rolled = np.roll(my_array, 1)
print(f"Rolled:\n{rolled}")

print("\nRolling by row...")
for row in my_array:
    print(f"Rolled row: {np.roll(row, 1)}")

# More efficient to roll by axis
rolled = np.roll(my_array, 1, axis=1)
print(f"\nRolling the whole array by row axis:\n{rolled}")

# Obviously, we can do it by column too
rolled = np.roll(my_array, 1, axis=0)
print(f"\nRolling the whole array by col axis:\n{rolled}")


# How many times is value n greater than value n-1
my_array = np.asarray([1, 5, 20, 15, 11, 16])
print(my_array)
increases = my_array[1:] > my_array[:-1]
print(f"n > n-1? {increases}")
print(f"Count of (n > n-1): {increases.sum()}")

# Turning a List of Str into a 2D NumPy Char Array
data = """abcd
1234
efgh"""

my_array = np.array([list(line) for line in data.splitlines()])
print(my_array)

# Carving Up a 2D Array into Smaller Regions
# Start with data where rows are of different lengths
data = """        1111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666"""

data = data.splitlines()
max_width = max(len(line) for line in data)

# Make all rows the same length
data = [
    line + " " * (max_width - len(line)) if len(line) < max_width else line
    for line in data
]

my_array = np.array([list(line) for line in data])
print(my_array)

face_coords = [(2, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 2)]  # Faces 0-5
num_horiz_faces = max(x for x, y in face_coords) + 1
face_width = max_width // num_horiz_faces

faces = [
    my_array[
        y * face_width : (y + 1) * face_width, x * face_width : (x + 1) * face_width
    ]
    for x, y in face_coords
]

for face in faces:
    print(face)

# Creating 2D Arrays, and Selecting / Updating Values

import re

DATA = """toggle 1,6 through 2,6
turn off 1,7 through 2,9
turn off 6,1 through 6,3
turn off 8,2 through 11,6
turn on 19,2 through 21,3
turn on 17,4 through 26,8
turn on 10,10 through 19,15
turn off 4,14 through 6,16
toggle 5,15 through 15,25
toggle 20,1 through 29,10"""

INSTR_PATTERN = re.compile(r"(\d+),(\d+) through (\d+),(\d+)")
np.full


data = DATA.splitlines()
data
line = data[0]
match = INSTR_PATTERN.search(line)
assert not match, "error message"
x, y, z, t = map(int, match.groups())
x, y, z, t

np.logical_not
