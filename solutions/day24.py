"""
Advent of Code 2024 - Day 24
"""

from utils import Puzzle


class PuzzleSolution(Puzzle):
    """Puzzle day 24"""

    def __init__(self):
        super().__init__()
        space_pos = self.data.index("")
        self.input_wires = self.data[:space_pos]
        self.gate_connections = self.data[space_pos + 1 :]
        self.gates = {}
        self.wires = {}

    def _compute_output(self, output: str) -> tuple:
        """fill missing output"""
        if self.wires[output] is not None:
            return self.wires[output]
        input_a, gate, input_b = self.gates[output]

        for input_i in [input_a, input_b]:
            if self.wires[input_i] is None:
                self.wires[input_i] = self._compute_output(input_i)
        if gate == "AND":
            self.wires[output] = (
                1 if self.wires[input_a] + self.wires[input_b] == 2 else 0
            )
        elif gate == "OR":
            self.wires[output] = (
                1 if self.wires[input_a] + self.wires[input_b] > 0 else 0
            )
        elif gate == "XOR":
            self.wires[output] = 1 if self.wires[input_a] != self.wires[input_b] else 0
        return self.wires[output]

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        self.gates = {}
        self.wires = {}
        for line in self.gate_connections:
            input_a, gate, input_b, _, output = line.split()
            self.gates[output] = [input_a, gate, input_b]

        for line in self.gate_connections:
            input_a, gate, input_b, _, output = line.split()
            for input_i in [input_a, input_b, output]:
                self.wires[input_i] = None

        for line in self.input_wires:
            wire, value = line.split(": ")
            self.wires[wire] = int(value)

        for line in self.gate_connections:
            _, _, _, _, output = line.split()
            if self.wires[output] is None:
                self.wires[output] = self._compute_output(output)

        z_wires = sorted(
            [val for val in self.wires.items() if val[0][0].startswith("z")],
            key=lambda x: x[0],
            reverse=True,
        )
        return int("".join(map(str, [v for _, v in z_wires])), 2)

    def _update_gate_connections(self) -> None:
        """update gate connections"""
        self.gate_connections = []
        for output, (input_a, gate, input_b) in self.gates.items():
            self.gate_connections.append(f"{input_a} {gate} {input_b} -> {output}")

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        x_bin = "".join(
            [line.split(": ")[1] for line in self.input_wires if line.startswith("x")]
        )[::-1]
        y_bin = "".join(
            [line.split(": ")[1] for line in self.input_wires if line.startswith("y")]
        )[::-1]
        _z = int(x_bin, 2) + int(y_bin, 2)
        z_bin = bin(_z)[2:][::-1]

        swap_key = []
        result = []

        while True:
            self._update_gate_connections()
            z_test = bin(self.solve_part1())[2:][::-1]
            if z_bin == z_test:
                break
            for _i, z_value in enumerate(z_bin):
                if z_value != z_test[_i] or len(swap_key) == 1:
                    z_key = f"z{_i:02}"
                    input_1, gate, input_2 = self.gates[z_key]
                    for input_a, input_b in [(input_1, input_2), (input_2, input_1)]:
                        if len(swap_key) == 2:
                            break
                        if gate == "XOR":
                            # a XOR b
                            if input_a[0] in ("x", "y") and input_b[0] in ("x", "y"):
                                continue

                            input_a_l1, gate1_l1, input_b_l1 = self.gates[input_a]
                            input_a_r1, gate1_r1, input_b_r1 = self.gates[input_b]

                            if gate1_l1 == "XOR" and input_a_l1[0] in ("x", "y"):
                                # (a1 XOR a2) XOR b, a1,a2 are x/y
                                if gate1_r1 != "OR":
                                    if input_b not in swap_key:
                                        swap_key.append(input_b)
                                else:
                                    # ((a1 XOR a2) XOR ((b11 AND b12) OR (b21 AND b22)))
                                    _, gate1_r1_l2, _ = self.gates[input_a_r1]
                                    if (
                                        gate1_r1_l2 != "AND"
                                        and input_a_r1 not in swap_key
                                    ):
                                        swap_key.append(input_a_r1)
                                    _, gate1_r1_r2, _ = self.gates[input_b_r1]
                                    if (
                                        gate1_r1_r2 != "AND"
                                        and input_b_r1 not in swap_key
                                    ):
                                        swap_key.append(input_b_r1)
                            else:
                                if gate1_l1 != "OR" and input_a not in swap_key:
                                    swap_key.append(input_a)
                                else:
                                    _, gate1_l1_l2, _ = self.gates[input_a_l1]
                                    if (
                                        gate1_l1_l2 != "AND"
                                        and input_a_l1 not in swap_key
                                    ):
                                        swap_key.append(input_a_l1)
                                    _, gate1_l1_r2, _ = self.gates[input_b_l1]
                                    if (
                                        gate1_l1_r2 != "AND"
                                        and input_b_l1 not in swap_key
                                    ):
                                        swap_key.append(input_b_l1)
                        else:
                            if z_key not in swap_key:
                                swap_key.append(z_key)

                        if len(swap_key) == 2:
                            break

            self.gates[swap_key[0]], self.gates[swap_key[1]] = (
                self.gates[swap_key[1]],
                self.gates[swap_key[0]],
            )
            result += swap_key
            swap_key = []

        return ",".join(sorted(result))
