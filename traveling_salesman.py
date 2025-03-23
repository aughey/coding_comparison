import itertools
from typing import TypeVar, Callable, List, Optional, Any, Iterable
from functools import lru_cache
import unittest

T = TypeVar('T')
Distance = TypeVar('Distance')


def start_list_end(start: T, inner: Iterable[T], end: T) -> Iterable[T]:
    yield start
    for item in inner:
        yield item
    yield end


def all_routes(start: T, inner_destinations: Iterable[Iterable[T]], end: T) -> Iterable[Iterable[T]]:
    for inner in inner_destinations:
        yield start_list_end(start, inner, end)


def total_distance(route: Iterable[T], compute_distance: Callable[[tuple[T, T]], Distance]) -> Distance:
    pairs = pairwise(route)
    return sum(compute_distance(pair) for pair in pairs)

def pairwise(iterable: Iterable[T]) -> Iterable[tuple[T, T]]:
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def traveling_salesman(
    inner_destinations: List[T],
    start: T,
    end: T,
    compute_distance: Callable[[tuple[T, T]], Distance]
) -> Optional[List[T]]:
    """
    For all of the inner destinations, find the shortest path that visits all of them starting
    at `start` and ending at `end`.

    Args:
        inner_destinations: The destinations to visit.
        start: The starting destination.
        end: The ending destination.
        compute_distance: A function that computes the distance between two destinations.

    Returns:
        The shortest path that visits all of the inner destinations starting at `start` and ending at `end`.
    """
    # Get all permutations of the inner destinations
    destinations_count = len(inner_destinations)
    all_permutations = itertools.permutations(
        inner_destinations, destinations_count)

    # Create a route for each permutation that includes the start and end destinations
    routes = all_routes(start, all_permutations, end)

    route_distances = []
    for route in routes:
        # unfortunately we need to listify the route to avoid iterator exhaustion
        route = list(route)
        distance = total_distance(iter(route), compute_distance)
        route_distances.append((distance, route))

    min_route = min(route_distances, key=lambda x: x[0])
    return min_route[1]


def cached_fn(func: Callable) -> Callable:
    """
    Caches the results of any function call using Python's built-in lru_cache.
    """
    return lru_cache(maxsize=None)(func)


class TestTravelingSalesman(unittest.TestCase):
    def test_traveling_salesman(self):
        # Test with references (integers)
        destinations = [1, 2, 3, 4, 5]
        start = 0
        end = 6

        # Works with references
        @cached_fn
        def compute_distance_ref(pair: tuple[int, int]) -> int:
            return abs(pair[0] - pair[1])

        result = traveling_salesman(
            destinations, start, end, compute_distance_ref)
        self.assertEqual(list(result), [0, 1, 2, 3, 4, 5, 6])

        # Test with different distance function
        @cached_fn
        def compute_distance_squared(pair: tuple[int, int]) -> int:
            return (pair[0] - pair[1]) ** 2

        result = traveling_salesman(
            destinations, start, end, compute_distance_squared)
        self.assertEqual(list(result), [0, 1, 2, 3, 4, 5, 6])

    def test_cached_fn(self):
        call_count = 0

        def count_calls(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        cached_f = cached_fn(count_calls)

        self.assertEqual(cached_f(5), 10)
        self.assertEqual(cached_f(5), 10)  # Second call uses cache
        self.assertEqual(call_count, 1)  # Verify f was only called once

    def test_empty_destinations(self):
        """Test that the function handles empty destinations correctly"""
        destinations = []
        start = 0
        end = 1

        @cached_fn
        def compute_distance(pair: tuple[int, int]) -> int:
            return abs(pair[0] - pair[1])

        result = traveling_salesman(destinations, start, end, compute_distance)
        self.assertEqual(result, [0, 1])

    def test_single_destination(self):
        """Test that the function works correctly with a single destination"""
        destinations = [1]
        start = 0
        end = 2

        @cached_fn
        def compute_distance(pair: tuple[int, int]) -> int:
            return abs(pair[0] - pair[1])

        result = traveling_salesman(destinations, start, end, compute_distance)
        self.assertEqual(list(result), [0, 1, 2])


if __name__ == '__main__':
    unittest.main()
