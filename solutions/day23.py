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
        for x, y in _edges:
            if x not in self._graph:
                self._graph[x] = []
            self._graph[x].append(y)
            if y not in self._graph:
                self._graph[y] = []
            self._graph[y].append(x)

    def _is_cycle(self, nodes: tuple) -> bool:
        """check if all noeds are connected"""
        for i, ni in enumerate(nodes):
            for nj in nodes[i + 1 :]:
                if ni not in self._graph[nj]:
                    return False
        return True

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        triplets = set()
        for vertex, neighs in self._graph.items():
            for i, vi in enumerate(neighs[:-1]):
                for vj in neighs[i + 1 :]:
                    if vj in self._graph[vi]:
                        triplets.add(tuple([vertex, vi, vj]))
        return sum(("t" in [x[0] for x in triple]) for triple in triplets) // 3

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        _connected_set = []
        for vertex, neighs in self._graph.items():
            for i in range(len(neighs), 1, -1):
                if i < len(_connected_set):
                    break
                for comb in itertools.combinations(neighs, r=i):
                    if self._is_cycle(comb):
                        _connected_set = max(
                            list(comb) + [vertex], _connected_set, key=len
                        )
                        break
        _connected_set.sort()
        return ",".join(_connected_set)
