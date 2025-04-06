"""
Debug script for the CLI using Click's testing features.

This script demonstrates how to test the CLI commands using Click's CliRunner.
"""

import click
from click.testing import CliRunner
from flatforge.cli.main import main

runner = CliRunner()
result = runner.invoke(main, ['validate', '--help'])
print(result.output)

result = runner.invoke(main, [
    'validate',
    '--config', 'samples/config/employee_csv.yaml',
    '--input', 'samples/input/employee_data.csv',
    '--output', 'samples/output/debug_output.csv',
    '--errors', 'samples/output/debug_errors.csv'
])
print(f"Exit code: {result.exit_code}")
print(result.output) 