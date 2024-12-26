"""
Advent of Code 2024 - Day 19
"""

from utils import Puzzle


class PuzzleSolution(Puzzle):
    """Puzzle day 19"""

    def __init__(self):
        super().__init__()

        self._towel_patterns = self.data[0].split(", ")
        self._design_list = self.data[2:]
        self._max_pattern_len = max(len(pattern) for pattern in self._towel_patterns)
        self._max_pattern_dict = {
            pattern_len: [
                pattern
                for pattern in self._towel_patterns
                if len(pattern) == pattern_len
            ]
            for pattern_len in range(0, self._max_pattern_len)
        }
        self._design_cache = {}

    def _is_matching_design(self, design: str) -> bool:
        """check if design can be composed by patterns combination"""
        if not design:
            return True
        if design in self._design_cache:
            return False
        for i in range(1, self._max_pattern_len):
            subdesign = design[0:i]
            if subdesign in self._max_pattern_dict[i]:
                if self._is_matching_design(design[i:]):
                    return True
                self._design_cache[design[i:]] = False
        return False

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        self._design_cache = {}
        return sum(self._is_matching_design(design) for design in self._design_list)

    def _counting_matching_design(self, design: str) -> int:
        """count how many patterns combination for each design can be composed"""
        if not design:
            return 1
        if design in self._design_cache:
            return self._design_cache[design]

        total = 0

        for i in range(len(design)):
            subdesign = design[0 : i + 1]
            if (
                len(subdesign) > self._max_pattern_len
                or subdesign not in self._towel_patterns
            ):
                continue
            total += self._counting_matching_design(design[i + 1 :])

        self._design_cache[design] = total
        return total

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        self._design_cache = {}
        return sum(
            self._counting_matching_design(design) for design in self._design_list
        )
