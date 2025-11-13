from ec import nums, read_input


nails = nums(read_input(1, split_lines=False))
total = 0
for n1, n2 in zip(nails[:-1], nails[1:]):
    if abs(n1 - n2) == 16:
        total += 1

print(total)


def intersects(l1, l2):
    n1, n2 = tuple(sorted(l1))
    n3, n4 = l2
    good1 = n1 < n3 < n2 and (n4 < n1 or n4 > n2)
    good2 = n1 < n4 < n2 and (n3 < n1 or n3 > n2)
    return good1 or good2


nails = nums(read_input(2, split_lines=False))
lines = list(zip(nails[:-1], nails[1:]))
total = 0
for i in range(1, len(lines)):
    for j in range(i):
        l1, l2 = lines[i], lines[j]
        if intersects(l1, l2):
            total += 1

print(total)

nails = nums(read_input(3, split_lines=False))
lines = list(zip(nails[:-1], nails[1:]))
best = 0
for i in range(1, 257):
    for j in range(i + 1, 257):
        # adjust experimentally, the best cut is usually somewhere through the middle of the circle
        # e.g. when i and j are about 256/2 = 128 apart
        if abs(i - j) < 125 or abs(i - j) > 145:
            continue
        line = (i, j)
        total = sum(1 for l in lines if intersects(l, line))
        best = max(best, total)

print(best)
