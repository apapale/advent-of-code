"""
Advent of Code 2024 - Day 14
"""

import matplotlib.pyplot as plt
import numpy as np
from utils import Puzzle

def _multiple_vect(x, a):
    """multiplay array for a scalar"""
    return [x[0] * a, x[1] * a]

def _sum_vect(a, b):
    """sum two arrays element by element"""
    return [x + y for x, y in zip(a, b)]

class PuzzleSolution(Puzzle):
    """Puzzle day 14"""

    def __init__(self):
        super().__init__()
        self._wide = 101
        self._tall = 103

        self._robots = []
        for line in self.data:
            pos, vel = line.split(" ")
            x, y = map(int, pos[2:].split(","))
            vx, vy = map(int, vel[2:].split(","))
            self._robots.append(([x, y], [vx, vy]))

    def _pbc(self, pos):
        """rescale position inside box"""
        return [pos[0] % self._wide, pos[1] % self._tall]

    def _compute_final_position(self, robots, run_time):
        """compute all robots final positions"""
        final_positions = []
        for pos, vel in robots:
            x, y = self._pbc(_sum_vect(pos, _multiple_vect(vel, run_time)))
            # remove if on central stripes
            if x == self._wide // 2 or y == self._tall // 2:
                continue
            final_positions.append([x, y])
        return final_positions

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        run_time = 100
        final_positions = self._compute_final_position(self._robots, run_time)

        q_top_left = sum(
            True
            for pos in final_positions
            if pos[0] <= (self._wide - 1) / 2 and pos[1] <= (self._tall - 1) / 2
        )
        q_top_right = sum(
            True
            for pos in final_positions
            if pos[0] >= (self._wide + 1) / 2 and pos[1] <= (self._tall - 1) / 2
        )
        q_bottom_left = sum(
            True
            for pos in final_positions
            if pos[0] <= (self._wide - 1) / 2 and pos[1] >= (self._tall + 1) / 2
        )
        q_bottom_right = sum(
            True
            for pos in final_positions
            if pos[0] >= (self._wide + 1) / 2 and pos[1] >= (self._tall + 1) / 2
        )
        return q_top_left * q_top_right * q_bottom_left * q_bottom_right

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        run_time = 7753
        final_positions = self._compute_final_position(self._robots, run_time)

        robots_np = np.zeros((self._wide, self._tall))
        plt.figure(figsize=(6, 6))

        for x, y in final_positions:
            robots_np[x][y] += 1
        ax = plt.subplot(1, 1, 1)
        ax.imshow(robots_np)
        plt.show()
        return run_time
