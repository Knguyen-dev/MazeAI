import time
import tracemalloc
import csv
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt

class Profiler:
    def __init__(self):
        self.std_log_file_header = ["Timestamp", "Function", "Execution Time (s)", "Memory (KB)", "Peak Memory (KB)"]
        self.benchmark_log_file_header = ["Timestamp", "Function", "Runs", "Avg Execution Time (s)", "Avg Memory (KB)", "Avg Peak Memory (KB)"]
    
    def _log_entry(self, log_file, entry, header):
        file_exists = os.path.isfile(log_file)
        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists or os.stat(log_file).st_size == 0:
                writer.writerow(header)
            writer.writerow(entry)
    
    def profile(self, func, log_file,*args, **kwargs):
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
    
        self._log_entry(log_file, log_entry, self.std_log_file_header)

        return result
    
    @staticmethod
    def clear_log_file(log_file):
        """
        Clears the log file. Does not delete it, just clear the content.
        """
        # open in write mode to truncate the file (clear contents), or create it if it doesn't exist
        with open(log_file, 'w') as file:
            pass #opening file in write mode clears the content
        
    def benchmark(self, func, log_file, benchmark_log_file=None, runs=5, *args, **kwargs):
        """
        Runs the function multiple times and computes average execution time and memory usage.
        Individual runs are logged to the normal log file, aggregated results to the benchmark file.
        """
        if benchmark_log_file is None:
            benchmark_log_file = log_file + ".benchmark"
            
        total_time = 0
        total_memory = 0
        total_peak_memory = 0
        
        for _ in range(runs):
            # profile each individual run and log to the main log file
            tracemalloc.start()
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            execution_time = end_time - start_time
            memory = current / 1024
            peak_memory = peak / 1024
            
            # log individual run to normal log file
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = [timestamp, func.__name__, execution_time, memory, peak_memory]
            
            file_exists = os.path.isfile(log_file)
            self._log_entry(log_file, log_entry, self.std_log_file_header)
            
            total_time += execution_time
            total_memory += memory
            total_peak_memory += peak_memory
        
        # calculate averages for the benchmark log
        avg_time = total_time / runs
        avg_memory = total_memory / runs
        avg_peak_memory = total_peak_memory / runs
        
        # log aggregated results to benchmark file
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        benchmark_entry = [timestamp, func.__name__, runs, avg_time, avg_memory, avg_peak_memory]
        
        benchmark_file_exists = os.path.isfile(benchmark_log_file)
        self._log_entry(benchmark_log_file, benchmark_entry, self.benchmark_log_file_header)

        return avg_time, avg_memory, avg_peak_memory
