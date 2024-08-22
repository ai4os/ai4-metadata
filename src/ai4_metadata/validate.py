"""Main module for AI4 metadata validator."""

import pathlib
from jsonschema import validators
import jsonschema.exceptions
import typing

from ai4_metadata import exceptions
from ai4_metadata import utils


def validate(
    instance: typing.Union[dict, pathlib.Path], schema: typing.Union[dict, pathlib.Path]
) -> None:
    """Validate the schema."""
    if isinstance(instance, pathlib.Path):
        instance_file: typing.Union[str, pathlib.Path] = instance
        try:
            instance = utils.load_json(instance_file)
        except exceptions.InvalidJSONError:
            instance = utils.load_yaml(instance_file)
    else:
        instance_file = "no-file"

    if isinstance(schema, pathlib.Path):
        schema_file: typing.Union[str, pathlib.Path] = schema
        schema = utils.load_json(schema_file)
    else:
        schema_file = "no-file"

    try:
        validator = validators.validator_for(schema)
        validator.check_schema(schema)
    except jsonschema.exceptions.SchemaError as e:
        raise exceptions.SchemaValidationError(schema_file, e)

    try:
        validators.validate(instance, schema)
    except jsonschema.exceptions.ValidationError as e:
        raise exceptions.MetadataValidationError(instance_file, e)
