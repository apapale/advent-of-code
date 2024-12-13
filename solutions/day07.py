"""
Advent of Code 2024 - Day 7
"""

from typing import Callable
from utils import Puzzle


class PuzzleSolution(Puzzle):
    """Puzzle day 7"""

    def _add_element_plus_minus(self, current_combination: list, value: int) -> list:
        """add possible element to combination"""
        new_combination = []
        for comb in current_combination:
            new_combination.append(comb + value)
            new_combination.append(comb * value)
        return new_combination

    def _add_element_plus_minus_concat(
        self, current_combination: list, value: int
    ) -> list:
        """add possible element to combination"""
        new_combination = []
        for comb in current_combination:
            new_combination.append(comb + value)
            new_combination.append(comb * value)
            new_combination.append(int(str(comb) + str(value)))
        return new_combination

    def _compute_operators_combination(
        self, test_value: int, numbers: list, add_element_function: Callable
    ) -> int:
        """compute all possible combinations of operators"""
        all_combinations = [numbers[0]]
        for num in numbers[1:]:
            all_combinations = add_element_function(all_combinations, num)
        if any(combination == test_value for combination in all_combinations):
            return test_value
        return 0

    def _find_guard_pos(self) -> tuple:
        """search for guard initial position"""
        return None, None

    def _guard_path(self, data: list) -> tuple:
        """compute guard path and keeps track of visited sites"""

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        return sum(
            self._compute_operators_combination(
                int(line.split(":")[0]),
                list(map(int, line.split(":")[1].split())),
                self._add_element_plus_minus,
            )
            for line in self.data
        )

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        return sum(
            self._compute_operators_combination(
                int(line.split(":")[0]),
                list(map(int, line.split(":")[1].split())),
                self._add_element_plus_minus_concat,
            )
            for line in self.data
        )
