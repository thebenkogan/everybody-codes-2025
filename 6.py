from collections import defaultdict, deque
from string import ascii_lowercase, ascii_uppercase
from ec import read_input


def count_pairs(line, include_set=None):
    counts = defaultdict(int)
    total = 0
    for c in line:
        if include_set is not None and c not in include_set:
            continue
        if c in ascii_lowercase:
            total += counts[c]
        else:
            counts[c.lower()] += 1

    return total


line = read_input(1, split_lines=False)
print(count_pairs(line, "aA"))

line = read_input(2, split_lines=False)
print(count_pairs(line))

DIST = 1000
LOOP = 1000
line = read_input(3, split_lines=False)

# part 3 algorithm:
# compute the counts of each novice position in 2 modes:
# loop: count it assuming the left and right extend forever in loops
# non-loop: respect the line boundaries
# then for the first and last 1000, we can use 1*non-loop + 999*loops
# for all else in the middle, just use the loop count * 1000


def get_counts(line, should_loop):
    window_counts = defaultdict(int)
    window = deque([])
    for c in line:
        if len(window) == DIST + 1:
            break
        window.append(c)
        if c in ascii_uppercase:
            window_counts[c.lower()] += 1

    if should_loop:
        for i in range(len(line) - 1, len(line) - DIST - 1, -1):
            c = line[i]
            window.appendleft(c)
            if c in ascii_uppercase:
                window_counts[c.lower()] += 1

    pos_counts = defaultdict(int)
    for i, c in enumerate(line):
        if c in ascii_lowercase:
            pos_counts[i] = window_counts[c]

        nxt_index = i + DIST + 1
        if should_loop:
            nxt_index = nxt_index % len(line)

        has_next = nxt_index < len(line)
        if has_next:
            nxt = line[nxt_index]
            window.append(nxt)
            if nxt in ascii_uppercase:
                window_counts[nxt.lower()] += 1

        if len(window) > 2 * DIST + 1 or not has_next:
            removed = window.popleft()
            if removed in ascii_uppercase:
                window_counts[removed.lower()] -= 1

    return pos_counts


non_loop = get_counts(line, False)
loop = get_counts(line, True)
total = 0
for i, c in enumerate(line):
    if i < DIST or len(line) - i - 1 < DIST:
        total += non_loop[i] + (LOOP - 1) * loop[i]
    else:
        total += loop[i] * LOOP

print(total)
