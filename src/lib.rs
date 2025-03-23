use std::{cell::RefCell, collections::HashMap, iter::Sum};

use itertools::Itertools as _;

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
    compute_distance: impl Fn((Destination, Destination)) -> Distance,
) -> Option<Vec<Destination>>
where
    Destinations: Iterator<Item = Destination> + ExactSizeIterator,
    Destination: Clone,
    Distance: Ord + Sum<Distance> + Clone,
{
    // Get all permutations of the inner destinations
    let destinations_count = inner_destinations.len();
    let permutations = inner_destinations.permutations(destinations_count);

    // Create a route for each permutation that includes the start and end destinations
    let routes = permutations.map(|permutation| {
        std::iter::once(start.clone())
            .chain(permutation.into_iter())
            .chain(std::iter::once(end.clone()))
    });
    // Calculate the distance for each route
    let distances = routes.map(|route| {
        (
            route
                .clone()
                .tuple_windows()
                .map(|pair| compute_distance(pair))
                .sum::<Distance>(),
            route,
        )
    });

    // Find the route with the shortest distance
    let min = distances.min_by_key(|(distance, _)| distance.clone());

    // Return the route with the shortest distance
    min.map(|(_, route)| route.collect())
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

#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn test_traveling_salesman() {
        let destinations = vec![1, 2, 3, 4, 5];
        let start = 0;
        let end = 6;

        // Works with references
        let compute_distance = |pair: (&i32, &i32)| pair.0.abs_diff(*pair.1);
        let compute_distance = cached_fn(compute_distance);

        let result = traveling_salesman(destinations.iter(), &start, &end, compute_distance);
        assert_eq!(result, Some(vec![&0, &1, &2, &3, &4, &5, &6]));

        // Works with owned values
        let compute_distance = |pair: (i32, i32)| pair.0.abs_diff(pair.1);
        let compute_distance = cached_fn(compute_distance);

        let result = traveling_salesman(destinations.into_iter(), start, end, compute_distance);
        assert_eq!(result, Some(vec![0, 1, 2, 3, 4, 5, 6]));
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
}
