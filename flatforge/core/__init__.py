"""
Core module for FlatForge.

This module contains the core components of the FlatForge library.
"""

from flatforge.core.exceptions import (
    FlatForgeError, ConfigError, ParserError, ValidationError, 
    TransformationError, ProcessorError
)
from flatforge.core.models import (
    FileType, SectionType, Field, Record, Section, FileFormat,
    FieldValue, ParsedRecord, ProcessingResult
)

__all__ = [
    'FlatForgeError', 'ConfigError', 'ParserError', 'ValidationError',
    'TransformationError', 'ProcessorError', 'FileType', 'SectionType',
    'Field', 'Record', 'Section', 'FileFormat', 'FieldValue',
    'ParsedRecord', 'ProcessingResult'
] 