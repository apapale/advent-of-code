"""
Advent of Code 2024 - Day 25
"""
from utils import Puzzle


class PuzzleSolution(Puzzle):
    """Puzzle day 25"""

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        space_index = self.data.index("")
        schematics = []

        while True:
            schematics.append(self.data[:space_index])
            self.data = self.data[space_index + 1 :]
            if "" not in self.data:
                schematics.append(self.data)
                break
            space_index = self.data.index("")

        lock_heights = []
        keys_heights = []
        for schematic in schematics:
            schematic_heights = [line.count("#") - 1 for line in zip(*schematic)]
            if schematic[0] == "#####" and schematic[-1] == ".....":
                lock_heights.append(schematic_heights)
            elif schematic[-1] == "#####" and schematic[0] == ".....":
                keys_heights.append(schematic_heights)
        return sum(
            all(l + k <= 5 for l, k in zip(lock_h, key_h))
            for lock_h in lock_heights
            for key_h in keys_heights
        )

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        return 0
