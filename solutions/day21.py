"""
Advent of Code 2024 - Day 21
"""

from utils import Puzzle

KEY_PAD_NUM = ["789", "456", "123", " 0A"]
KEY_PAD_ARR = [" ^A", "<v>"]


def _key_pad_pos(key_pad: list[str]) -> dict:
    """compute dictionary wiith keypad positions"""
    _key_dic = {}
    for _l, _line in enumerate(key_pad):
        for _s, _site in enumerate(_line):
            _key_dic[_site] = (_l, _s)
    return _key_dic


class PuzzleSolution(Puzzle):
    """Puzzle day 21"""

    def __init__(self):
        super().__init__()
        self._moves_num = self._parse_keypad_codes(KEY_PAD_NUM)
        self._moves_arr = self._parse_keypad_codes(KEY_PAD_ARR)
        self._code_translation_cache = {}

    def _keypad_codes(
        self, x: tuple[int, int], y: tuple[int, int], forbidden_pos: tuple[int, int]
    ) -> list:
        """compute code connecting from x to y"""
        _codes = []
        if x[0] == y[0]:
            _dir = ">" if y[1] > x[1] else "<"
            _codes.append(_dir * (abs(y[1] - x[1])) + "A")
        elif x[1] == y[1]:
            _dir = "v" if y[0] > x[0] else "^"
            _codes.append(_dir * (abs(y[0] - x[0])) + "A")
        else:
            if x[0] != forbidden_pos[0] or y[1] != forbidden_pos[1]:
                _dir_hor = ">" if y[1] > x[1] else "<"
                _dir_ver = "v" if y[0] > x[0] else "^"
                _codes.append(
                    _dir_hor * (abs(y[1] - x[1])) + _dir_ver * (abs(y[0] - x[0])) + "A"
                )
            if x[1] != forbidden_pos[1] or y[0] != forbidden_pos[0]:
                _dir_hor = "v" if y[0] > x[0] else "^"
                _dir_ver = ">" if y[1] > x[1] else "<"
                _codes.append(
                    _dir_hor * (abs(y[0] - x[0])) + _dir_ver * (abs(y[1] - x[1])) + "A"
                )
        return _codes

    def _parse_keypad_codes(self, key_pad: list) -> dict:
        """parse keypad code"""
        _key_pos = _key_pad_pos(key_pad)
        _pad_keys = sorted(_key_pos.keys())
        _codes = {}
        for _key_in in _pad_keys:
            for _key_fin in _pad_keys:
                if _key_in == " " or _key_fin == " " or _key_in == _key_fin:
                    continue
                _pos_in = _key_pos[_key_in]
                _pos_fin = _key_pos[_key_fin]
                _codes[(_key_in, _key_fin)] = self._keypad_codes(
                    _pos_in, _pos_fin, _key_pos[" "]
                )
        return _codes

    # @cache
    def _translate_code(self, code: str, robots: int) -> int:
        """translate recursivelly codes"""
        if (code, robots) in self._code_translation_cache:
            return self._code_translation_cache[(code, robots)]
        if code[0].isnumeric():
            _translated_code = self._translate_num_pad(code)
        else:
            _translated_code = self._translate_arrow_pad(code)
        if robots == 0:
            _min_len_code = min(
                sum(len(sub_code) for sub_code in code) for code in _translated_code
            )
        else:
            _min_len_code = min(
                sum(self._translate_code(sub_code, robots - 1) for sub_code in code)
                for code in _translated_code
            )
        self._code_translation_cache[(code, robots)] = _min_len_code
        return _min_len_code

    def _translate_arrow_pad(self, code: str) -> list:
        """translate arrow keypad code"""
        code = "A" + code
        moves = [
            self._moves_arr[(a, b)] if a != b else ["A"] for a, b in zip(code, code[1:])
        ]
        moves = self._build_combinations(moves)
        return moves

    def _translate_num_pad(self, code: str) -> list:
        """translate numeric keypad code"""
        code = "A" + code
        moves = [self._moves_num[(a, b)] for a, b in zip(code, code[1:])]
        moves = self._build_combinations(moves)
        return moves

    def _build_combinations(self, code_arrays, current=None, index=0):
        """build code combinations"""
        if current is None:
            current = []
        if index == len(code_arrays):
            return [current]
        _code_combination = []
        for value in code_arrays[index]:
            new_code = self._build_combinations(
                code_arrays, current + [value], index + 1
            )
            _code_combination.extend(new_code)
        return _code_combination

    def _compute_complexity(self, robots: int) -> int:
        """compute complexy generic number of robots"""
        _complexity = 0
        for code in self.data:
            _min_code_len = self._translate_code(code, robots)
            _complexity += _min_code_len * int(code[:-1])
        return _complexity

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        return self._compute_complexity(2)

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        return self._compute_complexity(25)
