"""Puzzle base class"""

import abc


class Puzzle(abc.ABC):
    """Puzzle base class"""

    def __init__(self):
        with open("input.txt", encoding="utf-8") as f:
            self.data = f.read().splitlines()
        self._nrows = len(self.data)
        self._ncols = len(self.data[0])

    @abc.abstractmethod
    def solve_part1(self) -> int:
        """solve first part of the puzzle"""

    @abc.abstractmethod
    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
