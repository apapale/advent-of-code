"""
Advent of Code 2024 - Day 20
"""

from utils import Puzzle

_DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def _sum_tuple(v: tuple, w: tuple) -> tuple:
    return v[0] + w[0], v[1] + w[1]


def _diff_tuple(v: tuple, w: tuple) -> tuple:
    return v[0] - w[0], v[1] - w[1]


class PuzzleSolution(Puzzle):
    """Puzzle day 20"""

    def __init__(self):
        super().__init__()
        self.data = [list(line) for line in self.data]
        self._pos_start = self._find_start()
        self._pos_end = self._find_end()
        self._nmax = len(self.data)
        self._shortest_path = []
        self._site_time = {}

    def _find_pattern(self, pattern: str) -> tuple:
        for _l, _line in enumerate(self.data):
            for _r, _row in enumerate(_line):
                if _line[_r] == pattern:
                    return _l, _r
        return None, None

    def _find_start(self) -> tuple:
        return self._find_pattern("S")

    def _find_end(self) -> tuple:
        return self._find_pattern("E")

    def _is_free(self, pos: tuple) -> bool:
        """return bool if site free"""
        return self.data[pos[0]][pos[1]] != "#"

    def _is_wall(self, pos: tuple) -> bool:
        """return bool if site free"""
        return self.data[pos[0]][pos[1]] == "#"

    def _is_in_memory(self, pos: tuple) -> bool:
        """check if is inside memory"""
        return 0 <= pos[0] < self._nmax and 0 <= pos[1] < self._nmax

    def _get_possible_moves(self, pos: tuple, visited_sites: dict) -> list:
        """return list of possible positions and directions"""
        moves_available = []
        for direction in _DIRECTIONS:
            new_pos = _sum_tuple(pos, direction)
            if (
                self._is_in_memory(new_pos)
                and self._is_free(new_pos)
                and new_pos not in visited_sites
            ):
                moves_available.append(new_pos)
        return moves_available

    def _find_shortest_path(self) -> tuple[list, dict]:
        """compute shortest path without cheating"""
        current_site = self._pos_start
        step_index = 0
        shortest_path = [self._pos_start]
        site_time = {}

        while True:
            site_time[current_site] = step_index
            if current_site == self._pos_end:
                return shortest_path, site_time

            # there will be always only one possible move and one path
            moves_available = self._get_possible_moves(current_site, shortest_path)
            new_site = moves_available[0]
            step_index += 1
            shortest_path += [new_site]
            current_site = new_site

    def _compare_sites_distance(self, x: tuple, y: tuple, cheat_limit: int) -> bool:
        site_diff = _diff_tuple(x, y)
        distance = abs(site_diff[0]) + abs(site_diff[1])
        if distance <= cheat_limit:
            time_saved = self._site_time[y] - self._site_time[x] - distance
            if time_saved >= 100:
                return True
        return False

    def _find_cheat_path_short(self, cheat_limit: int) -> int:
        count_valid_cheats = 0

        for i, pos in enumerate(self._shortest_path[:-1]):
            count_valid_cheats += sum(
                self._compare_sites_distance(pos, next_pos, cheat_limit)
                for next_pos in self._shortest_path[i:]
            )

        return count_valid_cheats

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        self._shortest_path, self._site_time = self._find_shortest_path()
        return self._find_cheat_path_short(2)

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        return self._find_cheat_path_short(20)
