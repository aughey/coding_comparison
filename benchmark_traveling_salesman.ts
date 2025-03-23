import { Suite } from 'benchmark';
import { travelingSalesman, handRolledTravelingSalesman } from './traveling_salesman';

function generateStressTestDestinations(): number[] {
    // Using 8 destinations will give us 8! = 40320 permutations
    // This matches the Rust and Python benchmarks
    return Array.from({ length: 8 }, (_, i) => i + 1);
}

// Create benchmark suite
const suite = new Suite();

// Setup common variables
const destinations = generateStressTestDestinations();
const start = 0;
const end = 9;

// Create distance function
const computeDistanceRef = (pair: [number, number]) => Math.abs(pair[0] - pair[1]);

// Add benchmarks
suite
    .add('traveling_salesman_ref', () => {
        const result = travelingSalesman(
            destinations,
            start,
            end,
            computeDistanceRef
        );
        // Verify result is correct (should be in ascending order for this case)
        if (JSON.stringify(result) !== JSON.stringify([0, ...Array.from({ length: 8 }, (_, i) => i + 1), 9])) {
            throw new Error('Incorrect result');
        }
    })
    .add('handrolled_traveling_salesman', () => {
        const result = handRolledTravelingSalesman(
            destinations,
            start,
            end,
            computeDistanceRef
        );
        // Verify result is correct (should be in ascending order for this case)
        if (JSON.stringify(result) !== JSON.stringify([0, ...Array.from({ length: 8 }, (_, i) => i + 1), 9])) {
            throw new Error('Incorrect result');
        }
    })
    .on('cycle', function (event: any) {
        console.log(String(event.target));
    })
    .on('complete', function (this: Suite) {
        console.log('Fastest is ' + this.filter('fastest').map('name'));

        // Get detailed stats
        const benchmarks = (this as any) as { [key: string]: any }[];
        const stats = benchmarks.map(bench => ({
            name: bench.name,
            mean: bench.stats.mean * 1000, // Convert to ms
            moe: bench.stats.moe * 1000,
            rme: bench.stats.rme,
            sem: bench.stats.sem * 1000,
            deviation: bench.stats.deviation * 1000,
            variance: bench.stats.variance * 1000000,
            ops: bench.hz
        }));

        console.log('\nDetailed Statistics:');
        stats.forEach(stat => {
            console.log(`\n${stat.name}:`);
            console.log(`  Mean (ms):     ${stat.mean.toFixed(3)} ±${stat.moe.toFixed(3)}`);
            console.log(`  Ops/sec:       ${stat.ops.toFixed(2)}`);
            console.log(`  Deviation (ms): ${stat.deviation.toFixed(3)}`);
            console.log(`  RME (%):       ${stat.rme.toFixed(2)}`);
        });
    })
    .run({ async: true }); 