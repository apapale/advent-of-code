"""
Advent of Code 2024 - Day 22
"""

from utils import Puzzle


def _compute_new_secret_number(secret_number: int) -> int:
    secret_number = ((secret_number * 64) ^ secret_number) % 16777216
    secret_number = ((secret_number // 32) ^ secret_number) % 16777216
    secret_number = ((secret_number * 2048) ^ secret_number) % 16777216
    return secret_number


def _generate_2000th_secret_number(secret_number: int) -> int:
    for _ in range(0, 2000):
        secret_number = _compute_new_secret_number(secret_number)
    return secret_number


def _price(secret_number: int) -> int:
    return secret_number % 10


class PuzzleSolution(Puzzle):
    """Puzzle day 22"""

    def solve_part1(self) -> int:
        """solve first part of the puzzle"""
        return sum(
            _generate_2000th_secret_number(secret_number)
            for secret_number in map(int, self.data)
        )

    def _compute_prices(self) -> list:
        """compute all prices"""
        _all_prices = []
        for secret_number in map(int, self.data):
            _prices = []
            for _ in range(0, 2000):
                secret_number = _compute_new_secret_number(secret_number)
                _prices.append(_price(secret_number))
            _all_prices.append(_prices)
        return _all_prices

    def solve_part2(self) -> int:
        """solve second part of the puzzle"""
        _all_prices = self._compute_prices()
        _changes = [
            [y - x for x, y in zip(prices, prices[1:])] for prices in _all_prices
        ]

        bananas = {}
        for buyer, change in enumerate(_changes):
            buyer_cache = {}
            for i in range(len(change) - 3):
                price_seq = tuple(change[i : i + 4])
                if price_seq in buyer_cache:
                    continue
                buyer_cache[price_seq] = _all_prices[buyer][i + 4]

                if price_seq in bananas:
                    bananas[price_seq] += _all_prices[buyer][i + 4]
                else:
                    bananas[price_seq] = _all_prices[buyer][i + 4]
        return bananas[max(bananas, key=bananas.get)]
