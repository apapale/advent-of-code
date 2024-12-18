"""
Advent of Code 2024 - Day 16
"""

from utils import Puzzle

_DIRECTIONS = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def _sum_tuple(v, w):
    return v[0] + w[0], v[1] + w[1]


class PuzzleSolution(Puzzle):
    """Puzzle day 16"""

    def __init__(self):
        super().__init__()
        self.data = [list(line) for line in self.data]
        self.pos_start, self.pos_end = self._find_start_end()
        self.path_collection = []
        self.best_score = -1

    def _find_start_end(self) -> tuple:
        """search initial and final position"""
        pos_start = None
        pos_end = None
        for x, line in enumerate(self.data):
            for y, m in enumerate(line):
                if m == "S":
                    pos_start = (x, y)
                if m == "E":
                    pos_end = (x, y)
        return pos_start, pos_end

    def _is_free(self, pos: tuple) -> bool:
        """return bool if site free"""
        return self.data[pos[0]][pos[1]] != "#"

    def _get_possible_moves(
        self, pos: tuple, direction: int, current_path: list
    ) -> list:
        """return list of possible positions and directions"""
        moves_available = []
        for idir, new_direction in enumerate(_DIRECTIONS):
            if (direction + 2) % 4 != idir:
                new_pos = _sum_tuple(pos, new_direction)
                if self._is_free(new_pos) and new_pos not in current_path:
                    moves_available.append((new_pos, idir))
        return moves_available

    def _compute_best_paths(self) -> None:
        """compute all best paths"""
        site_cache = {}
        queued_sites = [(self.pos_start, 0, [self.pos_start], 0)]

        while queued_sites:
            pos, direction, current_path, score = queued_sites.pop(0)

            if pos == self.pos_end:
                self.path_collection.append((current_path, score))
                continue

            if (pos, direction) in site_cache and site_cache[(pos, direction)] < score:
                continue

            site_cache[(pos, direction)] = score
            moves_available = self._get_possible_moves(pos, direction, current_path)
            for new_pos, idir in moves_available:
                if idir == direction:
                    queued_sites.append(
                        (new_pos, idir, current_path + [new_pos], score + 1)
                    )
                else:
                    queued_sites.append((pos, idir, current_path, score + 1000))

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        self._compute_best_paths()
        self.best_score = min(path[1] for path in self.path_collection)
        return self.best_score

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        best_paths = [
            path[0] for path in self.path_collection if path[1] == self.best_score
        ]
        return len({site for path in best_paths for site in path})
