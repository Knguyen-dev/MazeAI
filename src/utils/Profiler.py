import time
import tracemalloc
from datetime import datetime


def profile(maze_num_row, maze_num_col, log_file_path, func,  *args, **kwargs):
    """Profiles both execution time and memory usage of a function."""
    tracemalloc.start()
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time

    # Log data to a function
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    with open(log_file_path, "a") as log_file:
        log_file.write(f"{maze_num_row}x{maze_num_col},{func.__name__},{execution_time:.4f} seconds,{current / 1024:.2f} KB, peak: {peak / 1024:.2f} KB,{timestamp}\n")

    return result

