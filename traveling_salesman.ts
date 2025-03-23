import { time } from 'console';
import { single, reduce } from 'itertools-ts';
import { permutations } from 'itertools-ts/lib/combinatorics';

/**
 * Calculates the total distance of a route by summing the distances between consecutive points.
 * 
 * @template T - The type of elements in the route
 * @param {Iterable<T>} route - The route to calculate distance for
 * @param {(pair: [T, T]) => number} computeDistance - Function to compute distance between two points
 * @returns {number} The total distance of the route
 */
function total_distance<T>(route: Iterable<T>, computeDistance: (pair: [T, T]) => number): number {
    let distance = 0;
    for (const [a, b] of single.pairwise(route)) {
        distance += computeDistance([a, b]);
    }
    return distance;
}

/**
 * Calculates distances for multiple routes.
 * 
 * @template T - The type of elements in the routes
 * @param {Iterable<Iterable<T>>} routes - Collection of routes to calculate distances for
 * @param {(pair: [T, T]) => number} computeDistance - Function to compute distance between two points
 * @yields {[number, T[]]} Tuples containing the distance and route array for each route
 */
function* calculateDistances<T>(routes: Iterable<Iterable<T>>, computeDistance: (pair: [T, T]) => number): Generator<[number, T[]]> {
    for (const route of routes) {
        // we do unfold the route to an array so we can provide the route as a return value
        const routeArray = Array.from(route);
        const distance = total_distance(routeArray, computeDistance);

        yield [distance, routeArray];
    }
}

/**
 * Generates a route that starts with a specific point, includes inner points, and ends with another specific point.
 * 
 * @template T - The type of elements in the route
 * @param {T} start - The starting point
 * @param {T} end - The ending point
 * @param {Iterable<T>} inner - The inner points to include in the route
 * @yields {T} The complete route including start, inner points, and end
 */
function* startAndEnd<T>(start: T, end: T, inner: Iterable<T>) {
    yield start;
    yield* inner;
    yield end;
}

/**
 * Generates complete routes by combining start and end points with inner routes.
 * 
 * @template T - The type of elements in the routes
 * @param {T} start - The starting point
 * @param {T} end - The ending point
 * @param {Iterable<Iterable<T>>} inner - Collection of inner routes to combine
 * @yields {Iterable<T>} Complete routes including start, inner points, and end
 */
function* generateRoutes<T>(start: T, end: T, inner: Iterable<Iterable<T>>) {
    for (const innerRoute of inner) {
        yield startAndEnd(start, end, innerRoute);
    }
}

/**
 * Solves the traveling salesman problem by finding the shortest path that visits all destinations.
 * The path must start at a specific point and end at another specific point.
 * 
 * @template T - The type of destinations
 * @param {ArrayLike<T> & Iterable<T>} innerDestinations - The destinations to visit
 * @param {T} start - The starting destination
 * @param {T} end - The ending destination
 * @param {(pair: [T, T]) => number} computeDistance - Function to compute distance between two destinations
 * @returns {T[]} The shortest path that visits all destinations
 * @throws {Error} If no valid route is found
 */
export function travelingSalesman<T>(
    innerDestinations: ArrayLike<T> & Iterable<T>,
    start: T,
    end: T,
    computeDistance: (pair: [T, T]) => number
): T[] {
    // Convert to array to work with permutations function
    const destinationsArray = Array.from(innerDestinations);

    // Get all permutations of the inner destinations
    const destinationsCount = destinationsArray.length;
    const permutationsIter = permutations(destinationsArray, destinationsCount);

    // Create a route for each permutation that includes the start and end destinations
    const routes = generateRoutes(start, end, permutationsIter);

    const distances = calculateDistances(routes, computeDistance);

    // Find the route with the minimum distance
    const minRoute = reduce.toMin(distances, ([distance]) => distance);

    if (!minRoute) {
        return [start, end];
    } else {
        return minRoute![1];
    }
}

/**
 * Creates a cached version of a function that stores results in memory to avoid recomputation.
 * 
 * @template Input - The type of the function input
 * @template Output - The type of the function output
 * @param {(input: Input) => Output} f - The function to cache
 * @returns {(input: Input) => Output} A new function that caches results of the original function
 * @example
 * ```typescript
 * const expensiveFn = (n: number) => { 
 *   // expensive computation
 *   return n * n; 
 * };
 * const cachedExpensiveFn = cachedFn(expensiveFn);
 * cachedExpensiveFn(5); // computes result
 * cachedExpensiveFn(5); // returns cached result
 * ```
 */
export function cachedFn<Input, Output>(f: (input: Input) => Output): (input: Input) => Output {
    const cache = new Map<Input, Output>();

    return (input: Input): Output => {
        if (cache.has(input)) {
            return cache.get(input)!;
        }
        const result = f(input);
        cache.set(input, result);
        return result;
    };
}

export function handRolledTravelingSalesman<T>(
    destinations: ArrayLike<T> & Iterable<T>,
    start: T,
    end: T,
    computeDistance: (pair: [T, T]) => number
): T[] {
    let minDistance = Infinity;
    let minRoute: T[] = [];

    const destinationsCount = destinations.length;
    const permutationsIter = permutations(destinations, destinationsCount);

    for (const route of permutationsIter) {
        let distance = total_distance(route, computeDistance);

        distance += computeDistance([start, route[0]]);
        distance += computeDistance([route[route.length - 1], end]);

        if (distance < minDistance) {
            minDistance = distance;
            minRoute = route;
        }
    }

    return [start, ...minRoute, end];
}   