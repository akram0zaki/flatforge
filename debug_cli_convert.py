"""
Debug script for the FlatForge CLI convert command.

This script allows you to debug the convert command in your IDE.
"""
import sys
from flatforge.cli import cli

if __name__ == "__main__":
    # Set up the arguments for the convert command
    sys.argv = [
        "flatforge",
        "convert",
        "--input-config", "samples/config/employee_csv.yaml",
        "--output-config", "samples/config/employee_fixed_length.yaml",
        "--input", "samples/input/employee_data.csv",
        "--output", "samples/output/debug_converted.txt",
        "--errors", "samples/output/debug_convert_errors.txt"
    ]
    
    # Call the CLI function
    cli() 