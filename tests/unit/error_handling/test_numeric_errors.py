"""
Unit tests for numeric value error handling.

This module contains unit tests for handling numeric value errors in FlatForge.
"""
import os
import unittest
from flatforge.core.models import FileFormat, FileType, Section, Record, Field, SectionType
from flatforge.processors.validation import ValidationProcessor


class TestNumericErrors(unittest.TestCase):
    """Test case for numeric value errors."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a test file format
        self._create_test_file_format()
        
        # Create a test file with numeric value errors
        self.test_input_file = "test_numeric_errors.csv"
        with open(self.test_input_file, "w") as f:
            f.write("H,BATCH001,20230101120000\n")
            f.write("D,ABC1,John Smith,19800101,US,75000.00,1000,Jane Doe\n")  # Non-numeric employee_id
            f.write("D,1002,Alice Johnson,19850215,CA,80K,1000,Jane Doe\n")  # Non-numeric salary
            f.write("D,1003,Bob Williams,19900320,UK,65,000.00,1001,John Smith\n")  # Incorrectly formatted number
            f.write("D,1004,Carol Brown,19950425,AU,-60000.00,1001,John Smith\n")  # Negative salary (if not allowed)
            f.write("D,1005,David Miller,19881130,DE,70000.00,MANAGER,Alice Johnson\n")  # Non-numeric manager_id
            f.write("F,350000.00,FIVE\n")  # Non-numeric employee_count
        
        # Output files
        self.test_output_file = "test_numeric_valid.csv"
        self.test_error_file = "test_numeric_errors.txt"
        
    def tearDown(self):
        """Clean up after tests."""
        # Remove test files
        for file in [self.test_input_file, self.test_output_file, self.test_error_file]:
            if os.path.exists(file):
                os.remove(file)
                
    def _create_test_file_format(self):
        """Create a test file format for CSV files with numeric validation."""
        # Create fields for the header record
        header_fields = [
            Field(name="record_type", position=0, rules=[{"type": "choice", "params": {"choices": ["H"]}}]),
            Field(name="batch_reference", position=1, rules=[{"type": "required"}]),
            Field(name="batch_timestamp", position=2, rules=[
                {"type": "required"},
                {"type": "date", "params": {"format": "%Y%m%d%H%M%S"}}
            ])
        ]
        
        # Create fields for the body record
        body_fields = [
            Field(name="record_type", position=0, rules=[{"type": "choice", "params": {"choices": ["D"]}}]),
            Field(name="employee_id", position=1, rules=[
                {"type": "required"}, 
                {"type": "numeric"}
            ]),
            Field(name="employee_name", position=2, rules=[{"type": "required"}]),
            Field(name="date_of_birth", position=3, rules=[
                {"type": "date", "params": {"format": "%Y%m%d"}}
            ]),
            Field(name="country_code", position=4, rules=[
                {"type": "string_length", "params": {"min_length": 2, "max_length": 2}}
            ]),
            Field(name="salary", position=5, rules=[
                {"type": "numeric", "params": {"min_value": 0, "decimal_precision": 2}}
            ]),
            Field(name="manager_id", position=6, rules=[{"type": "numeric"}]),
            Field(name="manager_name", position=7)
        ]
        
        # Create fields for the footer record
        footer_fields = [
            Field(name="record_type", position=0, rules=[{"type": "choice", "params": {"choices": ["F"]}}]),
            Field(name="total_salary", position=1, rules=[
                {"type": "required"}, 
                {"type": "numeric", "params": {"min_value": 0, "decimal_precision": 2}}
            ]),
            Field(name="employee_count", position=2, rules=[
                {"type": "required"}, 
                {"type": "numeric", "params": {"min_value": 0}}
            ])
        ]
        
        # Create records
        header_record = Record(name="header_record", fields=header_fields)
        body_record = Record(name="body_record", fields=body_fields)
        footer_record = Record(name="footer_record", fields=footer_fields)
        
        # Create sections
        header_section = Section(
            name="header",
            type=SectionType.HEADER,
            record=header_record,
            min_records=1,
            max_records=1
        )
        
        body_section = Section(
            name="body",
            type=SectionType.BODY,
            record=body_record
        )
        
        footer_section = Section(
            name="footer",
            type=SectionType.FOOTER,
            record=footer_record,
            min_records=1,
            max_records=1
        )
        
        # Create file format
        self.file_format = FileFormat(
            name="Test CSV Format",
            type=FileType.DELIMITED,
            sections=[header_section, body_section, footer_section],
            delimiter=",",
            quote_char='"',
            escape_char=None,
            newline="\n",
            encoding="utf-8",
            skip_blank_lines=True,
            exit_on_first_error=False,
            abort_after_n_failed_records=-1
        )
        
    def test_numeric_errors(self):
        """Test handling of numeric value errors."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.test_input_file, self.test_output_file, self.test_error_file)
        
        # Check the results
        self.assertEqual(result.total_records, 7)  # Header + 5 body records + footer
        self.assertEqual(result.valid_records, 2)  # Header and footer
        self.assertEqual(result.failed_records, 5)  # All body records have numeric errors
        self.assertGreater(result.error_count, 0)  # Should have errors
        
        # Check that the error file exists and has content
        self.assertTrue(os.path.exists(self.test_error_file))
        with open(self.test_error_file, "r") as f:
            error_content = f.read()
            # Check for numeric error indicators in the content
            self.assertTrue(any(term in error_content.lower() for term in ["numeric", "number"]))
            self.assertIn("ABC1", error_content)  # Should mention the invalid value
            self.assertIn("80K", error_content)  # Should mention the invalid value
            self.assertIn("FIVE", error_content)  # Should mention the invalid value
            
        # Check that the output file exists and has valid records
        self.assertTrue(os.path.exists(self.test_output_file))
        with open(self.test_output_file, "r") as f:
            output_content = f.read()
            self.assertIn("H,BATCH001,20230101120000", output_content)  # Header should be valid
            
            # Invalid records should not be in the output
            self.assertNotIn("ABC1", output_content)
            self.assertNotIn("80K", output_content)
            self.assertNotIn("FIVE", output_content)
            
    def test_error_details(self):
        """Test that error details are correctly captured."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.test_input_file, self.test_output_file, self.test_error_file)
        
        # Check that errors have detailed information
        numeric_errors = [e for e in result.errors if "numeric" in str(e).lower()]
        self.assertGreater(len(numeric_errors), 0)  # Should have numeric errors
        
        for error in numeric_errors:
            error_str = str(error)
            self.assertIn("numeric", error_str.lower())  # Should mention it's a numeric error
            
            # Check if the error message contains the field name and record number
            self.assertTrue(
                any(field in error_str for field in ["employee_id", "salary", "manager_id", "employee_count"]) or
                "record" in error_str.lower()
            )


if __name__ == "__main__":
    unittest.main() 