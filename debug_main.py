"""
Debug script for the FlatForge CLI main module.

This script allows you to debug the main.py module directly in your IDE.
"""
from flatforge.cli.main import main

if __name__ == "__main__":
    # Call the main function with the arguments you want to test
    main(
        config="samples/config/employee_csv.yaml",
        input="samples/input/employee_data.csv",
        output="samples/output/debug_output.csv",
        errors="samples/output/debug_errors.csv",
        chunk_size=0,
        show_progress=False
    ) 