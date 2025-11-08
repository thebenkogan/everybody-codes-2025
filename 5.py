from functools import cmp_to_key
import math
from ec import nums, read_input

ns = nums(read_input(1, split_lines=False))
ns = ns[1:]


def get_quality(ns):
    segments = [[None, ns[0], None]]
    for n in ns[1:]:
        found = False
        for segment in segments:
            if n < segment[1] and segment[0] == None:
                segment[0] = n
                found = True
                break
            elif n > segment[1] and segment[2] == None:
                segment[2] = n
                found = True
                break
        if not found:
            segments.append([None, n, None])

    return int("".join(str(s[1]) for s in segments)), segments


print(get_quality(ns)[0])

lines = read_input(2)
hi, lo = -math.inf, math.inf
for line in lines:
    ns = nums(line)
    identifier, ns = ns[0], ns[1:]
    quality, _ = get_quality(ns)
    hi = max(hi, quality)
    lo = min(lo, quality)

print(hi - lo)


lines = read_input(3)
results = []
for line in lines:
    ns = nums(line)
    identifier, ns = ns[0], ns[1:]
    quality, segments = get_quality(ns)
    results.append((quality, segments, identifier))


def level_to_number(l):
    return int("".join([str(n) for n in l if n is not None]))


def compare(r1, r2):
    q1, s1, i1 = r1
    q2, s2, i2 = r2

    if q1 != q2:
        return 1 if q1 > q2 else -1

    for l1, l2 in zip(s1, s2):
        n1, n2 = level_to_number(l1), level_to_number(l2)
        if n1 != n2:
            return 1 if n1 > n2 else -1

    return 1 if i1 > i2 else -1


results = sorted(results, key=cmp_to_key(compare), reverse=True)
print(sum([(i + 1) * n for i, (_, _, n) in enumerate(results)]))
