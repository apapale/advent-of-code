"""
Advent of Code 2024 - Day 12
"""

from typing import Callable
from utils import Puzzle

_DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class PuzzleSolution(Puzzle):
    """Puzzle day 12"""

    def __init__(self) -> None:
        super().__init__()
        self.data = [list(line) for line in self.data]
        self.regions = []
        self.assigned = [
            [False for _n in range(self._ncols)] for _n in range(self._nrows)
        ]

    def _check_in_map(self, pos: tuple) -> bool:
        """check if pos is in the map"""
        return 0 <= pos[0] < self._nrows and 0 <= pos[1] < self._ncols

    def _check_neighbours(self, r: int, c: int, plant_type: str) -> None:
        """check if all the neighbours are in the same garden"""
        for direction in _DIRECTIONS:
            new_r, new_c = tuple(_x + _y for _x, _y in zip((r, c), direction))
            if (
                self._check_in_map((new_r, new_c))
                and self.data[new_r][new_c] == plant_type
                and self.assigned[new_r][new_c] is False
            ):
                self.regions[-1][1].append((new_r, new_c))
                self.assigned[new_r][new_c] = True
                self._check_neighbours(new_r, new_c, plant_type)

    def _compute_gardens(self) -> None:
        """compute all gardens from data"""
        for _r in range(self._nrows):
            for _c in range(self._ncols):
                if self.assigned[_r][_c] is False:
                    plant_type = self.data[_r][_c]
                    self.regions.append([plant_type, [(_r, _c)]])
                    self.assigned[_r][_c] = True
                    self._check_neighbours(_r, _c, plant_type)

    def _compute_area(self, garden: list) -> int:
        """compute garden's area"""
        return len(garden[1])

    def _compute_plant_perimeter(self, plant: list, garden: list):
        """compute plant's perimeter"""
        return 4 - sum(
            1
            for direction in _DIRECTIONS
            if tuple(_x + _y for _x, _y in zip(plant, direction)) in garden[1]
        )

    def _compute_perimeter(self, garden: list) -> int:
        """compute garden's perimeter"""
        return sum(self._compute_plant_perimeter(plant, garden) for plant in garden[1])

    def _compute_price(self, perimeter_sides_func: Callable) -> int:
        """compute garden's price"""
        return sum(
            self._compute_area(garden) * perimeter_sides_func(garden)
            for garden in self.regions
        )

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        self._compute_gardens()
        return self._compute_price(self._compute_perimeter)

    def _compute_segments(self, garden: list) -> list:
        """compute all garden's segments"""
        segments = []
        for plant in garden[1]:
            for direction in _DIRECTIONS:
                neigh = tuple(_x + _y for _x, _y in zip(plant, direction))
                if neigh not in garden[1]:
                    segments.append([plant, neigh])
        return segments

    def _compute_sides(self, garden: list) -> int:
        """compute if segments belong to the same side"""
        segments = self._compute_segments(garden)
        count_sides = 0
        for _i, i_segment in enumerate(segments):
            _x, _y = i_segment
            direction = None
            other_dir = None
            for _k in [0, 1]:
                if _x[_k] == _y[_k]:
                    direction = _k
                else:
                    other_dir = _k
            for _, j_segment in enumerate(segments[_i + 1 :], start=_i + 1):
                _m, _n = j_segment
                if _m[direction] == _n[direction]:
                    _dx = _x[direction] - _m[direction]
                    if (
                        _dx in (1, -1)
                        and _x[other_dir] == _m[other_dir]
                        and _y[other_dir] == _n[other_dir]
                    ):
                        count_sides -= 1
            count_sides += 1
        return count_sides

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        return self._compute_price(self._compute_sides)
