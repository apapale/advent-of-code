"""
Advent of Code 2024 - Day 18
"""

from utils import Puzzle

_DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, -1)]
_NMAX = 70


def _sum_tuple(v, w):
    return v[0] + w[0], v[1] + w[1]


class PuzzleSolution(Puzzle):
    """Puzzle day 18"""

    def __init__(self):
        super().__init__()
        self.data = [list(map(int, line.split(","))) for line in self.data]
        self.memory_space = []

        self.pos_start = (0, 0)
        self.pos_end = (_NMAX, _NMAX)
        self.path_collection = []
        self.best_score = -1

    def _is_free(self, pos: tuple) -> bool:
        """return bool if site free"""
        return self.memory_space[pos[0]][pos[1]] != "#"

    def _is_in_memory(self, pos: tuple) -> bool:
        """check if is inside memory"""
        return 0 <= pos[0] <= _NMAX and 0 <= pos[1] <= _NMAX

    def _get_possible_moves(self, pos: tuple, distance_nodes: dict) -> list:
        """return list of possible positions and directions"""
        moves_available = []
        for direction in _DIRECTIONS:
            new_pos = _sum_tuple(pos, direction)
            if (
                self._is_in_memory(new_pos)
                and self._is_free(new_pos)
                and new_pos not in distance_nodes
            ):
                moves_available.append(new_pos)
        return moves_available

    def _compute_best_paths(self) -> None:
        """compute all best paths"""
        site_cache = {}
        # position, path, score
        queued_sites = [(self.pos_start, [self.pos_start], 0)]

        while queued_sites:
            pos, current_path, score = queued_sites.pop(0)

            if pos == self.pos_end:
                self.path_collection.append((current_path, score))
                continue

            if pos in site_cache and site_cache[pos] <= score:
                continue
            site_cache[pos] = score

            moves_available = self._get_possible_moves(pos, current_path)
            for new_pos in moves_available:
                queued_sites.append((new_pos, current_path + [new_pos], score + 1))

    def _prepare_memory_space(self, max_index: int) -> None:
        """set up path collection and memory space"""
        self.path_collection = []
        self.memory_space = [
            ["." for _c in range(0, _NMAX + 1)] for _r in range(0, _NMAX + 1)
        ]
        for index in self.data[:max_index]:
            self.memory_space[index[1]][index[0]] = "#"

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        self._prepare_memory_space(1024)
        self._compute_best_paths()
        self.best_score = min(path[1] for path in self.path_collection)
        return self.best_score

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        min_length = 1024
        max_length = len(self.data)

        while max_length - min_length > 1:
            test_length = (max_length + min_length) // 2
            self._prepare_memory_space(test_length)
            self._compute_best_paths()
            if len(self.path_collection) > 0:
                min_length = test_length
            else:
                max_length = test_length

        return str(self.data[min_length][0]) + "," + str(self.data[min_length][1])
