"""
Exceptions module for FlatForge.

This module contains all the custom exceptions used throughout the FlatForge library.
"""


class FlatForgeError(Exception):
    """Base exception for all FlatForge errors."""
    pass


class ConfigError(FlatForgeError):
    """Exception raised for configuration errors."""
    pass


class ParserError(FlatForgeError):
    """Exception raised for parsing errors."""
    pass


class ValidationError(FlatForgeError):
    """Exception raised for validation errors."""
    
    def __init__(self, message, field_name=None, value=None, rule_name=None):
        """
        Initialize a validation error.
        
        Args:
            message: The error message
            field_name: The name of the field that failed validation
            value: The value that failed validation
            rule_name: The name of the rule that failed
        """
        self.field_name = field_name
        self.value = value
        self.rule_name = rule_name
        
        # Build a detailed error message
        detailed_message = message
        if field_name:
            detailed_message = f"Field '{field_name}': {detailed_message}"
        if value is not None:
            detailed_message = f"{detailed_message} (value: '{value}')"
        if rule_name:
            detailed_message = f"{detailed_message} [rule: {rule_name}]"
            
        super().__init__(detailed_message)


class TransformationError(FlatForgeError):
    """Exception raised for transformation errors."""
    pass


class ProcessorError(FlatForgeError):
    """Exception raised for processor errors."""
    pass 