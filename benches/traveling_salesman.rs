use coding_compairson::{cached_fn, traveling_salesman};
use criterion::{black_box, criterion_group, criterion_main, Criterion};

// Generate a list of destinations that will stress the algorithm
fn generate_stress_test_destinations() -> Vec<i32> {
    // Using 8 destinations will give us 8! = 40320 permutations
    // This is enough to stress the algorithm while still being reasonable for benchmarking
    (1..=8).collect()
}

fn benchmark_traveling_salesman(c: &mut Criterion) {
    let destinations = generate_stress_test_destinations();
    let start = 0;
    let end = 9;

    // Benchmark the referenced version
    c.bench_function("traveling_salesman_ref", |b| {
        let compute_distance = |pair: (&i32, &i32)| pair.0.abs_diff(*pair.1);
        let compute_distance = cached_fn(compute_distance);

        b.iter(|| {
            traveling_salesman(
                black_box(destinations.iter()),
                black_box(&start),
                black_box(&end),
                &compute_distance,
            )
        });
    });

    // Benchmark the owned version
    c.bench_function("traveling_salesman_owned", |b| {
        let compute_distance = |pair: (i32, i32)| pair.0.abs_diff(pair.1);
        let compute_distance = cached_fn(compute_distance);

        b.iter(|| {
            traveling_salesman(
                black_box(destinations.clone().into_iter()),
                black_box(start),
                black_box(end),
                &compute_distance,
            )
        });
    });
}

criterion_group!(benches, benchmark_traveling_salesman);
criterion_main!(benches);
