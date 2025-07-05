# Performance Testing - Measuring and Optimizing

This section covers performance testing with pytest, including benchmarking, load testing, memory profiling, and performance assertions to ensure your code meets performance requirements.

## 📋 What You'll Learn

1. **Basic Performance Testing**
   - Timing measurements
   - Performance assertions
   - Benchmarking functions

2. **Advanced Performance Testing**
   - Memory profiling
   - Load testing
   - Performance regression testing

3. **Performance Tools**
   - pytest-benchmark
   - memory-profiler
   - Custom performance fixtures

4. **Real-World Scenarios**
   - API performance testing
   - Database query optimization
   - Algorithm benchmarking

## 🚀 Step-by-Step Guide

### Step 1: Basic Timing

Measure execution time of functions:

```python
import pytest
import time

def test_function_performance():
    start_time = time.time()
    
    # Function to test
    result = expensive_function()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Performance assertion
    assert execution_time < 1.0  # Should complete within 1 second
    assert result is not None

def test_algorithm_performance():
    # Test with different input sizes
    for size in [100, 1000, 10000]:
        start_time = time.time()
        result = sort_algorithm(generate_data(size))
        execution_time = time.time() - start_time
        
        # Performance should scale reasonably
        assert execution_time < size * 0.001  # Linear scaling
```

### Step 2: Using pytest-benchmark

Use the pytest-benchmark plugin for accurate benchmarking:

```python
import pytest

def test_benchmark_function(benchmark):
    result = benchmark(expensive_function)
    assert result is not None

def test_benchmark_algorithm(benchmark):
    data = generate_test_data(1000)
    result = benchmark(sort_algorithm, data)
    assert len(result) == 1000

@pytest.mark.benchmark(
    group="sorting",
    min_rounds=100,
    max_rounds=1000,
    warmup=True
)
def test_sorting_algorithms(benchmark):
    data = generate_test_data(1000)
    
    # Test different sorting algorithms
    result1 = benchmark(lambda: sorted(data))
    result2 = benchmark(lambda: custom_sort(data))
    
    assert len(result1) == len(result2)
```

### Step 3: Memory Profiling

Monitor memory usage during execution:

```python
import pytest
from memory_profiler import profile

@profile
def memory_intensive_function():
    large_list = [i for i in range(1000000)]
    return sum(large_list)

def test_memory_usage():
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Run memory-intensive operation
    result = memory_intensive_function()
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Memory should not increase by more than 100MB
    assert memory_increase < 100 * 1024 * 1024
    assert result == 499999500000
```

### Step 4: Load Testing

Test performance under load:

```python
import pytest
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def test_concurrent_requests():
    def make_request():
        start_time = time.time()
        response = api_client.get("/api/endpoint")
        end_time = time.time()
        return end_time - start_time
    
    # Test with multiple concurrent requests
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(100)]
        response_times = [future.result() for future in futures]
    
    # All requests should complete within reasonable time
    assert all(time < 2.0 for time in response_times)
    assert len(response_times) == 100
```

## 📁 File Structure

```
08_performance_testing/
├── README.md
├── test_basic_performance.py
├── test_benchmarking.py
├── test_memory_profiling.py
├── test_load_testing.py
├── test_algorithm_performance.py
├── test_api_performance.py
├── conftest.py
├── performance_utils.py
└── algorithms.py
```

## 🎯 Key Concepts

### 1. Performance Measurement
- Use accurate timing methods
- Consider system load and variability
- Run multiple iterations for reliable results
- Account for warmup effects

### 2. Benchmarking
- Use dedicated benchmarking tools
- Compare different implementations
- Track performance over time
- Set performance baselines

### 3. Memory Profiling
- Monitor memory usage patterns
- Detect memory leaks
- Optimize memory-intensive operations
- Set memory usage limits

### 4. Load Testing
- Test under realistic conditions
- Measure response times under load
- Identify performance bottlenecks
- Test scalability limits

## 🔧 Advanced Patterns

### Custom Performance Fixtures
```python
@pytest.fixture
def performance_timer():
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
            return self.end_time - self.start_time
        
        def assert_faster_than(self, max_time):
            execution_time = self.end_time - self.start_time
            assert execution_time < max_time, f"Execution took {execution_time}s, expected < {max_time}s"
    
    return Timer()

def test_with_custom_timer(performance_timer):
    performance_timer.start()
    result = expensive_operation()
    performance_timer.stop()
    
    performance_timer.assert_faster_than(1.0)
    assert result is not None
```

### Performance Regression Testing
```python
def test_performance_regression(benchmark):
    # Baseline performance from previous runs
    baseline_time = 0.1  # seconds
    
    def test_function():
        return expensive_operation()
    
    result = benchmark(test_function)
    
    # Performance should not degrade by more than 20%
    assert result.stats.mean < baseline_time * 1.2
```

### Memory Leak Detection
```python
def test_memory_leak():
    import gc
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    
    # Force garbage collection
    gc.collect()
    initial_memory = process.memory_info().rss
    
    # Run operation multiple times
    for _ in range(100):
        result = potentially_leaky_function()
        del result
    
    # Force garbage collection again
    gc.collect()
    final_memory = process.memory_info().rss
    
    # Memory should not increase significantly
    memory_increase = final_memory - initial_memory
    assert memory_increase < 10 * 1024 * 1024  # 10MB
```

### Load Testing with Metrics
```python
def test_api_load_performance():
    import statistics
    
    def make_api_request():
        start_time = time.time()
        response = api_client.get("/api/data")
        end_time = time.time()
        return {
            'response_time': end_time - start_time,
            'status_code': response.status_code
        }
    
    # Simulate load
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(make_api_request) for _ in range(200)]
        results = [future.result() for future in futures]
    
    # Analyze performance metrics
    response_times = [r['response_time'] for r in results]
    status_codes = [r['status_code'] for r in results]
    
    # Performance assertions
    assert all(code == 200 for code in status_codes)
    assert statistics.mean(response_times) < 0.5  # Average < 500ms
    assert statistics.percentile(response_times, 95) < 1.0  # 95th percentile < 1s
    assert max(response_times) < 2.0  # Max response time < 2s
```

## 📊 Best Practices

### 1. Measurement Accuracy
- Use high-resolution timers
- Run multiple iterations
- Account for system variability
- Warm up the system before testing

### 2. Performance Baselines
- Establish performance baselines
- Track performance over time
- Set realistic performance targets
- Document performance requirements

### 3. Test Environment
- Use consistent test environments
- Minimize external factors
- Run tests in isolation
- Use dedicated performance testing environments

### 4. Result Analysis
- Analyze performance trends
- Identify bottlenecks
- Set performance thresholds
- Document performance characteristics

## 🎓 Exercises

1. Create performance tests for sorting algorithms
2. Implement memory profiling for data processing functions
3. Build load tests for a simple web API
4. Create performance regression tests
5. Develop custom performance measurement utilities

## 📚 Real-World Examples

### Algorithm Performance Comparison
```python
@pytest.mark.benchmark(group="algorithms")
def test_sorting_algorithm_performance(benchmark):
    data_sizes = [100, 1000, 10000]
    
    for size in data_sizes:
        data = generate_random_data(size)
        
        # Test different sorting algorithms
        result1 = benchmark(lambda: sorted(data))
        result2 = benchmark(lambda: bubble_sort(data))
        result3 = benchmark(lambda: quick_sort(data))
        
        # Verify results are correct
        assert result1 == result2 == result3
        
        # Performance assertions
        assert result1.stats.mean < result2.stats.mean  # Built-in sort should be faster
        assert result3.stats.mean < result2.stats.mean  # Quick sort should be faster than bubble sort
```

### Database Query Performance
```python
def test_database_query_performance(benchmark, database):
    # Test different query patterns
    def simple_query():
        return database.execute("SELECT * FROM users LIMIT 100")
    
    def complex_query():
        return database.execute("""
            SELECT u.name, COUNT(p.id) as post_count
            FROM users u
            LEFT JOIN posts p ON u.id = p.user_id
            GROUP BY u.id, u.name
            HAVING COUNT(p.id) > 5
            ORDER BY post_count DESC
        """)
    
    def indexed_query():
        return database.execute("SELECT * FROM users WHERE email = 'test@example.com'")
    
    # Benchmark queries
    simple_result = benchmark(simple_query)
    complex_result = benchmark(complex_query)
    indexed_result = benchmark(indexed_query)
    
    # Performance assertions
    assert simple_result.stats.mean < 0.1  # Simple query should be fast
    assert indexed_result.stats.mean < simple_result.stats.mean  # Indexed query should be faster
    assert complex_result.stats.mean < 1.0  # Complex query should complete within 1s
```

### API Endpoint Performance
```python
def test_api_endpoint_performance(benchmark, api_client):
    def get_users():
        return api_client.get("/api/users")
    
    def create_user():
        user_data = {"name": "Test User", "email": "test@example.com"}
        return api_client.post("/api/users", json=user_data)
    
    def get_user_by_id():
        return api_client.get("/api/users/1")
    
    # Benchmark different endpoints
    get_users_result = benchmark(get_users)
    create_user_result = benchmark(create_user)
    get_user_result = benchmark(get_user_by_id)
    
    # Performance assertions
    assert get_users_result.stats.mean < 0.5  # GET should be fast
    assert get_user_result.stats.mean < get_users_result.stats.mean  # Single user should be faster
    assert create_user_result.stats.mean < 1.0  # POST should complete within 1s
```

### Memory-Intensive Operations
```python
def test_memory_intensive_operations():
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    
    def process_large_dataset():
        # Simulate processing large dataset
        data = [i for i in range(1000000)]
        processed = [x * 2 for x in data]
        return sum(processed)
    
    # Monitor memory usage
    initial_memory = process.memory_info().rss
    
    result = process_large_dataset()
    
    final_memory = process.memory_info().rss
    memory_used = final_memory - initial_memory
    
    # Memory assertions
    assert memory_used < 200 * 1024 * 1024  # Should use less than 200MB
    assert result == 999999000000  # Verify correct computation
    
    # Test memory cleanup
    del result
    import gc
    gc.collect()
    
    cleanup_memory = process.memory_info().rss
    memory_after_cleanup = cleanup_memory - initial_memory
    
    # Memory should be cleaned up
    assert memory_after_cleanup < 50 * 1024 * 1024  # Should use less than 50MB after cleanup
```

## 📚 Next Steps

After completing this section, you should:
- Understand how to measure and test performance
- Be able to use benchmarking tools effectively
- Know how to profile memory usage
- Understand load testing techniques
- Be familiar with performance optimization strategies

Proceed to the next section: **09_integration_testing/** to learn about integration testing. 