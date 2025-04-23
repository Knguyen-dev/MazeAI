from utils.Profiler import Profiler

profiler = Profiler()


# Generate data by running these first
# profiler.mass_profile()
# profiler.mass_profile()
# profiler.mass_profile()
# profiler.mass_profile()
# profiler.mass_profile()

# Then generate plots by running these
profiler.generate_visualizations()

print("Done?")