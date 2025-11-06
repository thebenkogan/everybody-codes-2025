from collections import Counter
from ec import nums, read_input

ns = nums(read_input(1, split_lines=False))
print(sum(set(ns)))

ns = nums(read_input(2, split_lines=False))
ns = sorted(set(ns))
print(sum(ns[:20]))

ns = nums(read_input(3, split_lines=False))
counts = Counter(ns)
print(max(counts.values()))
