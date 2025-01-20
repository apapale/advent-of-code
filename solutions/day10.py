"""
Advent of Code 2024 - Day 10
"""

import numpy as np
from utils import Puzzle

_DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class PuzzleSolution(Puzzle):
    """Puzzle day 10"""

    def __init__(self):
        super().__init__()
        self.data = np.array([list(map(int, line)) for line in self.data])
        self._zeros = self._find_zeros()

    def _find_zeros(self) -> list:
        """search trailhead start"""
        return [
            [_c, _r]
            for _c in range(self._nrows)
            for _r in range(self._ncols)
            if self.data[_c][_r] == 0
        ]

    def _check_in_map(self, pos: list) -> bool:
        """check if position is in map"""
        return 0 <= pos[0] < self._nrows and 0 <= pos[1] < self._ncols

    def _possible_trail(self, pos_list: list, next_value: int) -> list:
        """search for possible trail"""
        trails = []
        for pos in pos_list:
            for direction in _DIRECTIONS:
                new_pos = tuple(x + y for x, y in zip(pos, direction))
                if self._check_in_map(new_pos):
                    if (
                        self.data[new_pos[0]][new_pos[1]] == next_value
                        and new_pos not in trails
                    ):
                        trails.append(new_pos)
        return trails

    def _get_trailhead_value(self, zero_pos: list, select_trail) -> int:
        """compute score or rating"""
        trail_list = [zero_pos]
        for _n in range(1, 10):
            trail_list = select_trail(trail_list, _n)
            if len(trail_list) == 0:
                return 0
        return len(trail_list)

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        return sum(
            self._get_trailhead_value(zero_pos, self._possible_trail)
            for zero_pos in self._zeros
        )

    def _all_trails(self, pos_list: list, next_value: int) -> list:
        """search all possible trails"""
        trails = []
        for pos in pos_list:
            for direction in _DIRECTIONS:
                new_pos = tuple(x + y for x, y in zip(pos, direction))
                if self._check_in_map(new_pos):
                    if self.data[new_pos[0]][new_pos[1]] == next_value:
                        trails.append(new_pos)
        return trails

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        return sum(
            self._get_trailhead_value(zero_pos, self._all_trails)
            for zero_pos in self._zeros
        )
