"""
Debug script for testing the CLI with chunked processing.

This script allows testing the CLI with chunked processing in your IDE.
"""

import sys
from flatforge.cli.main import main

if __name__ == "__main__":
    # Set up the arguments for chunked processing
    sys.argv = [
        "flatforge",
        "validate",
        "--config", "samples/config/large_file_config.yaml",
        "--input", "samples/input/large_file.csv",
        "--output", "samples/output/chunked_output.csv",
        "--errors", "samples/output/chunked_errors.csv",
        "--chunk-size", "1000",
        "--show-progress"
    ]
    
    # Call the CLI function
    main() 