# Changelog

All notable changes to the FlatForge project will be documented in this file.

## [Unreleased]

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
- Refactored validation rules into individual modules for better modularity
- Enhanced NumericRule documentation to clearly describe min_value, max_value, and decimal_precision parameters
- Improved validation rule organization by moving each rule to its own file

### Fixed
- Bug in date format validation that caused incorrect error messages
- Issue with string length validation when processing non-ASCII characters
- Performance issue when processing large files with multiple validation rules

## [0.3.2] - 2025-04-01

### Fixed
- Fixed ConversionProcessor to properly accept mapping configuration parameter
- Enhanced CLI 'convert' command to correctly process mappings between formats
- Improved compatibility between CLI interface and processor implementations

### Changed
- Updated validation and conversion error reporting for better readability
- Enhanced CLI command output with more consistent formatting

## [0.3.1] - 2025-03-31

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
- Refactored validation rules into individual modules for better modularity
- Enhanced NumericRule documentation to clearly describe min_value, max_value, and decimal_precision parameters
- Improved validation rule organization by moving each rule to its own file

### Fixed
- Bug in date format validation that caused incorrect error messages
- Issue with string length validation when processing non-ASCII characters
- Performance issue when processing large files with multiple validation rules

## [0.3.0] - 2025-03-16

### Added
- Comprehensive testing documentation in the `docs/testing` directory
  - Main testing guide with overview of testing infrastructure
  - Detailed unit testing documentation with best practices
  - Error handling testing guide with sample files explanation
  - CLI testing documentation with command examples
  - Sample files documentation detailing test data structure
  - Debugging guide for library development
- Debug scripts for local development and troubleshooting
  - `debug_main.py` for core processing functionality
  - `debug_cli.py` for CLI interface testing
  - `debug_cli_chunked.py` for chunked processing testing
  - `debug_cli_convert.py` for file format conversion testing
  - `debug_cli_click.py` for Click-based CLI testing
- Development mode installation instructions for library debugging
- Global rules system for validating relationships between records
- Support for global rules that can alter field values (e.g., inserting calculated sums or counts)
- Global rules for cross-record validation:
  - Count validation for record counts
  - Sum validation for numeric field totals
  - Uniqueness validation for fields that must be unique
- Ability to validate uniqueness of fields or combinations of fields across records
- Documentation for global rules in the user guide
- Sample configuration and test script for global rules
- Comprehensive rules guide documenting all rule types and their parameters

### Changed
- Renamed `abort_after_n_errors` to `abort_after_n_failed_records` to better reflect its purpose
- Updated validation processor to track failed records separately from error count
- Modified abort logic to count failed records instead of individual errors
- Added unit tests for the abort functionality
- Improved documentation with references to the new rules guide
- Fixed CLI entry point in setup.py to ensure proper command execution

## [0.2.2] - 2025-03-09

### Fixed
- Fixed CLI entry point in setup.py to ensure proper command execution
- Resolved issue with FileFormat.from_yaml method in CLI implementation
- Improved error handling in validation processor
- Enhanced CLI output with more detailed processing statistics

## [0.2.1] - 2025-03-08

### Fixed
- Fixed documentation links in README.md to use absolute URLs for PyPI compatibility

## [0.2.0] - 2025-03-08

### Added
- Renamed library from FlatMagic to FlatForge
- Chunked processing for large files (>1GB) with configurable chunk size
- Progress reporting for long-running operations
- CLI options `--chunk-size` and `--show-progress` for all commands
- Memory-efficient processing of large datasets
- Example script `samples/large_file_processing.py` demonstrating chunked processing
- Documentation for large file processing in the user guide

### Changed
- Updated base `Processor` class to support chunked processing
- Modified `ValidationProcessor`, `ConversionProcessor`, and `CounterProcessor` to implement chunked processing
- Improved error handling for file operations
- Updated CLI interface to support new options
- Enhanced documentation with examples of chunked processing

### Fixed
- Fixed handling of None values for output files
- Improved newline handling in output files
- Fixed unit tests to work with the new chunked processing feature

## [0.1.0] - 2025-03-08

### Added
- Initial release of FlatForge (formerly FlatMagic)
- Support for fixed-length and delimited file formats
- Validation, conversion, and counting of records
- CLI interface for easy integration into workflows
- Comprehensive documentation
- Unit tests for core functionality

## Authors
- Akram Zaki (azpythonprojects@gmail.com, [@akram0zaki](https://github.com/akram0zaki)) 