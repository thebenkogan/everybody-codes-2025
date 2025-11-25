from math import lcm, prod
from ec import read_input

nums = [int(n) for n in read_input(1, split_lines=False).split(",")]
cols = [0 for _ in range(90)]
for n in nums:
    for i in range(n - 1, len(cols), n):
        cols[i] += 1

print(sum(cols))


def get_original(nums):
    i = 0
    orig = []
    while i < len(nums):
        if nums[i] > 0:
            for j in range(i, len(nums), i + 1):
                nums[j] -= 1
            orig.append(i + 1)
        i += 1

    return orig


nums = [int(n) for n in read_input(2, split_lines=False).split(",")]
orig = get_original(nums)
print(prod(orig))

nums = [int(n) for n in read_input(3, split_lines=False).split(",")]
total_blocks = 202520252025000
orig = get_original(nums)
orig_lcm = lcm(*orig)

# total blocks = 202520252025000 = cols / n1 + cols / n2 + ... cols / n for n in orig
# cols = 202520252025000 * lcm / sum(lcm / n for n in orig)
# each division has to be integer division since we don't allow partials
# so the answer will be a bit bigger than this result, idk how to compute it without manually checking

denominator = sum(orig_lcm / n for n in orig)
numerator = total_blocks * orig_lcm
ans = int(numerator / denominator)

while True:
    blocks = sum(ans // n for n in orig)
    if blocks > total_blocks:
        print(ans - 1)
        break
    ans += 1
