from collections import defaultdict, deque
from math import ceil
from ec import nums, read_input


def min_flaps(part):
    lines = read_input(part)
    wall_xs = set()
    gaps = set()
    final_x = 0
    for line in lines:
        x, h, gap = nums(line)
        wall_xs.add(x)
        final_x = max(x, final_x)
        for y in range(h, h + gap):
            gaps.add((x, y))

    q = deque([(0, 0, 0)])
    seen = {(0, 0)}
    while len(q) > 0:
        c, x, y = q.popleft()
        if x == final_x:
            return c

        for dy in [-1, 1]:
            nx, ny = x + 1, y + dy
            if ny < 0 or (nx, ny) in seen or (nx in wall_xs and (nx, ny) not in gaps):
                continue
            q.append((c + max(dy, 0), nx, ny))
            seen.add((nx, ny))


print(min_flaps(1))
print(min_flaps(2))

gaps = defaultdict(list)
lines = read_input(3)
for line in lines:
    x, h, gap = nums(line)
    new_gap = [h, gap + h - 1]
    gaps[x].append(new_gap)

print(max(ceil((gaps[x][0][0] + x) / 2) for x in gaps))
