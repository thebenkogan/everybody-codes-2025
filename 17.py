from collections import defaultdict
import heapq
from math import ceil, sqrt
from ec import DIRS, read_input


def get_total_by_radius(part):
    lines = read_input(part)
    grid = [[c for c in line] for line in lines]

    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "@":
                cx, cy = x, y

    radius_to_total = defaultdict(int)
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "@":
                continue

            r = ceil(sqrt((x - cx) ** 2 + (y - cy) ** 2))
            radius_to_total[r] += int(c)

    return radius_to_total


totals = get_total_by_radius(1)
print(sum(v for (r, v) in totals.items() if r <= 10))

totals = get_total_by_radius(2)
r, best_total = max(totals.items(), key=lambda p: p[1])
print(r * best_total)

lines = read_input(3)
grid = [[c for c in line] for line in lines]


def get_best_by_steps(grid, steps):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "@":
                cx, cy = x, y
            if c == "S":
                sx, sy = x, y

    # first dijkstra: from S to right below volcano burn edge (only use left side)
    q = [(0, sx, sy)]
    seen = set()
    total = 0
    while len(q) > 0:
        c, x, y = heapq.heappop(q)

        if (x, y) in seen:
            continue
        seen.add((x, y))

        if x == cx and y > cy and y - 1 - cy <= steps:
            total += c
            bx, by = x, y
            break

        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            r = ceil(sqrt((nx - cx) ** 2 + (ny - cy) ** 2))
            if (
                0 <= nx < len(grid[0])
                and 0 <= ny < len(grid)
                and nx <= (cx + 2)
                and (nx, ny) not in seen
                and r > steps
            ):
                heapq.heappush(q, (c + int(grid[ny][nx]), nx, ny))

    # second dijkstra: from right below volcano to S (only use right side)
    seen = set()
    q = [(0, bx, by)]
    while len(q) > 0:
        c, x, y = heapq.heappop(q)

        if (x, y) in seen:
            continue
        seen.add((x, y))

        if x == sx and y == sy:
            total += c
            return total

        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            r = ceil(sqrt((nx - cx) ** 2 + (ny - cy) ** 2))
            if (
                0 <= nx < len(grid[0])
                and 0 <= ny < len(grid)
                and nx >= (cx - 2)
                and (nx, ny) not in seen
                and r > steps
            ):
                new_cost = c + int(grid[ny][nx]) if grid[ny][nx] != "S" else c
                heapq.heappush(q, (new_cost, nx, ny))


for steps in range(1, len(grid)):
    best = get_best_by_steps(grid, steps)
    if best < (steps + 1) * 30:
        print(steps * best)
        break
