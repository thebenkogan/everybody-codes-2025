from ec import read_input

ns = [int(n) for n in read_input(1)]
dial = [1] * (len(ns) + 1)

l, r = 1, len(ns)
for i, n in enumerate(ns):
    if i % 2 == 0:
        dial[l] = n
        l += 1
    else:
        dial[r] = n
        r -= 1

print(dial[2025 % len(dial)])


def calc_dial_with_ranges(lines, index):
    ranges = []
    for line in lines:
        a, b = map(int, line.split("-"))
        ranges.append(range(a, b + 1))

    dial = [1] * (len(ranges) + 1)
    dial[0] = range(1, 2)
    l, r = 1, len(dial) - 1
    for i, rng in enumerate(ranges):
        if i % 2 == 0:
            dial[l] = rng
            l += 1
        else:
            dial[r] = range(rng.stop - 1, rng.start - 1, -1)
            r -= 1

    size = sum(len(r) for r in dial)
    find = index % size
    for rng in dial:
        if len(rng) <= find:
            find -= len(rng)
            continue

        return rng.start + (find * rng.step)


print(calc_dial_with_ranges(read_input(2), 20252025))
print(calc_dial_with_ranges(read_input(3), 202520252025))
