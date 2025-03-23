use coding_compairson::{hand_rolled_traveling_salesman, traveling_salesman};
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
    let end = destinations.iter().copied().max().unwrap_or(1) + 1;

    // Benchmark the referenced version
    c.bench_function("traveling_salesman_ref", |b| {
        let compute_distance = |pair: (&&i32, &&i32)| pair.0.abs_diff(**pair.1);

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
        let compute_distance = |pair: (&i32, &i32)| pair.0.abs_diff(*pair.1);

        b.iter(|| {
            traveling_salesman(
                black_box(destinations.clone().into_iter()),
                black_box(start),
                black_box(end),
                &compute_distance,
            )
        });
    });

    // Benchmark the hand-rolled version
    c.bench_function("hand_rolled_traveling_salesman", |b| {
        b.iter(|| {
            hand_rolled_traveling_salesman(
                black_box(&destinations),
                black_box(&start),
                black_box(&end),
            )
        });
    });
}

criterion_group!(benches, benchmark_traveling_salesman);
criterion_main!(benches);
