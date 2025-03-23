use std::{cell::RefCell, collections::HashMap, iter::Sum, ops::Add};

use itertools::Itertools as _;

/// Calculates the total distance of a route by summing the distances between consecutive destinations.
///
/// # Arguments
///
/// * `route` - An iterator over destinations
/// * `compute_distance` - A function that computes the distance between two destinations
///
/// # Returns
///
/// The total distance of the route
fn total_distance_of_route<'a, Destination, Distance>(
    route: impl Iterator<Item = &'a Destination>,
    compute_distance: impl Fn((&Destination, &Destination)) -> Distance,
) -> Distance
where
    Destination: 'a,
    Distance: Sum,
{
    route.tuples().map(compute_distance).sum()
}

/// For all of the inner destinations, find the shortest path that visits all of them starting
/// at `start` and ending at `end`.
///
/// inner_destinations: The destinations to visit.
/// start: The starting destination.
/// end: The ending destination.
/// compute_distance: A function that computes the distance between two destinations.
///
/// Returns the shortest path that visits all of the inner destinations starting at `start` and ending at `end`.
pub fn traveling_salesman<Destinations, Destination, Distance>(
    inner_destinations: Destinations,
    start: Destination,
    end: Destination,
    compute_distance: impl Fn((&Destination, &Destination)) -> Distance,
) -> Vec<Destination>
where
    Destinations: Iterator<Item = Destination> + ExactSizeIterator,
    Destination: Clone,
    Distance: Ord + Sum<Distance> + Add<Distance, Output = Distance>,
{
    // Get all permutations of the inner destinations
    let permutations = {
        let count = inner_destinations.len();
        inner_destinations
            .permutations(count)
            .filter(|r| !r.is_empty())
    };

    // Calculate the distance for each route
    // distance is a Iterator of tuples of (distance, route)
    let distances = permutations.map(|route| {
        let inner_distance = total_distance_of_route(route.iter(), &compute_distance);

        // Add the distance from the start to the first destination and from the last destination to the end
        // Safety: route.len() >= 1
        let total_distance = inner_distance
            + compute_distance((&start, &route[0]))
            + compute_distance((&route[route.len() - 1], &end));

        (total_distance, route)
    });

    // Find the route with the shortest distance
    let min_route = distances
        .min_by(|a, b| a.0.cmp(&b.0))
        .map(|(_, route)| route);

    let mut route = vec![start];
    if let Some(min_route) = min_route {
        route.extend(min_route);
    }
    route.push(end);
    route
}

/// Caches the results of any function call.
pub fn cached_fn<Input, Output>(f: impl Fn(Input) -> Output) -> impl Fn(Input) -> Output
where
    Input: std::hash::Hash + std::cmp::Eq + Clone,
    Output: Clone,
{
    let cache = HashMap::<Input, Output>::new();
    let cache = RefCell::new(cache);

    move |input| {
        let mut cache = cache.borrow_mut();

        if let Some(result) = cache.get(&input) {
            result.clone()
        } else {
            let result = f(input.clone());
            cache.insert(input, result.clone());
            result
        }
    }
}

/// A hand-optimized version of the traveling salesman algorithm for i32 destinations.
///
/// This implementation is specific to i32 types and uses a different approach
/// than the generic version for potential (negligible) performance benefits.
///
/// # Arguments
///
/// * `destination` - Slice of destinations to visit
/// * `start` - The starting point
/// * `end` - The ending point
///
/// # Returns
///
/// The shortest path that visits all destinations
pub fn hand_rolled_traveling_salesman<'a>(
    destination: &'a [i32],
    start: &'a i32,
    end: &'a i32,
) -> Vec<&'a i32> {
    let mut min_distance = None;
    let mut min_route = None;

    for perm in destination
        .iter()
        .permutations(destination.len())
        .filter(|p| !p.is_empty())
    {
        // Hand-calculate the distance of the pairs
        let mut distance = 0;
        for i in 1..perm.len() {
            // Safety: i >= 1 and i < perm.len()
            distance += perm[i - 1].abs_diff(*perm[i]);
        }

        // Safety: Safe because perm.len() >= 1
        // add from start to the first
        distance += start.abs_diff(*perm[0]);
        // add from end to the last
        distance += end.abs_diff(*perm[perm.len() - 1]);

        if let Some(min_distance) = min_distance {
            if distance >= min_distance {
                continue; // skip if this route is longer than the current minimum
            }
        }
        min_distance = Some(distance);
        min_route = Some(perm);
    }

    // prepend start and append end
    let mut route = vec![start];
    if let Some(min_route) = min_route {
        route.extend(min_route);
    }
    route.push(end);

    route
}

#[cfg(test)]
mod tests {

    use std::collections::HashSet;

    use super::*;

    #[test]
    fn test_traveling_salesman() {
        let destinations = vec![1, 2, 3, 4, 5];
        let start = 0;
        let end = 6;

        // Works with references
        let compute_distance = |pair: (&&i32, &&i32)| pair.0.abs_diff(**pair.1);

        let result = traveling_salesman(destinations.iter(), &start, &end, compute_distance);
        assert_eq!(result, vec![&0, &1, &2, &3, &4, &5, &6]);
        // Works with owned values
        let compute_distance = |pair: (&i32, &i32)| pair.0.abs_diff(*pair.1);

        let result = traveling_salesman(destinations.into_iter(), start, end, compute_distance);
        assert_eq!(result, vec![0, 1, 2, 3, 4, 5, 6]);
    }

    /// Test to ensure that the hand-rolled version of the traveling salesman
    /// algorithm matches the generic version for a set of random destinations.
    #[test]
    fn test_random_destinations_match_all() {
        for _ in 0..10 {
            let destinations =
                HashSet::<i32>::from_iter((1..=5).map(|_| rand::random::<i32>() % 100));

            let start = destinations.clone().into_iter().min().unwrap_or(0);
            let end = destinations.clone().into_iter().max().unwrap_or(1);

            let dv = destinations.clone().into_iter().collect::<Vec<_>>();
            let result = hand_rolled_traveling_salesman(&dv, &start, &end);

            let other_result = traveling_salesman(destinations.iter(), &start, &end, |pair| {
                pair.0.abs_diff(**pair.1)
            });
            assert_eq!(result, other_result);
        }
    }

    #[test]
    fn test_traveling_salesman_empty_destinations() {
        let destinations: Vec<i32> = vec![];
        let start = 0;
        let end = 1;

        let compute_distance = |pair: (&i32, &i32)| pair.0.abs_diff(*pair.1);

        let result = traveling_salesman(destinations.into_iter(), start, end, compute_distance);
        assert_eq!(result, vec![0, 1]);
    }

    #[test]
    fn test_cached_fn() {
        let call_count = std::cell::Cell::new(0);
        let f = |x: i32| {
            call_count.set(call_count.get() + 1);
            x * 2
        };
        let cached_f = cached_fn(f);

        assert_eq!(cached_f(5), 10);
        assert_eq!(cached_f(5), 10); // Second call uses cache
        assert_eq!(call_count.get(), 1); // Verify f was only called once
    }

    #[test]
    fn test_hand_rolled_traveling_salesman() {
        let destinations = vec![1, 2, 3, 4, 5];
        let start = 0;
        let end = 6;

        let result = hand_rolled_traveling_salesman(&destinations, &start, &end);
        assert_eq!(result, vec![&0, &1, &2, &3, &4, &5, &6]);
    }
}
