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

    def performance_analysis(self, func, grid_sizes, log_file, output_plot_path=None, runs_per_size=3, maze_generator=None,**kwargs):
        """
        Tests a function with different input sizes and creates a plot of execution time and memory usage.
        Particularly useful for analyzing maze solving algorithms with different grid dimensions.
        
        Args:
            func (function): Function to test (should accept a grid as first parameter)
            grid_sizes (list): List of grid sizes to test (e.g. [10, 20, 30, 40])
            log_file (str): Path to the log file for individual runs
            output_plot_path (str, optional): Path to save the resulting plot. If None, plot is displayed but not saved.
            runs_per_size (int, optional): Number of runs per grid size for averaging. Defaults to 3.
            **kwargs: Additional arguments to pass to the function
        
        Returns:
            dict: Dictionary with grid sizes as keys and performance metrics as values
        """
        from grid.Grid import Grid  
        from algorithms.MazeGenerator import MazeGenerator
        results = {}

        sizes = []
        times = []
        memory_usage = []
        peak_memory = []

        for size in grid_sizes:
            print(f"Testing grid size: {size}x{size}")
            grid = Grid(size, size)
            if maze_generator == None:
                maze_generator = MazeGenerator.randomized_kruskal
            maze_generator(grid)


            avg_time, avg_mem, avg_peak = self.benchmark(
                func, 
                log_file, 
                runs=runs_per_size, 
                grid=grid, 
                **kwargs
            )

            results[size] = {
                'time': avg_time,
                'memory': avg_mem,
                'peak_memory': avg_peak
            }

            sizes.append(size)
            times.append(avg_time)
            memory_usage.append(avg_mem)
            peak_memory.append(avg_peak)

        # create visualization
        plt.figure(figsize=(15, 10))

        # plot execution time
        plt.subplot(2, 1, 1)
        plt.plot(sizes, times, 'o-', color='blue', linewidth=2)
        plt.title(f'Execution Time vs Grid Size for {func.__name__}')
        plt.xlabel('Grid Size (n×n)')
        plt.ylabel('Execution Time (seconds)')
        plt.grid(True)

        # plot memory usage
        plt.subplot(2, 1, 2)
        plt.plot(sizes, memory_usage, 'o-', color='green', label='Avg Memory', linewidth=2)
        plt.plot(sizes, peak_memory, 'o-', color='red', label='Peak Memory', linewidth=2)
        plt.title(f'Memory Usage vs Grid Size for {func.__name__}')
        plt.xlabel('Grid Size (n×n)')
        plt.ylabel('Memory (KB)')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()

        if output_plot_path:
            plt.savefig(output_plot_path)
            print(f"Plot saved to {output_plot_path}")
        else:
            plt.show()
        
        return results