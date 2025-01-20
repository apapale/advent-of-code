"""
Advent of Code 2024 - Day 23
"""

import itertools
from utils import Puzzle


class PuzzleSolution(Puzzle):
    """Puzzle day 23"""

    def __init__(self):
        super().__init__()
        _edges = [_line.split("-") for _line in self.data]
        self._graph = {}
        for _x, _y in _edges:
            if _x not in self._graph:
                self._graph[_x] = []
            self._graph[_x].append(_y)
            if _y not in self._graph:
                self._graph[_y] = []
            self._graph[_y].append(_x)

    def _is_cycle(self, nodes: tuple) -> bool:
        """check if all noeds are connected"""
        for _i, _ni in enumerate(nodes):
            for _nj in nodes[_i + 1 :]:
                if _ni not in self._graph[_nj]:
                    return False
        return True

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        triplets = set()
        for _vertex, _neighs in self._graph.items():
            for _i, _vi in enumerate(_neighs[:-1]):
                for _vj in _neighs[_i + 1 :]:
                    if _vj in self._graph[_vi]:
                        triplets.add(tuple([_vertex, _vi, _vj]))
        return sum(("t" in [x[0] for x in triple]) for triple in triplets) // 3

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        _connected_set = []
        for _vertex, _neighs in self._graph.items():
            for _i in range(len(_neighs), 1, -1):
                if _i < len(_connected_set):
                    break
                for comb in itertools.combinations(_neighs, r=_i):
                    if self._is_cycle(comb):
                        _connected_set = max(
                            list(comb) + [_vertex], _connected_set, key=len
                        )
                        break
        _connected_set.sort()
        return ",".join(_connected_set)
