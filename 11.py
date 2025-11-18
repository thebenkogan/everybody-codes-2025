from ec import read_input


lines = read_input(1)
ns = [int(n) for n in lines]


def balance(ns, limit=None):
    first_phase = True
    rounds = 0
    for _ in range(limit if limit is not None else int(1e10)):
        moved = False
        for i in range(len(ns) - 1):
            if first_phase and ns[i] > ns[i + 1]:
                moved = True
                ns[i] -= 1
                ns[i + 1] += 1
            elif not first_phase and ns[i] < ns[i + 1]:
                moved = True
                ns[i] += 1
                ns[i + 1] -= 1

        if not moved:
            if not first_phase:
                return rounds
            first_phase = False
        rounds += 1

    return rounds


balance(ns, 11)
print(sum((i + 1) * n for i, n in enumerate(ns)))

lines = read_input(2)
ns = [int(n) for n in lines]
print(balance(ns) - 1)

# turns out we can just take the sum of differences below the mean, idk why

lines = read_input(3)
ns = [int(n) for n in lines]
mean = sum(ns) // len(ns)
print(sum(mean - n for n in ns if n < mean))
