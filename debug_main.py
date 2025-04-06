"""
Debug script for the main entry point.

This script is used to debug the main entry point of the CLI.
"""

import sys
from flatforge.cli.main import main

if __name__ == '__main__':
    sys.exit(main()) 