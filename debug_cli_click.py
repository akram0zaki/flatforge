"""
Debug script for the FlatForge CLI using Click's test runner.

This script allows you to debug the CLI in your IDE using Click's test runner,
which provides more detailed output and error handling.
"""
from click.testing import CliRunner
from flatforge.cli import cli

if __name__ == "__main__":
    runner = CliRunner()
    result = runner.invoke(cli, [
        "validate",
        "--config", "samples/config/employee_csv.yaml",
        "--input", "samples/input/employee_data.csv",
        "--output", "samples/output/debug_output.csv",
        "--errors", "samples/output/debug_errors.csv"
    ])
    
    # Print the result
    print(f"Exit code: {result.exit_code}")
    if result.exception:
        print(f"Exception: {result.exception}")
    print(f"Output:\n{result.output}") 