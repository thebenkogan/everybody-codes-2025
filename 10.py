from collections import defaultdict, deque
from functools import cache
from ec import read_input

DIRS = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

lines = read_input(1)
grid = [[c for c in line] for line in lines]
for y, row in enumerate(grid):
    for x, c in enumerate(row):
        if c == "D":
            sx, sy = x, y

q = deque([(0, sx, sy)])
seen = {(sx, sy)}
total = 0
while len(q) > 0:
    hops, x, y = q.popleft()

    if grid[y][x] == "S":
        total += 1

    if hops == 4:
        continue

    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if (nx, ny) not in seen and 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            seen.add((nx, ny))
            q.append((hops + 1, nx, ny))


print(total)

lines = read_input(2)
ROUNDS = 20
grid = [[c for c in line] for line in lines]
hideouts = set()
# precomputed locations of all sheeps for each round
# each sheeps location maps to it's original location so we don't eat it again later
round_to_sheeps = defaultdict(lambda: {})
for y, row in enumerate(grid):
    for x, c in enumerate(row):
        if c == "D":
            sx, sy = x, y
        if c == "#":
            hideouts.add((x, y))
        if c == "S":
            for r in range(ROUNDS + 1):
                ny = y + r
                if ny < len(grid):
                    round_to_sheeps[r][(x, ny)] = (x, y)

q = deque([(0, sx, sy)])
seen = set()
dead_sheep = set()
while len(q) > 0:
    hops, x, y = q.popleft()

    if hops > 0 and (x, y) not in hideouts:
        sheeps_prev = round_to_sheeps[hops - 1]
        sheeps_curr = round_to_sheeps[hops]
        if (x, y) in sheeps_prev and sheeps_prev[(x, y)] not in dead_sheep:
            dead_sheep.add(sheeps_prev[(x, y)])
        if (x, y) in sheeps_curr and sheeps_curr[(x, y)] not in dead_sheep:
            dead_sheep.add(sheeps_curr[(x, y)])

    if hops == ROUNDS:
        continue

    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if (
            (nx, ny, hops + 1) not in seen
            and 0 <= nx < len(grid[0])
            and 0 <= ny < len(grid)
        ):
            seen.add((nx, ny, hops + 1))
            q.append((hops + 1, nx, ny))

print(len(dead_sheep))

lines = read_input(3)
grid = [[c for c in line] for line in lines]
start_sheep = []
hideouts = set()
for y, row in enumerate(grid):
    for x, c in enumerate(row):
        if c == "D":
            sx, sy = x, y
        if c == "#":
            hideouts.add((x, y))
        if c == "S":
            start_sheep.append((x, y))
start_sheep = sorted(start_sheep)

# state is represented as the dragon's position + all sorted sheep's positions
# if sheep has already eaten, the associated state position is None


@cache
def traverse(state):
    x, y = state[0]
    sheep = list(state[1:])
    if all(s is None for s in sheep):
        return 1

    total = 0
    moved = False
    for i, s in enumerate(sheep):
        if s is None:
            continue

        sx, sy = s
        nx, ny = sx, sy + 1
        if ny >= len(grid):
            # sheep can move off the grid, still considered as making a turn
            moved = True
            continue

        if (nx, ny) == (x, y) and (x, y) not in hideouts:
            continue

        for dx, dy in DIRS:
            ndx, ndy = x + dx, y + dy
            if 0 <= ndx < len(grid[0]) and 0 <= ndy < len(grid):
                new_sheep = sheep.copy()
                new_sheep[i] = (nx, ny)
                if (ndx, ndy) not in hideouts and (ndx, ndy) in new_sheep:
                    new_sheep[new_sheep.index((ndx, ndy))] = None
                new_state = tuple([(ndx, ndy)] + new_sheep)
                total += traverse(new_state)
                moved = True

    # if no sheep could move, just try to move the dragon
    if not moved:
        for dx, dy in DIRS:
            ndx, ndy = x + dx, y + dy
            if 0 <= ndx < len(grid[0]) and 0 <= ndy < len(grid):
                new_sheep = sheep.copy()
                if (ndx, ndy) not in hideouts and (ndx, ndy) in new_sheep:
                    new_sheep[new_sheep.index((ndx, ndy))] = None
                new_state = tuple([(ndx, ndy)] + new_sheep)
                total += traverse(new_state)

    return total


initial_state = tuple([(sx, sy)] + start_sheep)
print(traverse(initial_state))
