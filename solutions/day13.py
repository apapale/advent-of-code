"""
Advent of Code 2024 - Day 13
"""

# from typing import Callable
from utils import Puzzle


class PuzzleSolution(Puzzle):
    """Puzzle day 13"""

    def _chunker(self, seq, size):
        """chunk file"""
        return (seq[pos : pos + size] for pos in range(0, len(seq), size))

    def _get_x_y_move(self, x):
        """get x y from move line"""
        split_input = x.split(" ")
        return int(split_input[2].split("+")[1].split(",")[0]), int(
            split_input[3].split("+")[1]
        )

    def _get_x_y_price(self, x):
        """get x y from price line"""
        split_input = x.split(" ")
        return int(split_input[1].split("=")[1].split(",")[0]), int(
            split_input[2].split("=")[1]
        )

    def _sum_button(self, a, b):
        """sum tuples"""
        return tuple(x + y for x, y in zip(a, b))

    def _cross_prod(self, a, b):
        """cross product of tuples"""
        return a[0] * b[1] - a[1] * b[0]

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        self.data.append(" ")
        max_token = 100
        cost = 0
        for x, y, z, _ in self._chunker(self.data, 4):
            a = self._get_x_y_move(x)
            b = self._get_x_y_move(y)
            p = self._get_x_y_price(z)
            b_times = self._cross_prod(a, p) / self._cross_prod(a, b)
            a_times = (p[0] - b[0] * b_times) / a[0]
            if (
                max_token >= a_times >= 0
                and max_token >= b_times >= 0
                and a_times.is_integer()
                and b_times.is_integer()
            ):
                cost += int(a_times) * 3 + int(b_times)
        return cost

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        max_token = 10000000000000
        cost = 0
        for x, y, z, _ in self._chunker(self.data, 4):
            a = self._get_x_y_move(x)
            b = self._get_x_y_move(y)
            p = self._get_x_y_price(z)
            p = self._sum_button(p, (max_token, max_token))
            b_times = self._cross_prod(a, p) / self._cross_prod(a, b)
            a_times = (p[0] - b[0] * b_times) / a[0]
            if (
                max_token >= a_times >= 0
                and max_token >= b_times >= 0
                and a_times.is_integer()
                and b_times.is_integer()
            ):
                cost += int(a_times) * 3 + int(b_times)
        return cost
