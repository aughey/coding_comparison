/**
 * For all of the inner destinations, find the shortest path that visits all of them starting
 * at `start` and ending at `end`.
 * 
 * @param innerDestinations - The destinations to visit
 * @param start - The starting destination
 * @param end - The ending destination
 * @param computeDistance - A function that computes the distance between two destinations
 * @returns The shortest path that visits all of the inner destinations starting at `start` and ending at `end`
 */
export function travelingSalesman<T, Distance extends number>(
    innerDestinations: T[],
    start: T,
    end: T,
    computeDistance: (pair: [T, T]) => Distance
): T[] {
    // Get all permutations of the inner destinations
    const destinationsCount = innerDestinations.length;
    const permutations = getPermutations(innerDestinations, destinationsCount);

    // Create a route for each permutation that includes the start and end destinations
    const routes = permutations.map(permutation => {
        return [start, ...permutation, end];
    });

    // Calculate the distance for each route
    const routeDistances = routes.map(route => {
        const distances: Distance[] = [];
        for (let i = 0; i < route.length - 1; i++) {
            distances.push(computeDistance([route[i], route[i + 1]]));
        }
        return {
            distance: distances.reduce((a, b) => (a + b) as Distance, 0 as Distance),
            route
        };
    });

    // Find the route with the shortest distance
    const minRoute = routeDistances.reduce((min, curr) =>
        curr.distance < min.distance ? curr : min
    );

    return minRoute.route;
}

/**
 * Generates all possible permutations of an array
 */
function getPermutations<T>(arr: T[], size: number): T[][] {
    if (size === 0) return [[]];

    const permutations: T[][] = [];

    for (let i = 0; i < arr.length; i++) {
        const current = arr[i];
        const remaining = [...arr.slice(0, i), ...arr.slice(i + 1)];
        const subPermutations = getPermutations(remaining, size - 1);

        for (const subPerm of subPermutations) {
            permutations.push([current, ...subPerm]);
        }
    }

    return permutations;
}

/**
 * Caches the results of any function call using a Map
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

// Example usage and tests
function runTests() {
    // Test with numbers
    const destinations = [1, 2, 3, 4, 5];
    const start = 0;
    const end = 6;

    // Works with references
    const computeDistanceRef = cachedFn((pair: [number, number]): number =>
        Math.abs(pair[0] - pair[1])
    );

    const result = travelingSalesman(
        destinations,
        start,
        end,
        computeDistanceRef
    );
    console.log('Result with references:', result);

    // Test empty destinations
    const emptyResult = travelingSalesman(
        [],
        0,
        1,
        computeDistanceRef
    );
    console.log('Empty destinations result:', emptyResult);

    // Test single destination
    const singleResult = travelingSalesman(
        [1],
        0,
        2,
        computeDistanceRef
    );
    console.log('Single destination result:', singleResult);
}

// Run tests if this file is executed directly
if (typeof window === 'undefined') {
    runTests();
} 