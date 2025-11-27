from ec import nums, read_input


def read_layers(plants):
    sections = plants.split("\n\n")
    layers = [[]]
    plant_to_layer = {}
    for plant in sections:
        ns = nums(plant)
        n = ns[0]
        t = ns[1]
        if "free" in plant:
            layers[0].append((n, t, []))
            plant_to_layer[n] = 0
        else:
            connections = []
            layer = 0
            for i in range(2, len(ns), 2):
                connections.append((ns[i], ns[i + 1]))
                layer = max(layer, plant_to_layer[ns[i]])
            layer += 1

            if layer >= len(layers):
                layers.append([])

            plant_to_layer[n] = layer
            layers[layer].append((n, t, connections))

    return layers


def forward(layers, v):
    for layer in layers[1:]:
        next_v = {}
        for n, t, conns in layer:
            energy = 0
            for c, ct in conns:
                energy += v[c] * ct
            if energy < t:
                energy = 0
            next_v[n] = energy
        v = next_v

    return v


lines = read_input(1, split_lines=False)
layers = read_layers(lines)
v = {n: 1 for (n, _, _) in layers[0]}
v = forward(layers, v)
print(list(v.values())[0])

lines = read_input(2, split_lines=False)
plants, inputs = lines.split("\n\n\n")
layers = read_layers(plants)
final_thickness = layers[-1][0][1]
inputs = [nums(i) for i in inputs.split("\n")]
total = 0
for i in inputs:
    v = {index + 1: val for (index, val) in enumerate(i)}
    v = forward(layers, v)
    result = list(v.values())[0]
    if result >= final_thickness:
        total += result

print(total)

lines = read_input(3, split_lines=False)
plants, inputs = lines.split("\n\n\n")
layers = read_layers(plants)
final_thickness = layers[-1][0][1]
inputs = [nums(i) for i in inputs.split("\n")]
total = 0
best = 0
for i in inputs:
    orig = {index + 1: val for (index, val) in enumerate(i)}
    v = forward(layers, orig)
    result = list(v.values())[0]
    if result < final_thickness:
        continue

    total += 13080 - result

    if result > best:
        best = result
        best_i = orig

print(total)

# we try to toggle the input of each position in the best performing input vector
# if that change results in a greater best output, then this is now the best vector
# it turns out for my input that we only need 1 toggle and that yields the maximum
for i in range(len(best_i)):
    best_i[i + 1] = 1 if best_i[i + 1] == 0 else 0
    after = forward(layers, best_i)
    result = list(after.values())[0]
    if result > best:
        print(result)
    best_i[i + 1] = 1 if best_i[i + 1] == 0 else 0
