"""
Advent of Code 2024 - Day 15
"""

from typing import Callable
from utils import Puzzle

_MOVEMENTS = {">": [0, 1], "<": [0, -1], "^": [-1, 0], "v": [1, 0]}
_SPLIT_SITES = {"#": ["#", "#"], "@": ["@", "."], "O": ["[", "]"], ".": [".", "."]}


def _sum_list(a: list, b: list) -> list:
    """sum two list element by element"""
    return [_x + _y for _x, _y in zip(a, b)]


class PuzzleSolution(Puzzle):
    """Puzzle day 15"""

    def __init__(self):
        super().__init__()
        self._warehouse_map = []
        self._warehouse_map_double = []
        self._moves = []
        self._nrows = 0
        self._ncols = 0

    def _find_robot(self) -> list:
        """search for robot initial position"""

        def _find_robot_with_error(line):
            try:
                return line.index("@")
            except ValueError:
                return None

        for _y, line in enumerate(self._warehouse_map):
            _x = _find_robot_with_error(line)
            if _x is not None:
                return [_y, _x]
        return [None, None]

    def _is_empty(self, pos: list) -> bool:
        """return bool if empty"""
        return self._warehouse_map[pos[0]][pos[1]] == "."

    def _is_wall(self, pos: list) -> bool:
        """return bool if wall"""
        return self._warehouse_map[pos[0]][pos[1]] == "#"

    def _is_box(self, pos: list) -> bool:
        """return bool if single site box"""
        return self._warehouse_map[pos[0]][pos[1]] == "O"

    def _is_robot(self, pos: list) -> bool:
        """return bool if robot"""
        return self._warehouse_map[pos[0]][pos[1]] == "@"

    def _move_box(self, pos: list, move: list) -> None:
        """move box"""
        new_pos = _sum_list(pos, move)
        move_this_box = False
        if self._is_box(new_pos) and self._box_can_be_moved(new_pos, move):
            self._move_box(new_pos, move)
            move_this_box = True
        if self._is_empty(new_pos):
            move_this_box = True
        if move_this_box:
            self._warehouse_map[pos[0]][pos[1]] = "."
            self._warehouse_map[new_pos[0]][new_pos[1]] = "O"

    def _box_can_be_moved(self, pos: list, move: list) -> bool:
        """current box can be moved"""
        new_pos = _sum_list(pos, move)
        if self._is_empty(new_pos):
            return True
        if self._is_box(new_pos):
            return self._box_can_be_moved(new_pos, move)
        return False

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        data_index = self.data.index("")
        self._warehouse_map = [list(line) for line in self.data[:data_index]]
        self._moves = [list(line) for line in self.data[data_index + 1 :]]
        self._nrows = len(self._warehouse_map)
        self._ncols = len(self._warehouse_map[0])
        robot_pos = self._find_robot()

        for move_line in self._moves:
            for move in move_line:
                new_robot_pos = self._move_robot(
                    robot_pos,
                    _MOVEMENTS[move],
                    self._is_box,
                    self._box_can_be_moved,
                    self._move_box,
                )
                robot_pos = new_robot_pos
        return sum(
            100 * _y + _x
            for _y in range(self._nrows)
            for _x in range(self._ncols)
            if self._is_box([_y, _x])
        )

    def _move_robot(
        self,
        pos: list,
        move: list,
        is_box_func: Callable,
        box_can_be_moved_func: Callable,
        move_box_func: Callable,
    ) -> list:
        """move robot"""
        new_pos = _sum_list(pos, move)
        if self._is_wall(new_pos):
            return pos
        if is_box_func(new_pos):
            if box_can_be_moved_func(new_pos, move):
                move_box_func(new_pos, move)
            else:
                return pos

        self._warehouse_map[pos[0]][pos[1]] = "."
        self._warehouse_map[new_pos[0]][new_pos[1]] = "@"
        return new_pos

    def _is_large_box(self, pos: list) -> bool:
        """return bool if one side of large box"""
        return self._is_large_box_left(pos) or self._is_large_box_right(pos)

    def _is_large_box_left(self, pos: list) -> bool:
        """return bool if left side of large box"""
        return self._warehouse_map[pos[0]][pos[1]] == "["

    def _is_large_box_right(self, pos: list) -> bool:
        """return bool if right side of large box"""
        return self._warehouse_map[pos[0]][pos[1]] == "]"

    def _split_warehouse(self) -> None:
        """split warehouse sites"""
        warehouse_map_double = []
        for site_line in self._warehouse_map:
            warehouse_map_double.append([])
            for site in site_line:
                for new_site in _SPLIT_SITES[site]:
                    warehouse_map_double[-1].append(new_site)
        self._warehouse_map = warehouse_map_double
        self._nrows = len(self._warehouse_map)
        self._ncols = len(self._warehouse_map[0])

    def _get_left_right_box_pos(self, pos: list) -> tuple:
        """given alarg box position, return left and right positions"""
        if self._is_large_box_left(pos):
            pos_l = pos
            pos_r = _sum_list(pos, _MOVEMENTS[">"])
        else:
            # is a right side of a large box
            pos_r = pos
            pos_l = _sum_list(pos_r, _MOVEMENTS["<"])
        return pos_l, pos_r

    def _large_box_can_be_moved_horizontal(
        self, new_pos: list, move: list, large_left_right_func: Callable
    ) -> bool:
        """check if large box can be moved horizontally"""
        if self._is_empty(new_pos):
            return True
        if large_left_right_func(new_pos):
            next_box = _sum_list(new_pos, move)
            return self._large_box_can_be_moved(next_box, move)
        return None

    def _large_box_can_be_moved_vertical(self, new_pos: list, move: list) -> bool:
        """check if large box can be moved vertically"""
        if self._is_empty(new_pos):
            return True
        if self._is_large_box(new_pos):
            return self._large_box_can_be_moved(new_pos, move)
        return False

    def _large_box_can_be_moved(self, pos: list, move: list) -> bool:
        """check if large box can be moved"""
        pos_l, pos_r = self._get_left_right_box_pos(pos)
        new_pos_l = _sum_list(pos_l, move)
        new_pos_r = _sum_list(pos_r, move)

        if move in [_MOVEMENTS["<"], _MOVEMENTS[">"]]:
            _new_pos_move = {-1: new_pos_l, 1: new_pos_r}
            _new_pos_func = {-1: self._is_large_box_right, 1: self._is_large_box_left}
            can_be_moved = self._large_box_can_be_moved_horizontal(
                _new_pos_move[move[1]], move, _new_pos_func[move[1]]
            )
            if can_be_moved is not None:
                return can_be_moved

        elif move in [_MOVEMENTS["^"], _MOVEMENTS["v"]]:
            return self._large_box_can_be_moved_vertical(
                new_pos_l, move
            ) and self._large_box_can_be_moved_vertical(new_pos_r, move)

        return False

    def _move_large_box_horizontal(self, new_pos: list, move: list) -> bool:
        """move large box horizontally"""
        if self._is_empty(new_pos):
            return True
        if self._is_large_box(new_pos) and self._large_box_can_be_moved(new_pos, move):
            self._move_large_box(new_pos, move)
            return True
        return False

    def _move_large_box_vertical(
        self, new_pos_l: list, new_pos_r: list, move: list
    ) -> bool:
        """move large box vertically"""
        move_this_box = False

        if self._is_empty(new_pos_l) and self._is_empty(new_pos_r):
            move_this_box = True

        # one empty, one box side
        new_pos_move = [[new_pos_l, new_pos_r], [new_pos_r, new_pos_l]]
        for new_pos_a, new_pos_b in new_pos_move:
            if (
                self._is_empty(new_pos_a)
                and self._is_large_box(new_pos_b)
                and self._large_box_can_be_moved(new_pos_b, move)
            ):
                self._move_large_box(new_pos_b, move)
                move_this_box = True

        if self._is_large_box(new_pos_l) and self._is_large_box(new_pos_r):
            if self._large_box_can_be_moved(
                new_pos_l, move
            ) and self._large_box_can_be_moved(new_pos_r, move):
                if self._is_large_box_left(new_pos_l) and self._is_large_box_right(
                    new_pos_r
                ):
                    # l and r sides belong to the same box
                    self._move_large_box(new_pos_l, move)
                else:
                    # l and r sides belong to different boxes
                    self._move_large_box(new_pos_l, move)
                    self._move_large_box(new_pos_r, move)
                move_this_box = True
        return move_this_box

    def _move_large_box(self, pos: list, move: list) -> None:
        """move large box"""
        pos_l, pos_r = self._get_left_right_box_pos(pos)
        new_pos_l = _sum_list(pos_l, move)
        new_pos_r = _sum_list(pos_r, move)

        # check if the box can be moved
        move_this_box = False
        if move in [_MOVEMENTS["<"], _MOVEMENTS[">"]]:
            _new_pos_move = {-1: new_pos_l, 1: new_pos_r}
            move_this_box = self._move_large_box_horizontal(
                _new_pos_move[move[1]], move
            )

        elif move in [_MOVEMENTS["^"], _MOVEMENTS["v"]]:
            move_this_box = self._move_large_box_vertical(new_pos_l, new_pos_r, move)

        if move_this_box:
            if move in [_MOVEMENTS["<"], _MOVEMENTS[">"]]:
                _new_pos_move = {-1: new_pos_r, 1: new_pos_l}
                self._warehouse_map[_new_pos_move[move[1]][0]][
                    _new_pos_move[move[1]][1]
                ] = "."

            elif move in [_MOVEMENTS["^"], _MOVEMENTS["v"]]:
                self._warehouse_map[pos_l[0]][pos_l[1]] = "."
                self._warehouse_map[pos_r[0]][pos_r[1]] = "."
            self._warehouse_map[new_pos_l[0]][new_pos_l[1]] = "["
            self._warehouse_map[new_pos_r[0]][new_pos_r[1]] = "]"

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        data_index = self.data.index("")
        self._warehouse_map = [list(line) for line in self.data[:data_index]]
        self._split_warehouse()
        robot_pos = self._find_robot()

        for move_line in self._moves:
            for move in move_line:
                new_robot_pos = self._move_robot(
                    robot_pos,
                    _MOVEMENTS[move],
                    self._is_large_box,
                    self._large_box_can_be_moved,
                    self._move_large_box,
                )
                # new_robot_pos = self._move_robot_large(robot_pos,_MOVEMENTS[move])
                robot_pos = new_robot_pos

        return sum(
            100 * y + x
            for y in range(self._nrows)
            for x in range(self._ncols)
            if self._is_large_box_left([y, x])
        )
