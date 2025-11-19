from collections import deque
from ec import DIRS, read_input


def bfs(grid, start, destroyed=set()):
    q = deque(start)
    seen = set(start)
    while len(q) > 0:
        x, y = q.popleft()
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if (
                (nx, ny) not in seen
                and 0 <= nx < len(grid[0])
                and 0 <= ny < len(grid)
                and grid[ny][nx] <= grid[y][x]
                and (nx, ny) not in destroyed
            ):
                q.append((nx, ny))
                seen.add((nx, ny))

    return seen


lines = read_input(1)
grid = [[int(c) for c in line] for line in lines]
print(len(bfs(grid, [(0, 0)])))

lines = read_input(2)
grid = [[int(c) for c in line] for line in lines]
print(len(bfs(grid, [(0, 0), (len(grid[0]) - 1, len(grid) - 1)])))

lines = read_input(3)
grid = [[int(c) for c in line] for line in lines]
destroyed = set()
starts = []
for _ in range(3):
    best = set()
    best_coord = None
    for y, row in enumerate(grid):
        for x in range(len(row)):
            if (x, y) in destroyed:
                continue

            reached = bfs(grid, [(x, y)], destroyed)
            if len(reached) > len(best):
                best = reached
                best_coord = (x, y)

    destroyed.update(best)
    starts.append(best_coord)

print(len(bfs(grid, starts)))
