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
   - By-reference: ~6.87ms (min: 6.73ms, max: 7.01ms)
   - By-owned: ~7.33ms (min: 7.14ms, max: 7.55ms)
   - Difference: ~6.7% slower for owned
   - Operations per second: ~145.6 (ref), ~136.5 (owned)

2. Python:
   - By-reference: ~210.54ms (min: 195.72ms, max: 233.54ms)
   - Operations per second: ~4.75
   - Standard deviation: ~12.48ms

3. TypeScript (Node.js):
   - By-reference: ~580.48ms (min: ~527.35ms, max: ~621.31ms)
   - Operations per second: ~1.72
   - Standard deviation: ~53.13ms

Performance ranking (fastest to slowest):
1. Rust: ~6.87ms
2. Python: ~210.54ms (30.6x slower than Rust)
3. TypeScript: ~580.48ms (84.5x slower than Rust, 2.76x slower than Python)

Key observations:
- Rust shows significant performance improvement after removing caching
- Python maintains relatively consistent performance
- TypeScript shows improved consistency in execution time with lower variance
- All implementations maintain their relative performance rankings

## Code Complexity Analysis

All three implementations follow a similar algorithmic approach using iterators/generators. Here's a detailed comparison:

### Line Count Analysis
1. Rust (lib.rs):
   - Total lines: ~120
   - Core functions: ~80 lines
   - Tests: ~40 lines
   - Main algorithm: ~30 lines

2. Python (traveling_salesman.py):
   - Total lines: ~150
   - Core functions: ~100 lines
   - Tests: ~50 lines
   - Main algorithm: ~40 lines

3. TypeScript (traveling_salesman.ts):
   - Total lines: ~180
   - Core functions: ~130 lines
   - Tests: ~50 lines
   - Main algorithm: ~50 lines

### Code Structure Comparison

1. Rust:
   - Uses iterator chains and combinators
   - Most concise implementation
   - Strong type system with generics
   - Zero-cost abstractions
   - Key features:
     - Iterator chaining with `chain()`
     - Tuple windows with `tuple_windows()`
     - Generic type parameters
     - Efficient memory usage

2. Python:
   - Uses generators and itertools
   - Most readable implementation
   - Dynamic typing with type hints
   - Key features:
     - Generator functions with `yield`
     - itertools for permutations
     - Type hints for clarity
     - Simple caching with decorators

3. TypeScript:
   - Uses generators and iterables
   - Most verbose implementation
   - Static typing with generics
   - Key features:
     - Generator functions with `yield*`
     - Iterable interfaces
     - Explicit type annotations
     - Map-based caching

### Complexity Metrics

1. Cyclomatic Complexity:
   - Rust: Low (mostly linear iterator chains)
   - Python: Medium (generator functions with multiple yields)
   - TypeScript: Medium-High (explicit iteration handling)

2. Memory Usage:
   - Rust: Most efficient (zero-copy where possible)
   - Python: Moderate (generator-based streaming)
   - TypeScript: Moderate-High (array conversions)

3. Type Safety:
   - Rust: Strongest (compile-time guarantees)
   - TypeScript: Strong (compile-time checks)
   - Python: Weak (runtime type hints)

### Key Differences

1. Memory Management:
   - Rust: Manual control with zero-cost abstractions
   - Python: Automatic with garbage collection
   - TypeScript: Automatic with V8 garbage collection

2. Type System:
   - Rust: Strong, static, with ownership
   - TypeScript: Strong, static, with structural typing
   - Python: Dynamic with optional type hints

3. Iterator Implementation:
   - Rust: Native iterator traits
   - Python: Generator functions
   - TypeScript: Generator functions with iterables

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