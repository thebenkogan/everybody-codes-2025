from math import ceil
from ec import nums, read_input

ns = nums(read_input(1, split_lines=False))
factor = ns[0] / ns[-1]

print(int(factor * 2025))

ns = nums(read_input(2, split_lines=False))
factor = ns[0] / ns[-1]
print(ceil(10000000000000 / factor))

ns = nums(read_input(3, split_lines=False))
factor = 1
for i in range(0, len(ns), 2):
    prev, curr = ns[i], ns[i + 1]
    factor *= prev / curr

print(int(factor * 100))
