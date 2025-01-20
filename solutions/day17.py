"""
Advent of Code 2024 - Day 17
"""

from utils import Puzzle


class PuzzleSolution(Puzzle):
    """Puzzle day 17"""

    def __init__(self):
        super().__init__()

        self._output = []

        self.data = [line.split(" ") for line in self.data]

        self._a_value = 0
        self._b_value = 0
        self._c_value = 0
        self._program = list(map(int, self.data[4][1].split(",")))

    def _combo_operand(self, value: int) -> None:
        """combo operand"""
        if 0 <= value <= 3:
            return value
        if value == 4:
            return self._a_value
        if value == 5:
            return self._b_value
        if value == 6:
            return self._c_value
        raise ValueError("Invalid value, {value} >= 7")

    def _exec_instructions(self, initial_register_values: list[int]) -> None:
        """execute instructions program"""
        self._a_value, self._b_value, self._c_value = initial_register_values

        pointer = 0

        while pointer < len(self._program):
            opcode = self._program[pointer]
            operand = self._program[pointer + 1]
            if opcode == 0:
                # adv
                self._a_value //= 2 ** self._combo_operand(operand)
            elif opcode == 1:
                # bxl
                self._b_value ^= operand
            elif opcode == 2:
                # bst
                self._b_value = self._combo_operand(operand) % 8
            elif opcode == 3:
                # jnz
                if self._a_value != 0:
                    pointer = operand
                    continue  # jump the pointer increment
            elif opcode == 4:
                # bxc
                self._b_value ^= self._c_value
            elif opcode == 5:
                # out
                self._output.append(self._combo_operand(operand) % 8)
            elif opcode == 6:
                # bdv
                self._b_value = self._a_value // (2 ** self._combo_operand(operand))
            elif opcode == 7:
                # cdv
                self._c_value = self._a_value // (2 ** self._combo_operand(operand))

            pointer += 2

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        initial_register = [
            int(self.data[0][2]),
            int(self.data[1][2]),
            int(self.data[2][2]),
        ]

        self._exec_instructions(initial_register)
        return ",".join(map(str, self._output))

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        initial_register = [
            int(self.data[0][2]),
            int(self.data[1][2]),
            int(self.data[2][2]),
        ]

        a_value = 1
        while True:
            self._output = []
            initial_register[0] = a_value
            self._exec_instructions(initial_register)

            if self._output == self._program:
                return a_value

            # increase a until it get the righ len of output
            if len(self._output) < len(self._program):
                a_value = 10 ** (len(str(a_value)) + 1)
            else:
                # small a value affects first part of output, larger the last part
                for i in range(len(self._output) - 1, -1, -1):
                    if self._output[i] != self._program[i]:
                        a_value += 4 ** i
                        break

            if len(self._output) > len(self._program):
                raise ValueError("Missed, too long output")
