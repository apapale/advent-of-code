"""
Advent of Code 2024 - Day 3
"""

from re import findall
from utils import Puzzle


class PuzzleSolution(Puzzle):
    """Puzzle day 3"""

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        pattern = r"mul\((\d+),(\d+)\)"
        return sum(int(a) * int(b) for a, b in findall(pattern, "".join(self.data)))

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        enabled = True
        pattern = r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))"
        result = 0

        for a, b, do, dont in findall(pattern, "".join(self.data)):
            if do or dont:
                enabled = bool(do)
            else:
                if enabled:
                    result += int(a) * int(b)
        return result
