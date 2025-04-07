# FlatForge

A generic, modular, and extensible library to validate flat files of fixed length or delimited format.
This project was created with help of Claude Sonnet 3.7.

## Features

- Validate flat files against predefined schemas
- Transform flat files from one format to another
- Support for fixed-length and delimited file formats
- Extensible rule system for validation and transformation
- Global rules for cross-record validation (count, sum, checksum, uniqueness)
- CLI interface for easy integration into workflows
- Support for multi-section files (header, body, footer)
- Comprehensive error reporting with detailed error messages
- Efficient processing of large files (>1GB) with chunked processing and progress reporting
- Configuration validation with JSON schema
- Support for various validation rules (required, numeric, string length, regex, date, choice)
- Support for various transformation rules (trim, case, pad, date format, substring, replace)
- Support for value mapping and masking
- Support for GUID generation and Luhn algorithm
- Extensible architecture with support for custom rules and processors

## Installation

```bash
pip install flatforge
```

## Quick Start

### Command Line Interface

```bash
# Validate a file against a schema
flatforge validate --config schema.yaml --input data.csv --output valid.csv --errors errors.csv

# Convert a file from one format to another
flatforge convert --config mapping.yaml --input data.csv --output converted.txt

# Process a large file with chunked processing and progress reporting
flatforge validate --config schema.yaml --input large_data.csv --output valid.csv --errors errors.csv --chunk-size 10000 --show-progress

# Validate a configuration file against the JSON schema
flatforge validate-config --config schema.yaml
```

### Programmatic Usage

```python
from flatforge.core import FileFormat
from flatforge.processors import ValidationProcessor, ConversionProcessor, CounterProcessor
from flatforge.validators import ConfigValidator

# Validate configuration file against JSON schema
validator = ConfigValidator()
validator.validate_file("schema.yaml")

# Load configuration with validation enabled
file_format = FileFormat.from_yaml("schema.yaml", validate=True)

# Create a validation processor
validation_processor = ValidationProcessor(file_format)
result = validation_processor.process("data.csv", "valid.csv", "errors.csv")
print(f"Processed {result.total_records} records with {result.error_count} errors")

# Create a conversion processor
output_format = FileFormat.from_yaml("output_schema.yaml", validate=True)
conversion_processor = ConversionProcessor(file_format, output_format)
result = conversion_processor.process("data.csv", "converted.txt", "errors.csv")
print(f"Converted {result.total_records} records with {result.error_count} errors")

# Create a counter processor
counter_processor = CounterProcessor(file_format)
result = counter_processor.process("data.csv", "counts.txt")
print(f"Total records: {result.total_records}")

# Process a large file in chunks with progress reporting
def update_progress(processed, total):
    print(f"Progress: {processed}/{total} records ({int(100 * processed / total)}%)")

result = validation_processor.process_chunked(
    "large_data.csv", 
    "valid.csv", 
    "errors.csv", 
    chunk_size=10000, 
    progress_callback=update_progress
)
print(f"Processed {result.total_records} records with {result.error_count} errors")
```

## Documentation

### User Documentation
- [User Guide](https://github.com/akram0zaki/flatforge/blob/master/docs/user_guide/README.md): How to use FlatForge
- [Configuration Guide](https://github.com/akram0zaki/flatforge/blob/master/docs/user_guide/configuration_guide.md): Detailed explanation of configuration file structure and options
- [Configuration Validation](https://github.com/akram0zaki/flatforge/blob/master/docs/user_guide/configuration_validation.md): Guide to configuration validation using JSON schema
- [Rules Guide](https://github.com/akram0zaki/flatforge/blob/master/docs/user_guide/rules_guide.md): Comprehensive guide to all validation rules
- [Transformation Rules](https://github.com/akram0zaki/flatforge/blob/master/docs/user_guide/transformation_rules.md): Guide to transformation rules and their usage

### Developer Documentation
- [Developer Guide](https://github.com/akram0zaki/flatforge/blob/master/docs/developer_guide/README.md): How to extend FlatForge
- [Architecture](https://github.com/akram0zaki/flatforge/blob/master/docs/architecture/README.md): Design and architecture of FlatForge
- [Testing Guide](https://github.com/akram0zaki/flatforge/blob/master/docs/testing/README.md): How to test FlatForge and write new tests
- [Error Handling](https://github.com/akram0zaki/flatforge/blob/master/docs/testing/error_handling.md): Guide to error handling and debugging

## Changelog

See the [CHANGELOG.md](https://github.com/akram0zaki/flatforge/blob/master/CHANGELOG.md) file for details on the changes made in each release.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](https://github.com/akram0zaki/flatforge/blob/master/CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## Author

- Akram Zaki (azpythonprojects@gmail.com)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/akram0zaki/flatforge/blob/master/LICENSE) file for details. 