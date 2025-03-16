"""
Debug script for the FlatForge CLI with chunked processing.

This script allows you to debug the CLI with chunked processing and progress reporting.
"""
import sys
from flatforge.cli import cli

if __name__ == "__main__":
    # Set up the arguments for chunked processing
    sys.argv = [
        "flatforge",
        "validate",
        "--config", "samples/config/employee_csv.yaml",
        "--input", "samples/input/employee_data.csv",
        "--output", "samples/output/debug_chunked_output.csv",
        "--errors", "samples/output/debug_chunked_errors.csv",
        "--chunk-size", "2",  # Process 2 records at a time
        "--show-progress"     # Show progress bar
    ]
    
    # Call the CLI function
    cli() 