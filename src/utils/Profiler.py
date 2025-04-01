import time
import tracemalloc
import csv
from datetime import datetime
import os

class Profiler:
    @staticmethod
    def profile(func, log_file,*args, **kwargs):
        """
        Profiles execution time and memory usage of a function.
        """
        tracemalloc.start()
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        execution_time = end_time - start_time
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = [timestamp, func.__name__, execution_time, current / 1024, peak / 1024]

        # using a csv file for easier analysis
        log_file = log_file
        file_exists = os.path.isfile(log_file)
        
        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists or os.stat(log_file).st_size == 0:
                writer.writerow(["Timestamp", "Function", "Execution Time (s)", "Memory (KB)", "Peak Memory (KB)"])
            writer.writerow(log_entry)

        return result
    
    @staticmethod
    def clear_log_file(logging_file):
        """
        Clears the log file. Does not delete it, just clear the content.
        """
        # open in write mode to truncate the file (clear contents), or create it if it doesn't exist
        with open(logging_file, 'w') as file:
            pass  # just opening in 'w' mode clears it
        
    @staticmethod
    def benchmark(func, log_file, runs=5, *args, **kwargs):
        """
        Runs the function multiple times and computes average execution time and memory usage
        """
        total_time = 0
        total_memory = 0
        total_peak_memory = 0
        
        for _ in range(runs):
            tracemalloc.start()
            start_time = time.time()
            func(*args, **kwargs)
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            total_time += (end_time - start_time)
            total_memory += current / 1024
            total_peak_memory += peak / 1024

        avg_time = total_time / runs
        avg_memory = total_memory / runs
        avg_peak_memory = total_peak_memory / runs
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = [timestamp, func.__name__, runs, avg_time, avg_memory, avg_peak_memory]

        file_exists = os.path.isfile(log_file)
        
        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists or os.stat(log_file).st_size == 0:
                writer.writerow(["Timestamp", "Function", "Runs", "Avg Execution Time (s)", "Avg Memory (KB)", "Avg Peak Memory (KB)"])
            writer.writerow(log_entry)

        return avg_time, avg_memory, avg_peak_memory