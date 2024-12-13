"""
Advent of Code 2024 - Day 8
"""

from utils import Puzzle


class PuzzleSolution(Puzzle):
    """Puzzle day 8"""

    def __init__(self):
        super().__init__()
        self.data = [list(line) for line in self.data]
        self._antennas = [
            (r, c)
            for r in range(self._nrows)
            for c in range(self._nrows)
            if self.data[r][c] != "."
        ]

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        antinodes = []
        for i, antenna_i in enumerate(self._antennas):
            for j, antenna_j in enumerate(self._antennas[i + 1 :], start=i + 1):
                # same type
                if (
                    self.data[antenna_i[0]][antenna_i[1]]
                    == self.data[antenna_j[0]][antenna_j[1]]
                ):
                    # compute distance
                    distance = [x - y for x, y in zip(antenna_i, antenna_j)]
                    for k, sign in [(i, 1), (j, -1)]:
                        antenna_k = self._antennas[k]
                        # compute antinodes
                        antinode = tuple(
                            x + sign * y for x, y in zip(antenna_k, distance)
                        )
                        # check if antinodes inside map
                        if (
                            0 <= antinode[0] < self._nrows
                            and 0 <= antinode[1] < self._ncols
                        ):
                            # check if antinode is unique and not overlapping antennas
                            if antinode not in antinodes:
                                antinodes.append(antinode)
        return len(antinodes)

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        antinodes = []
        for i, antenna_i in enumerate(self._antennas):
            for j, antenna_j in enumerate(self._antennas[i + 1 :], start=i + 1):
                # same type
                if (
                    self.data[antenna_i[0]][antenna_i[1]]
                    == self.data[antenna_j[0]][antenna_j[1]]
                ):
                    # compute distance
                    distance = [x - y for x, y in zip(antenna_i, antenna_j)]
                    for k, sign in [(i, 1), (j, -1)]:
                        antenna_k = self._antennas[k]
                        if antenna_k not in antinodes:
                            antinodes.append(antenna_k)
                        # compute antinodes
                        antinode = tuple(
                            x + sign * y for x, y in zip(antenna_k, distance)
                        )
                        # check if antinodes inside map
                        while (
                            0 <= antinode[0] < self._nrows
                            and 0 <= antinode[1] < self._ncols
                        ):
                            # check if antinode is unique and not overlapping antennas
                            if antinode not in antinodes:
                                antinodes.append(antinode)
                            antinode = tuple(
                                x + sign * y for x, y in zip(antinode, distance)
                            )
        return len(antinodes)
