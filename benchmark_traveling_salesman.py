from traveling_salesman import traveling_salesman, hand_rolled_traveling_salesman
from typing import Tuple


def generate_stress_test_destinations():
    # Using 8 destinations will give us 8! = 40320 permutations
    # This matches the Rust benchmark
    return list(range(1, 9))


def test_traveling_salesman(benchmark):
    destinations = generate_stress_test_destinations()
    start = 0
    end = max(destinations) + 1

    def compute_distance(pair: Tuple[int, int]) -> int:
        return abs(pair[0] - pair[1])

    # Benchmark the reference version (in Python, everything is by reference)
    result = benchmark(
        lambda: traveling_salesman(
            destinations,
            start,
            end,
            compute_distance
        )
    )

    # Verify the result is correct (should be in ascending order for this case)
    assert list(result) == [0] + list(range(1, 9)) + [9]


def test_hand_rolled(benchmark):
    destinations = generate_stress_test_destinations()
    start = 0
    end = 9

    def compute_distance(pair: Tuple[int, int]) -> int:
        return abs(pair[0] - pair[1])

    # Benchmark the reference version (in Python, everything is by reference)
    result = benchmark(
        lambda: hand_rolled_traveling_salesman(
            destinations,
            start,
            end,
            compute_distance
        )
    )

    # Verify the result is correct (should be in ascending order for this case)
    assert list(result) == [0] + list(range(1, 9)) + [9]


if __name__ == "__main__":
    # This allows running with python -m pytest benchmark_traveling_salesman.py --benchmark-only
    import pytest
    pytest.main(['--benchmark-only', __file__])
