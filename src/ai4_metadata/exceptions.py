"""Custom exceptions for the metadata schema validation tool."""

import pathlib
import typing

import jsonschema.exceptions


class BaseExceptionError(Exception):
    """Base exception for the metadata schema validation tool."""

    message = "An error occurred."


class InvalidJSONError(BaseExceptionError):
    """Exception raised when a JSON file is invalid."""

    message = "Error loading JSON file '{f}': {e}"

    def __init__(self, f: typing.Union[str, pathlib.Path], e: Exception):
        """Initialize the exception."""
        self.f = f
        self.e = e
        super().__init__(self.message.format(f=f, e=e))


class SchemaValidationError(BaseExceptionError):
    """Exception raised when a schema is invalid."""

    message = "Error validating schema '{schema_file}': {e}"

    def __init__(
        self,
        schema_file: typing.Union[str, pathlib.Path],
        e: Exception
    ):
        """Initialize the exception."""
        self.e = e
        super().__init__(self.message.format(schema_file=schema_file, e=e))


class MetadataValidationError(BaseExceptionError):
    """Exception raised when a metadata file is invalid."""

    message = "Error validating instance '{instance_file}': {e}"

    def __init__(
        self,
        instance_file: typing.Union[str, pathlib.Path],
        e: jsonschema.exceptions.ValidationError
    ):
        """Initialize the exception."""
        self.instance_file = instance_file
        self.e = e
        super().__init__(self.message.format(instance_file=instance_file, e=e.message))
