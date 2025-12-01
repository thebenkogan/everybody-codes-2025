from collections import deque
from ec import DIRS, read_input


def parse(part):
    lines = read_input(part)
    grid = [[c for c in line] for line in lines]
    tri = [[None] * len(grid[0]) for _ in range(len(grid))]
    start, end = None, None
    for y, row in enumerate(grid):
        down = True
        for x, c in enumerate(row):
            if c == ".":
                continue
            if c == "S":
                start = (x, y)
            if c == "E":
                end = (x, y)
            if c != "#":
                tri[y][x] = down
            down = not down

    return tri, start, end


def is_neighbor(tri, x, y, nx, ny):
    return (
        (nx != x and tri[ny][nx] is not None)
        or (ny > y and not tri[y][x] and tri[ny][nx])
        or (ny < y and tri[y][x] and not tri[ny][nx])
    )


tri, _, _ = parse(1)
pairs = set()
for y, row in enumerate(tri):
    for x, c in enumerate(row):
        if c is None:
            continue

        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if (
                nx < 0
                or nx >= len(tri[0])
                or ny < 0
                or ny >= len(tri)
                or tri[ny][nx] is None
            ):
                continue
            if is_neighbor(tri, x, y, nx, ny):
                pairs.add(tuple(sorted([(x, y), (nx, ny)])))

print(len(pairs))

tri, (sx, sy), end = parse(2)
q = deque([(0, sx, sy)])
seen = {(sx, sy)}
while len(q) > 0:
    c, x, y = q.popleft()
    if (x, y) == end:
        print(c)
        break

    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if (
            nx < 0
            or nx >= len(tri[0])
            or ny < 0
            or ny >= len(tri)
            or tri[ny][nx] is None
            or (nx, ny) in seen
        ):
            continue
        if is_neighbor(tri, x, y, nx, ny):
            seen.add((nx, ny))
            q.append((c + 1, nx, ny))


def rotate(tri):
    n_rows, n_cols = len(tri), len(tri[0])
    tri_new = [[None for _ in range(n_cols)] for _ in range(n_rows)]
    for c in range(0, n_cols, 2):
        rn = c // 2
        cn = n_cols - 1 - c // 2
        for r in range(n_rows):
            if r + c < n_cols and tri[r][r + c] is not None:
                tri_new[rn][cn] = tri[r][r + c]
                cn -= 1
            if r + c + 1 < n_cols and tri[r][r + c + 1] is not None:
                tri_new[rn][cn] = tri[r][r + c + 1]
                cn -= 1
    return tri_new


tri, (sx, sy), end = parse(3)
# rotated = []
# for _ in range(3):
#     rotated.append(tri)
#     tri = rotate(tri)

for row in tri:
    print(row)
exit()

q = deque([(0, sx, sy)])
seen = {(sx, sy)}
while len(q) > 0:
    c, x, y = q.popleft()
    if (x, y) == end:
        print(c)
        break

    curr_tri = rotated[c % len(rotated)]
    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if (
            nx < 0
            or nx >= len(curr_tri[0])
            or ny < 0
            or ny >= len(curr_tri)
            or curr_tri[ny][nx] is None
            or (nx, ny) in seen
        ):
            continue
        if is_neighbor(curr_tri, x, y, nx, ny):
            seen.add((nx, ny))
            q.append((c + 1, nx, ny))
