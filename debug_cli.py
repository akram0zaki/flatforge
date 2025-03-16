"""
Debug script for the FlatForge CLI.

This script allows you to debug the CLI in your IDE by directly calling the CLI function
with command-line arguments.
"""
import sys
from flatforge.cli import cli

if __name__ == "__main__":
    # Set up the arguments you want to pass to the CLI
    # For example, to run: flatforge validate --config config.yaml --input input.csv
    # sys.argv = [
    #     "flatforge",  # Program name (can be anything)
    #     "validate",   # Command
    #     "--config", "samples/config/employee_csv.yaml",
    #     "--input", "samples/input/employee_data.csv",
    #     "--output", "samples/output/debug_output.csv",
    #     "--errors", "samples/output/debug_errors.csv"
    # ]
    sys.argv = [
        "flatforge",  # Program name (can be anything)
        "validate",   # Command
        "--config", "samples/config/employee_fixed_length.yaml",
        "--input", "samples/input/employee_data.txt",
        "--output", "samples/output/debug_output.csv",
        "--errors", "samples/output/debug_errors.csv"
    ]
    
    # Call the CLI function
    cli() 