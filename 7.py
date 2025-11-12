from collections import defaultdict
from ec import read_input


def get_input(part):
    lines = read_input(part, split_lines=False)
    names, rules = lines.split("\n\n")
    names = names.split(",")
    rules = rules.split("\n")

    adj = defaultdict(list)
    for rule in rules:
        src, dst = rule.split(" > ")
        adj[src].extend(dst.split(","))

    return adj, names


def is_valid(adj, name):
    nxt = adj[name[0]]
    for c in name[1:]:
        if c not in nxt:
            return False
        nxt = adj[c]
    return True


adj1, names = get_input(1)
print(next(name for name in names if is_valid(adj1, name)))

adj2, names = get_input(2)
print(sum(i + 1 for i, name in enumerate(names) if is_valid(adj2, name)))

adj3, prefixes = get_input(3)
prefixes = [prefix for prefix in prefixes if is_valid(adj3, prefix)]
seen = set(prefixes)
total = 0
while len(prefixes) > 0:
    prefix = prefixes.pop()
    if 7 <= len(prefix) <= 11:
        total += 1
    if len(prefix) == 11:
        continue
    for c in adj3[prefix[-1]]:
        nxt = prefix + c
        if nxt not in seen:
            seen.add(nxt)
            prefixes.append(nxt)

print(total)
