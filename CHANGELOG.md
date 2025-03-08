# Changelog

All notable changes to the FlatForge library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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