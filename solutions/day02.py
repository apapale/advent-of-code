"""
Advent of Code 2024 - Day 2
"""

import numpy as np
from utils import Puzzle

_DECREASING_ARRAY = np.array([1, 2, 3])
_INCREASING_ARRAY = (-1) * _DECREASING_ARRAY


class PuzzleSolution(Puzzle):
    """Puzzle day 2"""

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        return _count_safe(self.data)

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        return _count_safe(self.data, _is_safe_part2)


def _parse_line(in_str: str) -> np.array:
    return np.array(in_str.split(), dtype=int)


def _compute_diff(in_array: np.array) -> np.array:
    return in_array[:-1] - in_array[1:]


def _unique_diff(in_array: np.array) -> np.array:
    return np.unique(_compute_diff(in_array))


def _remove(in_array: np.array, index: int) -> np.array:
    return np.concatenate((in_array[:index], in_array[index + 1 :]))


def _is_safe(in_array: np.array) -> bool:
    unique = _unique_diff(in_array)
    return (unique[:, None] == _INCREASING_ARRAY).any(axis=1).all() or (
        unique[:, None] == _DECREASING_ARRAY
    ).any(axis=1).all()


def _is_safe_part2(in_array: np.array) -> bool:
    """Check if one sub array is safe"""
    return np.array(
        [_is_safe(_remove(in_array, i)) for i in range(0, len(in_array))]
    ).any()


def _count_safe(in_data: list, _is_safe_function=_is_safe) -> int:
    """Count all save arrays"""
    return sum(_is_safe_function(_parse_line(line)) for line in in_data)
