"""
Advent of Code 2024 - Day 11
"""

from utils import Puzzle


class PuzzleSolution(Puzzle):
    """Puzzle day 11"""

    _stone_cache = {}

    def _recursive_blink(self, stone: int, n_blinking: int) -> int:
        """compute recursively number of stones at each blink"""
        if n_blinking == 0:
            return 1
        if (stone, n_blinking) in self._stone_cache:
            return self._stone_cache[(stone, n_blinking)]
        if stone == 0:
            n_stones = self._recursive_blink(1, n_blinking - 1)
        else:
            if len(str(stone)) % 2 == 0:
                stone_str = str(stone)
                stone_left, stone_right = int(
                    stone_str[: int(len(stone_str) / 2)]
                ), int(stone_str[int(len(stone_str) / 2) :])
                n_stones = self._recursive_blink(
                    stone_left, n_blinking - 1
                ) + self._recursive_blink(stone_right, n_blinking - 1)
            else:
                n_stones = self._recursive_blink(stone * 2024, n_blinking - 1)
        self._stone_cache[(stone, n_blinking)] = n_stones
        return n_stones

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        stones_now = list(map(int, self.data[0].split()))
        return sum(self._recursive_blink(stone, 25) for stone in stones_now)

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        stones_now = list(map(int, self.data[0].split()))
        return sum(self._recursive_blink(stone, 75) for stone in stones_now)
