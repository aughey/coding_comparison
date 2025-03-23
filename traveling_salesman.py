import itertools
from typing import Generator, TypeVar, Callable, List, Optional, Any, Iterable, Tuple
from functools import lru_cache
import unittest
import heapq

T = TypeVar('T')
Distance = TypeVar('Distance')
GeneratorT = Generator[T, None, None]


def start_list_end(start: T, inner: Iterable[T], end: T) -> GeneratorT:
    yield start
    for item in inner:
        yield item
    yield end


def all_routes(start: T, inner_destinations: Iterable[Iterable[T]], end: T) -> Generator[GeneratorT, None, None]:
    for inner in inner_destinations:
        yield start_list_end(start, inner, end)


def total_distance(route: Iterable[T], compute_distance: Callable[[tuple[T, T]], Distance]) -> Distance:
    pairs = pairwise(route)
    return sum(compute_distance(pair) for pair in pairs)


def pairwise(iterable: Iterable[T]):
    """
    Create an iterator of paired items, s -> (s0,s1), (s1,s2), (s2, s3), ...
    Using the itertools.tee to avoid materializing the iterable.
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def route_with_distance(route_gen: GeneratorT, compute_distance: Callable[[tuple[T, T]], Distance]) -> tuple[Distance, List[T]]:
    """
    Compute the total distance of a route and return both the distance and the materialized route.
    This allows us to compute the distance in a streaming manner while preserving the route.
    """
    # We need to collect the route items for two purposes:
    # 1. To calculate the distance between consecutive points
    # 2. To return the complete route

    # First materialize the route since we need it twice
    # This is necessary because we can't reset a generator
    route = list(route_gen)

    # Compute distance using pairs of consecutive items
    pairs = pairwise(route)
    distance = sum(compute_distance(pair) for pair in pairs)

    return distance, route


def traveling_salesman(
    inner_destinations: List[T],
    start: T,
    end: T,
    compute_distance: Callable[[tuple[T, T]], Distance]
) -> List[T]:
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
    # Use the generator-based implementation and convert result to list
    return list(lazy_traveling_salesman(inner_destinations, start, end, compute_distance))


def hand_rolled_traveling_salesman(
    inner_destinations: List[T],
    start: T,
    end: T,
    compute_distance: Callable[[tuple[T, T]], Distance]
) -> Optional[List[T]]:
    """
    A hand-rolled version of the traveling salesman function that uses a more manual approach
    to find the shortest path.

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

    min_distance = None
    min_route = None
    for permutation in all_permutations:
        dist = 0
        it = iter(permutation)
        prev = next(it)
        for curr in it:
            dist += compute_distance((prev, curr))
            prev = curr
        # Add distance from start to first destination and last destination to end
        dist += compute_distance((start, permutation[0]))
        dist += compute_distance((permutation[-1], end))
        if min_distance is None or dist < min_distance:
            min_distance = dist
            min_route = [start] + list(permutation) + [end]

    return min_route


def cached_fn(func: Callable) -> Callable:
    """
    Caches the results of any function call using Python's built-in lru_cache.
    """
    return lru_cache(maxsize=None)(func)


def lazy_traveling_salesman(
    inner_destinations: Iterable[T],
    start: T,
    end: T,
    compute_distance: Callable[[tuple[T, T]], Distance]
) -> Generator[T, None, None]:
    """
    A fully generator-based implementation of the traveling salesman problem.

    This function computes the shortest path through all destinations but uses
    lazy evaluation as much as possible. The returned path is a generator.

    Args:
        inner_destinations: The destinations to visit.
        start: The starting destination.
        end: The ending destination.
        compute_distance: A function that computes the distance between two destinations.

    Returns:
        A generator yielding the nodes of the shortest path.
    """
    # Convert to list only if needed for getting the count
    if not isinstance(inner_destinations, (list, tuple)):
        inner_destinations = list(inner_destinations)

    destinations_count = len(inner_destinations)

    if destinations_count == 0:
        yield start
        yield end
        return

    min_distance = float('inf')
    min_permutation = None

    # Generate permutations lazily
    for permutation in itertools.permutations(inner_destinations, destinations_count):
        total_dist = compute_distance((start, permutation[0]))

        # Calculate distances between consecutive destinations
        for i in range(destinations_count - 1):
            total_dist += compute_distance(
                (permutation[i], permutation[i + 1]))
            # Early stopping - if we already exceed min_distance, no need to continue
            if total_dist >= min_distance:
                break

        # If we didn't break early, add the final leg
        else:
            total_dist += compute_distance((permutation[-1], end))

            if total_dist < min_distance:
                min_distance = total_dist
                min_permutation = permutation

    # Yield the best route
    if min_permutation is not None:
        yield start
        yield from min_permutation
        yield end


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

    def test_hand_rolled_traveling_salesman(self):
        # Test with hand-rolled version
        # random destinations of 5 values
        destinations = [10, 23, 13, 94, 35]
        start = 0
        end = 6

        def compute_distance(pair: tuple[int, int]) -> int:
            return abs(pair[0] - pair[1])

        hand_result = hand_rolled_traveling_salesman(
            destinations, start, end, compute_distance)
        other_result = traveling_salesman(
            destinations, start, end, compute_distance)
        self.assertEqual(list(hand_result), list(
            other_result), "Hand-rolled version should match the main function result.")


class TestLazyTravelingSalesman(unittest.TestCase):
    def test_lazy_traveling_salesman(self):
        # Test with references (integers)
        destinations = [1, 2, 3, 4, 5]
        start = 0
        end = 6

        @cached_fn
        def compute_distance_ref(pair: tuple[int, int]) -> int:
            return abs(pair[0] - pair[1])

        result = list(lazy_traveling_salesman(
            destinations, start, end, compute_distance_ref))
        self.assertEqual(result, [0, 1, 2, 3, 4, 5, 6])

    def test_lazy_empty_destinations(self):
        """Test that the lazy function handles empty destinations correctly"""
        destinations = []
        start = 0
        end = 1

        @cached_fn
        def compute_distance(pair: tuple[int, int]) -> int:
            return abs(pair[0] - pair[1])

        result = list(lazy_traveling_salesman(
            destinations, start, end, compute_distance))
        self.assertEqual(result, [0, 1])

    def test_lazy_single_destination(self):
        """Test that the lazy function works correctly with a single destination"""
        destinations = [1]
        start = 0
        end = 2

        @cached_fn
        def compute_distance(pair: tuple[int, int]) -> int:
            return abs(pair[0] - pair[1])

        result = list(lazy_traveling_salesman(
            destinations, start, end, compute_distance))
        self.assertEqual(result, [0, 1, 2])

    def test_compare_implementations(self):
        """Test that the lazy and original implementations produce the same result"""
        # Test with a non-trivial set of destinations
        destinations = [10, 23, 13, 94, 35]
        start = 0
        end = 6

        @cached_fn
        def compute_distance(pair: tuple[int, int]) -> int:
            return abs(pair[0] - pair[1])

        # Save original implementation
        original_result = hand_rolled_traveling_salesman(
            destinations, start, end, compute_distance)

        # Get lazy implementation result
        lazy_result = list(lazy_traveling_salesman(
            destinations, start, end, compute_distance))

        # Both should produce the same optimal path
        self.assertEqual(lazy_result, original_result,
                         "Lazy implementation should match the hand-rolled implementation result.")


if __name__ == '__main__':
    unittest.main()
