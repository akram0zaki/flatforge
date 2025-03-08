"""
Base processor module for FlatForge.

This module contains the abstract base class for processors.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set, Tuple, Callable, TextIO
import os

from flatforge.core import FileFormat, ProcessingResult, ValidationError, ParsedRecord, ProcessorError
from flatforge.rules import GlobalRule, GLOBAL_RULES
from flatforge.parsers import Parser


class Processor(ABC):
    """
    Abstract base class for processors.
    
    A processor defines the common methods which every processor must implement.
    """
    
    def __init__(self, file_format: FileFormat):
        """
        Initialize a processor.
        
        Args:
            file_format: The file format to process
        """
        self.file_format = file_format
        self.global_rules: List[GlobalRule] = []
        
        # Create global rules
        self._create_global_rules()
    
    def _create_global_rules(self) -> None:
        """
        Create global rules from the file format.
        
        This method creates global rules based on the configuration in the file format.
        """
        # Global rules can be defined at the file format level
        global_rules_config = getattr(self.file_format, 'global_rules', [])
        
        for rule_config in global_rules_config:
            if 'type' not in rule_config:
                continue
                
            rule_type = rule_config['type']
            rule_name = rule_config.get('name', rule_type)
            rule_params = rule_config.get('params', {})
            
            # Create the rule
            if rule_type in GLOBAL_RULES:
                rule_class = GLOBAL_RULES[rule_type]
                self.global_rules.append(rule_class(rule_name, rule_params))
    
    @abstractmethod
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
        pass
        
    def process_chunked(self, input_file: str, output_file: Optional[str] = None, error_file: Optional[str] = None,
                       chunk_size: int = 10000, progress_callback: Optional[Callable[[int, int], None]] = None) -> ProcessingResult:
        """
        Process a file in chunks for better memory efficiency with large files.
        
        Args:
            input_file: Path to the input file
            output_file: Optional path to the output file
            error_file: Optional path to the error file
            chunk_size: Number of records to process in each chunk
            progress_callback: Optional callback function that receives (processed_records, total_records)
            
        Returns:
            A ProcessingResult object
            
        Raises:
            ProcessorError: If the file cannot be processed
        """
        result = ProcessingResult()
        
        try:
            # Create a parser
            parser = Parser.create_parser(self.file_format)
            
            # Estimate the total number of records for progress reporting
            total_records = self._estimate_total_records(input_file)
            processed_records = 0
            
            # Open the output and error files
            out_file = None
            if output_file:
                out_file = open(output_file, 'w', encoding=self.file_format.encoding)
                
            error_file_obj = None
            if error_file:
                error_file_obj = open(error_file, 'w', encoding=self.file_format.encoding)
                
            try:
                # Process the file in chunks
                chunk = []
                for record in parser.parse_file(input_file):
                    # Apply global rules
                    for rule in self.global_rules:
                        rule.process_record(record)
                        
                    # Add the record to the current chunk
                    chunk.append(record)
                    
                    # Process the chunk if it's full
                    if len(chunk) >= chunk_size:
                        self._process_chunk(chunk, out_file, error_file_obj, result)
                        processed_records += len(chunk)
                        chunk = []
                        
                        # Report progress
                        if progress_callback:
                            progress_callback(processed_records, total_records)
                            
                # Process any remaining records
                if chunk:
                    self._process_chunk(chunk, out_file, error_file_obj, result)
                    processed_records += len(chunk)
                    
                    # Report final progress
                    if progress_callback:
                        progress_callback(processed_records, total_records)
                        
                # Finalize global rules
                for rule in self.global_rules:
                    errors = rule.finalize()
                    if errors:
                        result.error_count += len(errors)
                        result.errors.extend(errors)
                        
            finally:
                if out_file:
                    out_file.close()
                if error_file_obj:
                    error_file_obj.close()
                    
        except Exception as e:
            raise ProcessorError(f"Error processing file: {str(e)}")
            
        return result
    
    def _process_chunk(self, chunk: List[ParsedRecord], out_file: Optional[TextIO], 
                      error_file_obj: Optional[TextIO], result: ProcessingResult) -> None:
        """
        Process a chunk of records.
        
        Args:
            chunk: List of records to process
            out_file: Output file object or None
            error_file_obj: Error file object or None
            result: ProcessingResult object to update
        """
        # Update the total record count
        result.total_records += len(chunk)
        
        # Process each record in the chunk
        for record in chunk:
            self._process_record(record, out_file, error_file_obj, result)
            
            # Exit on first error if configured to do so
            if self.file_format.exit_on_first_error and result.error_count > 0:
                break
    
    @abstractmethod
    def _process_record(self, record: ParsedRecord, out_file: Optional[TextIO], 
                       error_file_obj: Optional[TextIO], result: ProcessingResult) -> None:
        """
        Process a single record.
        
        Args:
            record: Record to process
            out_file: Output file object or None
            error_file_obj: Error file object or None
            result: ProcessingResult object to update
        """
        pass
    
    def _estimate_total_records(self, input_file: str) -> int:
        """
        Estimate the total number of records in a file.
        
        This method estimates the total number of records in a file for progress reporting.
        The estimation is based on file size and average line length.
        
        Args:
            input_file: Path to the input file
            
        Returns:
            Estimated number of records
        """
        try:
            # Get file size
            file_size = os.path.getsize(input_file)
            
            # Sample the file to get average line length
            with open(input_file, 'r', encoding=self.file_format.encoding) as f:
                # Read up to 100 lines for sampling
                lines = []
                for _ in range(100):
                    line = f.readline()
                    if not line:
                        break
                    lines.append(line)
                
                if not lines:
                    return 0
                
                # Calculate average line length
                avg_line_length = sum(len(line) for line in lines) / len(lines)
                
                # Estimate total records
                estimated_records = int(file_size / avg_line_length)
                
                return max(1, estimated_records)  # Ensure at least 1 record
        except Exception:
            # If estimation fails, return a default value
            return 1000 