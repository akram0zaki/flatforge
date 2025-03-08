"""
Validation processor module for FlatForge.

This module contains the validation processor class.
"""
import csv
from typing import Dict, List, Optional, TextIO

from flatforge.core import (
    FileFormat, ProcessingResult, ValidationError, ParsedRecord, ProcessorError
)
from flatforge.parsers import Parser
from flatforge.processors.base import Processor


class ValidationProcessor(Processor):
    """
    Processor that validates a file against a schema.
    
    This processor validates an input file against a schema and writes valid
    records to an output file and invalid records to an error file.
    """
    
    def process(self, input_file: str, output_file: str, error_file: Optional[str] = None) -> ProcessingResult:
        """
        Process a file.
        
        Args:
            input_file: Path to the input file
            output_file: Path to the output file
            error_file: Optional path to the error file
            
        Returns:
            A ProcessingResult object
            
        Raises:
            ProcessorError: If the file cannot be processed
        """
        result = ProcessingResult()
        
        try:
            # Create a parser
            parser = Parser.create_parser(self.file_format)
            
            # Open the output and error files
            with open(output_file, 'w', encoding=self.file_format.encoding) as out_file:
                error_file_obj = None
                if error_file:
                    error_file_obj = open(error_file, 'w', encoding=self.file_format.encoding)
                    
                try:
                    # Process the file
                    for record in parser.parse_file(input_file):
                        result.total_records += 1
                        
                        # Apply global rules
                        for rule in self.global_rules:
                            rule.process_record(record)
                            
                        # Write the record to the appropriate file
                        if record.is_valid:
                            result.valid_records += 1
                            self._write_record(out_file, record)
                        else:
                            result.error_count += len([e for fv in record.field_values.values() for e in fv.errors])
                            result.errors.extend([e for fv in record.field_values.values() for e in fv.errors])
                            
                            if error_file_obj:
                                self._write_error_record(error_file_obj, record)
                                
                            # Exit on first error if configured to do so
                            if self.file_format.exit_on_first_error:
                                break
                                
                    # Finalize global rules
                    for rule in self.global_rules:
                        errors = rule.finalize()
                        if errors:
                            result.error_count += len(errors)
                            result.errors.extend(errors)
                            
                finally:
                    if error_file_obj:
                        error_file_obj.close()
                        
        except Exception as e:
            raise ProcessorError(f"Error processing file: {str(e)}")
            
        return result
    
    def _process_record(self, record: ParsedRecord, out_file: Optional[TextIO], 
                       error_file_obj: Optional[TextIO], result: ProcessingResult) -> None:
        """
        Process a single record for chunked processing.
        
        Args:
            record: Record to process
            out_file: Output file object or None
            error_file_obj: Error file object or None
            result: ProcessingResult object to update
        """
        # Write the record to the appropriate file
        if record.is_valid:
            result.valid_records += 1
            if out_file:
                self._write_record(out_file, record)
        else:
            result.error_count += len([e for fv in record.field_values.values() for e in fv.errors])
            result.errors.extend([e for fv in record.field_values.values() for e in fv.errors])
            
            if error_file_obj:
                self._write_error_record(error_file_obj, record)
    
    def _write_record(self, file_obj: TextIO, record: ParsedRecord) -> None:
        """
        Write a record to a file.
        
        Args:
            file_obj: File object to write to
            record: Record to write
        """
        # Write the raw data without adding an extra newline
        raw_data = record.raw_data.rstrip(self.file_format.newline)
        file_obj.write(raw_data + self.file_format.newline)
    
    def _write_error_record(self, file_obj: TextIO, record: ParsedRecord) -> None:
        """
        Write an error record to a file.
        
        Args:
            file_obj: File object to write to
            record: Record to write
        """
        # Write the raw data and the errors
        file_obj.write(f"Record {record.record_number} in section {record.section.name}:{self.file_format.newline}")
        file_obj.write(f"Raw data: {record.raw_data}{self.file_format.newline}")
        
        # Write the errors
        for field_name, field_value in record.field_values.items():
            for error in field_value.errors:
                file_obj.write(f"Error: {str(error)}{self.file_format.newline}")
                
        file_obj.write(self.file_format.newline) 