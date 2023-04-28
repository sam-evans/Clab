# Creating profiling reports

Use cProfile and Snakeviz

1. Download Snakeviz with `pip install snakeviz`
2. Create a .dat file containing the profiling report by running `python -m cProfile -o report.dat <PROGRAM>.py`

# Reading a report

Open the profiling report with `python -m snakeviz report.dat`
