"""
Advent of Code 2024 - Day 1
"""

import numpy as np

with open("input.txt", encoding="utf-8") as f:
    data = f.read().splitlines()

x = np.array([line.split() for line in data], dtype=int)
x[:, 0].sort()
x[:, 1].sort()

result = sum(np.abs(x[i, 0] - x[i, 1]) for i in range(0, len(x)))

print(f"Day 1 part 1: {result}")

unique, counts = np.unique(x[:, 1], return_counts=True)
xdict = dict(zip(unique, counts))
result = sum(xi * xdict[xi] for xi in x[:, 0] if xi in unique)

print(f"Day 1 part 2: {result}")
