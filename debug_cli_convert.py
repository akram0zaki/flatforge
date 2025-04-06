"""
Debug script for the CLI convert command.

This script is used to debug the convert command of the CLI.
"""
import sys
from flatforge.cli.main import main

if __name__ == "__main__":
    # Set up the arguments for the convert command
    sys.argv = [
        "flatforge",
        "convert",
        "--input-config", "samples/config/employee_csv.yaml",
        "--output-config", "samples/config/employee_fixed_length.yaml",
        "--input", "samples/input/employee_data.csv",
        "--output", "samples/output/converted_output.txt",
        "--errors", "samples/output/converted_errors.csv"
    ]
    
    # Call the CLI function
    main() 