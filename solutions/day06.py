"""
Advent of Code 2024 - Day 6
"""

import copy
from utils import Puzzle

_DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class PuzzleSolution(Puzzle):
    """Puzzle day 6"""

    def __init__(self):
        super().__init__()
        self.data = [list(line) for line in self.data]
        self._map_visited_part1 = {}

    def _find_guard_pos(self) -> tuple:
        """search for guard initial position"""

        def _find_guard_pos_with_error(line):
            try:
                return line.index("^")
            except ValueError:
                return None

        for _y, line in enumerate(self.data):
            _x = _find_guard_pos_with_error(line)
            if _x is not None:
                return _y, _x
        return None, None

    def _guard_path(self, data: list) -> tuple:
        """compute guard path and keeps track of visited sites"""
        guard_y, guard_x = self._find_guard_pos()
        index_direction = 0
        _map_visited = {}
        _map_visited[(guard_y, guard_x)] = [index_direction]

        while True:
            new_guard_y, new_guard_x = (
                guard_y + _DIRECTIONS[index_direction][0],
                guard_x + _DIRECTIONS[index_direction][1],
            )

            if (
                new_guard_y < 0
                or new_guard_y >= self._nrows
                or new_guard_x < 0
                or new_guard_x >= self._ncols
            ):
                return True, _map_visited
            if data[new_guard_y][new_guard_x] == "#":
                # 90 degrees rotation to change direction
                index_direction = (index_direction + 1) % 4
                continue
            guard_y, guard_x = new_guard_y, new_guard_x
            if (guard_y, guard_x) in _map_visited:
                if index_direction in _map_visited[(guard_y, guard_x)]:
                    # it's a loop
                    return False, None
                _map_visited[(guard_y, guard_x)].append(index_direction)
            else:
                _map_visited[(guard_y, guard_x)] = [index_direction]

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        _, self._map_visited_part1 = self._guard_path(self.data)
        return len(self._map_visited_part1)

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        self._map_visited_part1.pop(self._find_guard_pos())
        loop_count = 0
        for map_pos in self._map_visited_part1:
            data_obs = copy.deepcopy(self.data)
            data_obs[map_pos[0]][map_pos[1]] = "#"
            is_loop, _ = self._guard_path(data_obs)
            if is_loop is False:
                loop_count += 1
        return loop_count
