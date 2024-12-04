"""
Advent of Code 2024 - Day 1
"""

import numpy as np
from utils import Puzzle


class PuzzleSolution(Puzzle):
    """Puzzle day 1"""

    def __init__(self):
        """class init"""
        super().__init__()
        self.x = np.array([line.split() for line in self.data], dtype=int)

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        self.x[:, 0].sort()
        self.x[:, 1].sort()
        return sum(np.abs(self.x[i, 0] - self.x[i, 1]) for i in range(0, len(self.x)))

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        unique, counts = np.unique(self.x[:, 1], return_counts=True)
        xdict = dict(zip(unique, counts))
        return sum(xi * xdict[xi] for xi in self.x[:, 0] if xi in unique)
