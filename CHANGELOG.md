# Changelog

All notable changes to the FlatForge project will be documented in this file.

## [Unreleased]

### Added

### Changed

### Fixed

## [0.3.1] - 2025-03-30

### Added
- Extended checksum validation with support for multiple algorithms:
  - SHA256 algorithm for enhanced security
  - Multi-column checksum validation
  - Row-based checksum validation
  - Support for sum, xor, mod10, md5, and SHA256 algorithms
- GUID validation rule to validate UUIDs against RFC4122 specifications
- GUID generation transformer to create valid UUIDs in output files
- Value resolver transformer for complex value mappings
- Luhn algorithm validation for credit card number verification
- Field masking transformer with specific support for credit card masking
- Encoding transformation for converting between different file encodings
- Global rules for cross-record validation:
  - Count validation for record counts
  - Sum validation for numeric field totals
  - Uniqueness validation for fields that must be unique
- File-level settings for input and output encoding specification
- Comprehensive documentation for all new features
- Sample configuration files demonstrating new features
- Improved test script with standardized naming convention (yyyyMMdd format)
- Enhanced CLI documentation and examples

### Changed
- Improved error handling for validation rules
- Enhanced unit test coverage for all validation types
- Optimized checksum calculation performance
- Updated documentation structure for better organization
- Refactored transformation pipeline for better extensibility

### Fixed
- Bug in date format validation that caused incorrect error messages
- Issue with string length validation when processing non-ASCII characters
- Performance issue when processing large files with multiple validation rules

## [0.3.0] - 2023-09-15

### Added
- Support for fixed-length file format
- Support for delimited file format
- Basic validation rules: required field, string length, numeric range, date format
- Basic transformation rules: trim, case conversion, date format conversion
- CLI for validating and transforming files
- Documentation and examples

### Changed
- Improved error handling
- Enhanced CLI interface

## [0.1.0] - 2023-06-30

### Added
- Initial release
- Basic file parsing functionality
- Simple validation rules
- Command line interface basics

## Authors
- Akram Zaki (azpythonprojects@gmail.com, [@akram0zaki](https://github.com/akram0zaki)) 