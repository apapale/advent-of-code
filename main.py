"""Advent of Code puzzles runnner."""

import argparse
import importlib
import shutil
import os


def main():
    """main function to select and solve daily puzzles"""
    parser = argparse.ArgumentParser(description="Advent of Code runner.")
    parser.add_argument(
        "-d", dest="day", default=None, required=True, type=int, help="day of AoC"
    )
    args = parser.parse_args()

    shutil.copyfile(f"input/input_{args.day:02d}.txt", "input.txt")
    daily_puzzle = importlib.import_module(f"solutions.day{args.day:02d}")
    p = daily_puzzle.PuzzleSolution()
    print(f"Day {args.day} solutions:")
    print(f"Part 1 {p.solve_part1()}")
    print(f"Part 2 {p.solve_part2()}")
    os.remove("input.txt")


if __name__ == "__main__":
    main()
