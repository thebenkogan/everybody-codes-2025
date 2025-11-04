from ec import read_input


def get_input(part):
    data = read_input(part, split_lines=False)
    names, moves = data.split("\n\n")
    names = names.split(",")
    moves = moves.split(",")
    return names, moves


def get_first(part):
    names, moves = get_input(part)
    i = 0
    for move in moves:
        m = move[0]
        n = int(move[1:])
        factor = 1 if m == "R" else -1
        if part == 1:
            i = max(0, min(len(names) - 1, i + (factor * n)))
        elif part == 2:
            i = (i + (factor * n)) % len(names)

    return names[i]


print(get_first(1))
print(get_first(2))

names, moves = get_input(3)
for move in moves:
    m = move[0]
    n = int(move[1:])
    factor = 1 if m == "R" else -1
    i = (factor * n) % len(names)
    names[0], names[i] = names[i], names[0]

print(names[0])
