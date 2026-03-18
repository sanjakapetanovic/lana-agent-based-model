#!/usr/bin/env python3
"""
LANA Protocol v3.1 — Complete Analysis Pipeline
Usage: python run_analysis.py <data_directory> [output_directory]

Expects BehaviorSpace spreadsheet CSV files in the data directory.
Generates all figures (Fig 2–9) and tables (Tab 1–7, S1) in the output directory.

Example:
    python run_analysis.py ../data/ ../output/
"""
import sys, os, importlib

if len(sys.argv) < 2:
    print("Usage: python run_analysis.py <data_directory> [output_directory]")
    print("Example: python run_analysis.py ../data/ ../output/")
    sys.exit(1)

results_dir = os.path.abspath(sys.argv[1])
output_dir = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(os.getcwd(), "output")

if not os.path.isdir(results_dir):
    print(f"Error: {results_dir} is not a directory")
    sys.exit(1)

os.makedirs(output_dir, exist_ok=True)

# Set environment variables so sub-scripts can find paths
os.environ['LANA_DATA_DIR'] = results_dir
os.environ['LANA_OUTPUT_DIR'] = output_dir

# Add this directory to path so imports work
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

print(f"Data directory:   {results_dir}")
print(f"Output directory: {output_dir}")
print()

print("Running generate_all_analysis.py...")
exec(open(os.path.join(script_dir, 'generate_all_analysis.py')).read())

print("\nRunning generate_remaining_figs.py...")
exec(open(os.path.join(script_dir, 'generate_remaining_figs.py')).read())

print(f"\nDone! Check {output_dir}/ for figures and tables.")
