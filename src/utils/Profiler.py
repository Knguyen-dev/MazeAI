import time
import tracemalloc


def profile(func, *args, **kwargs):
    """Profiles both execution time and memory usage of a function."""
    tracemalloc.start()
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time

    # Log data to a function
    with open("execution_data.log", "a") as log_file:
        log_file.write(f"{func.__name__}: {execution_time:.4f} seconds; {current / 1024:.2f} KB, peak: {peak / 1024:.2f} KB \n")

    return result

