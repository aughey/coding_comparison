# Coding Comparison

This repository contains implementations of the Traveling Salesman Problem in Rust, Python, and TypeScript, along with benchmarks to compare their performance.

## Project Structure

```
.
├── src/                    # Rust implementation
│   └── lib.rs
├── python_impl/           # Python implementation
│   └── traveling_salesman.py
├── traveling_salesman.ts  # TypeScript implementation
├── benchmark_traveling_salesman.py  # Python benchmarks
├── benchmark_traveling_salesman.ts  # TypeScript benchmarks
├── benches/               # Rust benchmarks
│   └── traveling_salesman.rs
└── tests/                # Test files
    └── traveling_salesman_test.py
```

## Prerequisites

- Rust (latest stable version)
- Python 3.11+
- Node.js (latest LTS version)
- npm (comes with Node.js)

## Setup

### Rust Setup
```bash
# No additional setup needed, just ensure Rust is installed
```

### Python Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt
```

### TypeScript Setup
```bash
# Install dependencies
npm install
```

## Running Tests

### Rust Tests
```bash
cargo test
```

### Python Tests
```bash
# Make sure virtual environment is activated
source venv/bin/activate
python -m pytest tests/
```

### TypeScript Tests
```bash
npm test
```

## Running Benchmarks

### Rust Benchmarks
```bash
cargo bench
```

### Python Benchmarks
```bash
# Make sure virtual environment is activated
source venv/bin/activate
python -m pytest benchmark_traveling_salesman.py --benchmark-only
```

For more detailed benchmark output:
```bash
python -m pytest benchmark_traveling_salesman.py --benchmark-only --benchmark-verbose
```

### TypeScript Benchmarks
```bash
npm run benchmark
```

## Benchmark Results

The benchmarks use 8 destinations (8! = 40,320 permutations) to stress test the implementations. Here are the latest results:

1. Rust:
   - By-reference: ~16.5ms (min: 16.24ms, max: 16.80ms)
   - By-owned: ~18.3ms (min: 18.07ms, max: 18.49ms)
   - Difference: ~11% slower for owned
   - Operations per second: ~60.6 (ref), ~54.7 (owned)

2. Python:
   - By-reference: ~206.8ms (min: 172.8ms, max: 246.7ms)
   - Operations per second: ~4.84
   - Standard deviation: ~31.8ms

3. TypeScript (Node.js):
   - By-reference: ~779.7ms (min: ~582ms, max: ~978ms)
   - Operations per second: ~1.28
   - Standard deviation: ~197.9ms

Performance ranking (fastest to slowest):
1. Rust: ~16.5ms
2. Python: ~206.8ms (12.5x slower than Rust)
3. TypeScript: ~779.7ms (47.3x slower than Rust, 3.8x slower than Python)

Key observations:
- Rust shows the most consistent performance with low standard deviation
- Python has moderate variance in execution time
- TypeScript shows the highest variance in execution time
- All implementations show some performance regression compared to previous runs

## Implementation Details

All three implementations:
- Solve the Traveling Salesman Problem
- Support custom distance functions
- Include caching for distance calculations
- Handle edge cases (empty destinations, single destination)
- Use similar algorithms and data structures

Key differences:
- Rust uses zero-cost abstractions and compile-time optimizations
- Python leverages its highly optimized C implementation for core operations
- TypeScript runs on Node.js's V8 engine with JavaScript's dynamic typing overhead

## License

MIT License