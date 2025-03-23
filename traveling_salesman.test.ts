import { travelingSalesman, cachedFn } from './traveling_salesman';

describe('cachedFn', () => {
    it('should cache function results', () => {
        let callCount = 0;
        const testFn = (x: number) => {
            callCount++;
            return x * 2;
        };
        const cachedTestFn = cachedFn(testFn);

        // Call with same input multiple times
        cachedTestFn(5);
        cachedTestFn(5);
        cachedTestFn(5);
        expect(callCount).toBe(1);

        // Call with different input
        cachedTestFn(10);
        expect(callCount).toBe(2);
    });
});

describe('travelingSalesman', () => {
    const computeDistanceRef = cachedFn((pair: [number, number]): number =>
        Math.abs(pair[0] - pair[1])
    );

    it('should find shortest path for multiple destinations', () => {
        const destinations = [1, 2, 3, 4, 5];
        const start = 0;
        const end = 6;

        const result = travelingSalesman(
            destinations,
            start,
            end,
            computeDistanceRef
        );

        // The result should be an array containing all destinations including start and end
        expect(result).toContain(start);
        expect(result).toContain(end);
        destinations.forEach(dest => expect(result).toContain(dest));
        expect(result.length).toBe(destinations.length + 2);
    });

    it('should handle empty destinations', () => {
        const result = travelingSalesman(
            [],
            0,
            1,
            computeDistanceRef
        );

        expect(result).toEqual([0, 1]);
    });

    it('should handle single destination', () => {
        const result = travelingSalesman(
            [1],
            0,
            2,
            computeDistanceRef
        );

        expect(result).toEqual([0, 1, 2]);
    });
}); 