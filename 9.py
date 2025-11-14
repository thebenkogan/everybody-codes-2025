from collections import defaultdict
from ec import read_input


def similarity(d1, d2):
    total = 0
    for c1, c2 in zip(d1, d2):
        if c1 == c2:
            total += 1
    return total


def similarity_degree(dnas):
    return similarity(dnas[0], dnas[2]) * similarity(dnas[1], dnas[2])


lines = read_input(1)
dnas = []
for line in lines:
    d = line.split(":")[1]
    dnas.append(d)

print(similarity_degree(dnas))


def matches_child(child, parents):
    p1, p2 = parents
    for c, pc1, pc2 in zip(child, p1, p2):
        if c != pc1 and c != pc2:
            return False
    return True


def build_relationship(dnas):
    parents = []
    for i in range(len(dnas)):
        for j in range(i + 1, len(dnas)):
            parents.append((dnas[i], dnas[j]))

    parent_to_children = defaultdict(list)
    for pair in parents:
        for child in dnas:
            if child not in pair and matches_child(child, pair):
                parent_to_children[pair].append(child)

    return parent_to_children


lines = read_input(2)
dnas = []
for line in lines:
    d = line.split(":")[1]
    dnas.append(d)


total = 0
parent_to_children = build_relationship(dnas)
for (p1, p2), children in parent_to_children.items():
    for child in children:
        total += similarity_degree([p1, p2, child])

print(total)


lines = read_input(3)
dnas = []
dna_to_num = {}
for line in lines:
    num, d = line.split(":")
    dnas.append(d)
    dna_to_num[d] = int(num)

parent_to_children = build_relationship(dnas)
adj = defaultdict(list)
for (p1, p2), children in parent_to_children.items():
    for child in children:
        adj[p1].append(child)
        adj[p2].append(child)
        adj[child].extend([p1, p2])

seen = set()
best = []
for start in adj:
    if start in seen:
        continue
    seen.add(start)

    all_nums = []
    stack = [start]
    while len(stack) > 0:
        n = stack.pop()
        all_nums.append(dna_to_num[n])
        for neighbor in adj[n]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)

    if len(all_nums) > len(best):
        best = all_nums

print(sum(best))
