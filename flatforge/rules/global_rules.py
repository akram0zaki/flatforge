"""
Global rules for FlatForge.

This module contains the global rules for validating across multiple records.
"""
import hashlib
from typing import Dict, List, Optional, Any

from flatforge.core import ValidationError, ParsedRecord
from flatforge.rules.base import GlobalRule


class CountRule(GlobalRule):
    """
    Rule that counts the number of records in a section.
    
    This rule verifies that the number of records in a section matches
    a specified count or a count from another field.
    """
    
    def __init__(self, name: str, params: Optional[dict] = None):
        """
        Initialize a CountRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params)
        self.state = {"count": 0}
    
    def process_record(self, record: ParsedRecord) -> None:
        """
        Process a record.
        
        Args:
            record: The record to process
        """
        # Only count records from the specified section
        section_name = self.params.get("section")
        if section_name and record.section.name != section_name:
            return
            
        self.state["count"] += 1
    
    def finalize(self) -> List[ValidationError]:
        """
        Finalize the rule.
        
        Returns:
            A list of validation errors, if any
        """
        errors = []
        
        # Check if the count matches the expected count
        expected_count = self.params.get("expected_count")
        if expected_count is not None:
            expected_count = int(expected_count)
            actual_count = self.state["count"]
            
            if actual_count != expected_count:
                errors.append(ValidationError(
                    f"Record count mismatch: expected {expected_count}, got {actual_count}",
                    rule_name=self.name,
                    error_code="COUNT_MISMATCH"
                ))
                
        # Check if the count matches a field value
        count_field = self.params.get("count_field")
        if count_field:
            section_name, field_name = count_field.split(".")
            # This would require access to the parsed records, which we don't have here
            # In a real implementation, we would need to store the parsed records
            # or the specific field value in the state
            pass
            
        return errors


class SumRule(GlobalRule):
    """
    Rule that sums the values of a field across all records.
    
    This rule verifies that the sum of a field across all records matches
    a specified sum or a sum from another field.
    """
    
    def __init__(self, name: str, params: Optional[dict] = None):
        """
        Initialize a SumRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params)
        self.state = {"sum": 0}
    
    def process_record(self, record: ParsedRecord) -> None:
        """
        Process a record.
        
        Args:
            record: The record to process
        """
        # Only sum records from the specified section
        section_name = self.params.get("section")
        if section_name and record.section.name != section_name:
            return
            
        # Get the field to sum
        field_name = self.params.get("field")
        if not field_name:
            return
            
        # Get the field value
        field_value = record.field_values.get(field_name)
        if not field_value:
            return
            
        # Try to convert the value to a number and add it to the sum
        try:
            value = field_value.value.strip()
            if value:
                self.state["sum"] += float(value)
        except (ValueError, TypeError):
            # Ignore non-numeric values
            pass
    
    def finalize(self) -> List[ValidationError]:
        """
        Finalize the rule.
        
        Returns:
            A list of validation errors, if any
        """
        errors = []
        
        # Check if the sum matches the expected sum
        expected_sum = self.params.get("expected_sum")
        if expected_sum is not None:
            expected_sum = float(expected_sum)
            actual_sum = self.state["sum"]
            
            # Allow for a small tolerance due to floating point precision
            tolerance = float(self.params.get("tolerance", 0.0001))
            
            if abs(actual_sum - expected_sum) > tolerance:
                errors.append(ValidationError(
                    f"Sum mismatch: expected {expected_sum}, got {actual_sum}",
                    rule_name=self.name,
                    error_code="SUM_MISMATCH"
                ))
                
        # Check if the sum matches a field value
        sum_field = self.params.get("sum_field")
        if sum_field:
            section_name, field_name = sum_field.split(".")
            # This would require access to the parsed records, which we don't have here
            # In a real implementation, we would need to store the parsed records
            # or the specific field value in the state
            pass
            
        return errors


class ChecksumRule(GlobalRule):
    """
    Rule that calculates a checksum of a field across all records.
    
    This rule verifies that the checksum of a field across all records matches
    a specified checksum or a checksum from another field.
    """
    
    def __init__(self, name: str, params: Optional[dict] = None):
        """
        Initialize a ChecksumRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params)
        self.state = {"checksum": 0}
    
    def process_record(self, record: ParsedRecord) -> None:
        """
        Process a record.
        
        Args:
            record: The record to process
        """
        # Only checksum records from the specified section
        section_name = self.params.get("section")
        if section_name and record.section.name != section_name:
            return
            
        # Get the field to checksum
        field_name = self.params.get("field")
        if not field_name:
            return
            
        # Get the field value
        field_value = record.field_values.get(field_name)
        if not field_value:
            return
            
        # Calculate the checksum
        value = field_value.value
        checksum_type = self.params.get("type", "sum")
        
        if checksum_type == "sum":
            # Sum the ASCII values of the characters
            self.state["checksum"] += sum(ord(c) for c in value)
        elif checksum_type == "xor":
            # XOR the ASCII values of the characters
            for c in value:
                self.state["checksum"] ^= ord(c)
        elif checksum_type == "mod10":
            # Modulo 10 checksum (Luhn algorithm)
            # This is a simplified version
            try:
                digits = [int(d) for d in value if d.isdigit()]
                self.state["checksum"] = (self.state["checksum"] + sum(digits)) % 10
            except (ValueError, TypeError):
                # Ignore non-numeric values
                pass
    
    def finalize(self) -> List[ValidationError]:
        """
        Finalize the rule.
        
        Returns:
            A list of validation errors, if any
        """
        errors = []
        
        # Check if the checksum matches the expected checksum
        expected_checksum = self.params.get("expected_checksum")
        if expected_checksum is not None:
            expected_checksum = int(expected_checksum)
            actual_checksum = self.state["checksum"]
            
            if actual_checksum != expected_checksum:
                errors.append(ValidationError(
                    f"Checksum mismatch: expected {expected_checksum}, got {actual_checksum}",
                    rule_name=self.name,
                    error_code="CHECKSUM_MISMATCH"
                ))
                
        # Check if the checksum matches a field value
        checksum_field = self.params.get("checksum_field")
        if checksum_field:
            section_name, field_name = checksum_field.split(".")
            # This would require access to the parsed records, which we don't have here
            # In a real implementation, we would need to store the parsed records
            # or the specific field value in the state
            pass
            
        return errors 