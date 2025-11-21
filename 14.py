from collections import defaultdict
from ec import read_input

DIRS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


def step(grid):
    new_grid = [["."] * len(grid[0]) for _ in range(len(grid))]
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            active_diag = 0
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < len(grid[0])
                    and 0 <= ny < len(grid)
                    and grid[ny][nx] == "#"
                ):
                    active_diag += 1

            if c == "#" and active_diag % 2 == 1:
                new_grid[y][x] = "#"
            if c == "." and active_diag % 2 == 0:
                new_grid[y][x] = "#"

    return new_grid


def count_active_in_grid(grid):
    total = 0
    for row in grid:
        for c in row:
            if c == "#":
                total += 1
    return total


def count_active(grid, rounds):
    total = 0
    for _ in range(rounds):
        grid = step(grid)
        total += count_active_in_grid(grid)
    return total


lines = read_input(1)
grid = [[c for c in line] for line in lines]
print(count_active(grid, 10))

lines = read_input(2)
grid = [[c for c in line] for line in lines]
print(count_active(grid, 2025))


def matches_pattern(grid, pattern):
    for y, row in enumerate(pattern):
        for x, c in enumerate(row):
            if grid[y + 13][x + 13] != c:
                return False
    return True


lines = read_input(3)
pattern = [[c for c in line] for line in lines]
grid = [["."] * 34 for _ in range(34)]

seen = set()
total_after_rounds = defaultdict(int)
for i in range(1000000000):
    grid = step(grid)
    total_after_rounds[i] = total_after_rounds[i - 1]
    if matches_pattern(grid, pattern):
        total_after_rounds[i] += count_active_in_grid(grid)
    key = "".join("".join(row) for row in grid)
    if key in seen:
        cycle_length = i
        break
    seen.add(key)

completed = 1000000000 // cycle_length
remaining = 1000000000 % cycle_length
print(total_after_rounds[cycle_length] * completed + total_after_rounds[remaining])
