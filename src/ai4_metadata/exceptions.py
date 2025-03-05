"""Custom exceptions for the metadata schema validation tool."""

import os
import pathlib
import typing

import jsonschema.exceptions


class BaseExceptionError(Exception):
    """Base exception for the metadata schema validation tool."""

    message = "An error occurred."


class FileNotFoundError(BaseExceptionError):
    """Exception raised when a file is not found."""

    message = "File '{f}' not found."

    def __init__(self, f: typing.Union[str, pathlib.Path]):
        """Initialize the exception."""
        self.f = f
        super().__init__(self.message.format(f=f))


class InvalidFileError(BaseExceptionError):
    """Exception raised when a file is invalid."""

    message = "Error loading file '{f}': {e}"

    def __init__(self, f: typing.Union[str, pathlib.Path], e: Exception):
        """Initialize the exception."""
        self.f = f
        self.e = e
        super().__init__(self.message.format(f=f, e=e))


class InvalidJSONError(InvalidFileError):
    """Exception raised when a JSON file is invalid."""

    message = "Error loading JSON file '{f}': {e}"


class InvalidYAMLError(InvalidFileError):
    """Exception raised when a JSON/YAML file is invalid."""

    message = "Error loading YAML file '{f}': {e}"


class InvalidSchemaError(BaseExceptionError):
    """Exception raised when a schema is invalid."""

    message = "Schema file '{schema_file}' is invalid: {error}"

    def __init__(self, schema_file: typing.Union[str, pathlib.Path], error: str):
        """Initialize the exception."""
        super().__init__(self.message.format(schema_file=schema_file, error=error))


class SchemaValidationError(BaseExceptionError):
    """Exception raised when a schema is invalid."""

    message = "Error validating schema '{schema_file}': {e}"

    def __init__(self, schema_file: typing.Union[str, pathlib.Path], e: Exception):
        """Initialize the exception."""
        self.e = e
        super().__init__(self.message.format(schema_file=schema_file, e=e))


class MetadataValidationError(BaseExceptionError):
    """Exception raised when a metadata file is invalid."""

    message = "Error validating instance '{instance_file}': {e}"

    def __init__(
        self,
        instance_file: typing.Union[str, pathlib.Path],
        e: jsonschema.exceptions.ValidationError,
    ):
        """Initialize the exception."""
        self.instance_file = instance_file
        self.e = e
        message = e.message
        if e.absolute_path:  # the error comes from a specific parameter
            path = os.path.join(*[str(i) for i in e.absolute_path])
            message += f"\nParameter: [bold yellow]{path}[/bold yellow]"
        super().__init__(self.message.format(instance_file=instance_file, e=message))
