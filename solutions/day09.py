"""
Advent of Code 2024 - Day 9
"""

from dataclasses import dataclass
from utils import Puzzle


@dataclass
class Block:
    """memory block"""

    index: int
    block_type: bool  # 1 is a file, 0 is free space


@dataclass
class Segment:
    """segment of blocks"""

    index: int
    block_type: bool  # 1 is a file, 0 is free space
    lenght: int


class PuzzleSolution(Puzzle):
    """Puzzle day 9"""

    def __init__(self):
        super().__init__()
        self._disk_map = self.data[0]
        self._all_disk = []

    def _parse_blocks(self) -> None:
        """parse disk map in blocks"""

        self._all_disk = []
        index, block_type = 0, True

        for i in map(int, self._disk_map):
            if block_type is True:
                for _ in range(i):
                    self._all_disk.append(Block(index, block_type))
                index += 1
            else:
                for _ in range(i):
                    self._all_disk.append(Block(None, block_type))

            block_type = not block_type

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        self._parse_blocks()
        spaces = sum(1 for block in self._all_disk if block.block_type is False)

        while spaces:
            empty_space = None
            if self._all_disk[-1].block_type is True:
                for i, block in enumerate(self._all_disk):
                    if block.block_type is False:
                        empty_space = i
                        break
                if empty_space is not None:
                    self._all_disk[empty_space].block_type = True
                    self._all_disk[empty_space].index = self._all_disk[-1].index
                    spaces -= 1
                    self._all_disk.pop()
            else:
                spaces -= 1
                self._all_disk.pop()

        return sum(
            i * block.index
            for i, block in enumerate(self._all_disk)
            if block.block_type is True
        )

    def _parse_segments(self) -> None:
        """parse disk map in segments"""
        self._all_disk = []
        index, block_type = 0, True
        for i in map(int, self._disk_map):
            if block_type is True:
                self._all_disk.append(Segment(index, block_type, i))
                index += 1
            else:
                self._all_disk.append(Segment(None, block_type, i))
            block_type = not block_type

    def _compute_checksum_from_segments(self) -> int:
        check_sum = 0
        index_i = 0
        for segment in self._all_disk:
            if segment.block_type is True:
                for _ in range(segment.lenght):
                    check_sum += index_i * segment.index
                    index_i += 1
            else:
                index_i += segment.lenght
        return check_sum

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        self._parse_segments()
        for k in range(len(self._all_disk) - 1, 1, -1):
            if self._all_disk[k].block_type is True:
                empty_space = None
                for i, segment in enumerate(self._all_disk[:k]):
                    if segment.block_type is False:
                        if segment.lenght >= self._all_disk[k].lenght:
                            empty_space = i
                            break
                if empty_space is not None:
                    self._all_disk[empty_space].lenght -= self._all_disk[k].lenght
                    self._all_disk.insert(
                        empty_space,
                        Segment(
                            self._all_disk[k].index,
                            self._all_disk[k].block_type,
                            self._all_disk[k].lenght,
                        ),
                    )

                    self._all_disk[k + 1].block_type = False
                    self._all_disk[k + 1].index = None

        return self._compute_checksum_from_segments()
