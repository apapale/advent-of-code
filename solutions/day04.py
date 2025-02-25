"""
Advent of Code 2024 - Day 4
"""

from utils import Puzzle

_XMAS = "XMAS"
_SAMX = "SAMX"
_MS = {"M", "S"}


class PuzzleSolution(Puzzle):
    """Puzzle day 4"""

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        lines = self.data[:]

        lines.extend(
            ["".join([row[i] for row in self.data]) for i in range(len(self.data[0]))]
        )

        diagonals = {r - c: [] for r in range(self._nrows) for c in range(self._ncols)}
        antidiagonals = {
            r + c: [] for r in range(self._nrows) for c in range(self._ncols)
        }

        for _r in range(self._nrows):
            for _c in range(self._ncols):
                diagonals[_r - _c].append(self.data[_r][_c])
                antidiagonals[_r + _c].append(self.data[_r][_c])

        lines.extend(["".join(subdiagonal) for subdiagonal in diagonals.values()])
        lines.extend(["".join(subdiagonal) for subdiagonal in antidiagonals.values()])
        return sum(line.count(_XMAS) + line.count(_SAMX) for line in lines)

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        return sum(
            self.is_x_mas(_r, _c)
            for _r in range(1, self._nrows - 1)
            for _c in range(1, self._ncols - 1)
            if self.data[_r][_c] == "A"
        )

    def is_x_mas(self, r: int, c: int) -> bool:
        """check if X-MAS appeaars"""
        return {self.data[r - 1][c - 1], self.data[r + 1][c + 1]} == _MS and {
            self.data[r - 1][c + 1],
            self.data[r + 1][c - 1],
        } == _MS
