from ec import nums, read_input

ax, ay = nums(read_input(1, split_lines=False))
rx, ry = 0, 0


def mul(a, b, c, d):
    return (a * c - b * d, a * d + b * c)


def add(a, b, c, d):
    return (a + c, b + d)


def div(a, b, c, d):
    return (int(a / c), int(b / d))


for _ in range(3):
    rx, ry = mul(rx, ry, rx, ry)
    rx, ry = div(rx, ry, 10, 10)
    rx, ry = add(rx, ry, ax, ay)

print(f"[{rx},{ry}]")

ax, ay = nums(read_input(2, split_lines=False))


def should_engrave(px, py):
    rx, ry = 0, 0
    for _ in range(100):
        rx, ry = mul(rx, ry, rx, ry)
        rx, ry = div(rx, ry, 100000, 100000)
        rx, ry = add(rx, ry, px, py)
        if rx < -1000000 or rx > 1000000 or ry < -1000000 or ry > 1000000:
            return False
    return True


ex, ey = add(ax, ay, 1000, 1000)
total = 0
for i, y in enumerate(range(ay, ey + 1, 10)):
    for j, x in enumerate(range(ax, ex + 1, 10)):
        if should_engrave(x, y):
            total += 1

print(total)

ax, ay = nums(read_input(3, split_lines=False))
grid = [["."] * 1001 for _ in range(1001)]
total = 0
for i, y in enumerate(range(ay, ey + 1)):
    for j, x in enumerate(range(ax, ex + 1)):
        if should_engrave(x, y):
            total += 1
            grid[i][j] = "X"

for row in grid:
    print("".join(row))
print(total)
