"""
Advent of Code 2024 - Day 5
"""

from utils import Puzzle


class PuzzleSolution(Puzzle):
    """Puzzle day 5"""

    def __init__(self):
        super().__init__()
        _file_separator = self.data.index("")
        self.rules = {}
        for line in self.data[:_file_separator]:
            a,b = map(int, line.split("|"))
            if a not in self.rules.keys():
                self.rules[a] = [b]
            else:
                self.rules[a].append(b)

        self.updates = [list(map(int, line.split(","))) for line in self.data[_file_separator+1:]]

    def _update_validation(self, update: list) -> bool:
        for i in range(len(update)):
            for j in range(i+1, len(update)):
                if update[j] not in self.rules[update[i]]:
                    return False
        return True

    def _sort_update(self, update: list) -> list:
        filtered_rules = {}
        for i in update:
            for subrule in self.rules[i]:
                if subrule in update:
                    if i in filtered_rules.keys():
                        filtered_rules[i].append(subrule)
                    else:
                        filtered_rules[i] = [subrule]

        sorted_update = sorted(filtered_rules, key=lambda k: len(filtered_rules[k]), reverse=True)
        return sorted_update

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        return sum(update[len(update) // 2] for update in self.updates if self._update_validation(update))
        

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        sumsorted = 0
        for update in self.updates:
            if self._update_validation(update) is False:
                sorted_update = self._sort_update(update)
                if self._update_validation(sorted_update) is True:
                    sumsorted += sorted_update[len(sorted_update) // 2]
        return sumsorted
