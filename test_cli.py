"""
Test script for the FlatForge CLI.
"""
import os
import sys
import traceback
from flatforge.parsers import ConfigParser
from flatforge.processors import ValidationProcessor

def main():
    """Test the FlatForge CLI functionality."""
    try:
        # Parse the configuration
        config_path = 'samples/config/employee_csv_no_identifier.yaml'
        input_path = 'samples/input/employee_data_no_identifier.csv'
        output_path = 'samples/output/valid.csv'
        error_path = 'samples/output/errors.csv'
        
        print(f"Parsing configuration: {config_path}")
        config_parser = ConfigParser.from_file(config_path)
        file_format = config_parser.parse()
        
        print(f"Creating processor")
        processor = ValidationProcessor(file_format)
        
        print(f"Processing file: {input_path}")
        result = processor.process(input_path, output_path, error_path)
        
        print(f"Total records: {result.total_records}")
        print(f"Valid records: {result.valid_records}")
        print(f"Error count: {result.error_count}")
        
        print(f"Output written to: {output_path}")
        print(f"Errors written to: {error_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
    
if __name__ == '__main__':
    main() 