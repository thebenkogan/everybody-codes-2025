from collections import deque
from heapq import heappop, heappush

from ec import read_input


def shortest_path_slow(part):
    lines = read_input(part, split_lines=False)
    moves = lines.split(",")
    x, y = 0, 0
    dx, dy = 0, 1
    walls = set()
    for move in moves:
        n = int(move[1:])
        t = move[0]
        if t == "R":
            dx, dy = dy, -dx
        elif t == "L":
            dx, dy = -dy, dx

        for _ in range(n):
            x += dx
            y += dy
            walls.add((x, y))

    walls.discard((x, y))
    ex, ey = x, y

    q = deque([(0, 0, 0)])
    seen = {(0, 0)}
    while q:
        d, x, y = q.popleft()
        if (x, y) == (ex, ey):
            return d

        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in walls or (nx, ny) in seen:
                continue
            seen.add((nx, ny))
            q.append((d + 1, nx, ny))


print(shortest_path_slow(1))
print(shortest_path_slow(2))


class CoordinateCompression:
    def __init__(self, original_values):
        self.compressed = sorted(set(original_values))
        self.orig_to_compressed = {x: i for i, x in enumerate(self.compressed)}
        self.n = len(self.compressed)

    def compressed_value(self, original_value):
        return self.orig_to_compressed[original_value]

    def original_value(self, compressed_value):
        return self.compressed[compressed_value]

    def n_compressed_values(self):
        return self.n


def build_wall_segments(instr):
    x, y, dx, dy = 0, 0, 0, 1
    wall_segments = []
    for d, amount in instr:
        dx, dy = (-dy, dx) if d == "L" else (dy, -dx)
        xn, yn = x + amount * dx, y + amount * dy
        wall_segments.append((x, y, xn, yn))
        x, y = xn, yn
    return (0, 0), (x, y), wall_segments


# create points of interest at and around wall segment ends
def init_compression(wall_segments):
    xs, ys = set(), set()
    for x1, y1, x2, y2 in wall_segments:
        xs.update([x1 - 1, x1, x1 + 1, x2 - 1, x2, x2 + 1])
        ys.update([y1 - 1, y1, y1 + 1, y2 - 1, y2, y2 + 1])
    return CoordinateCompression(xs), CoordinateCompression(ys)


def compress_coord(x, y, compression):
    x_compression, y_compression = compression
    return x_compression.compressed_value(x), y_compression.compressed_value(y)


def uncompress_coord(x, y, compression):
    x_compression, y_compression = compression
    return x_compression.original_value(x), y_compression.original_value(y)


def compress(start, end, wall_segments, compression):
    start = compress_coord(*start, compression)
    end = compress_coord(*end, compression)
    wall = set()
    for x1, y1, x2, y2 in wall_segments:
        from_x, from_y = compress_coord(x1, y1, compression)
        to_x, to_y = compress_coord(x2, y2, compression)
        # add wall positions in the compressed space between POIs
        if from_x == to_x:
            for y in range(min(from_y, to_y), max(from_y, to_y) + 1):
                wall.add((from_x, y))
        else:
            for x in range(min(from_x, to_x), max(from_x, to_x) + 1):
                wall.add((x, from_y))
    return start, end, wall


def dijkstra(start, end, wall, compression):
    x_min, x_max = 0, compression[0].n_compressed_values() - 1
    y_min, y_max = 0, compression[1].n_compressed_values() - 1
    pq = [(0, start)]
    seen = set()
    while len(pq) > 0:
        d, (x, y) = heappop(pq)

        if (x, y) in seen:
            continue
        seen.add((x, y))

        if (x, y) == end:
            return d

        ux, uy = uncompress_coord(x, y, compression)
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            xn, yn = x + dx, y + dy
            if xn < x_min or xn > x_max or yn < y_min or yn > y_max:
                continue
            # turns out all adjacent positions are in the compressed space so we don't need to check
            uxn, uyn = uncompress_coord(xn, yn, compression)
            dist = abs(ux - uxn) + abs(uy - uyn)
            if ((xn, yn) == end or (xn, yn) not in wall) and (xn, yn) not in seen:
                heappush(pq, (d + dist, (xn, yn)))


lines = read_input(3, split_lines=False)
instr = [(x[0], int(x[1:])) for x in lines.split(",")]
start, end, wall_segments = build_wall_segments(instr)
compression = init_compression(wall_segments)
start, end, wall = compress(start, end, wall_segments, compression)
ans3 = dijkstra(start, end, wall, compression)
print(ans3)
