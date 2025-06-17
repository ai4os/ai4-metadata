"""Metadata schema for AI4 applications and its versions."""

import enum
import pathlib
from typing import Union

from jsonschema import validators
import jsonschema.exceptions

from ai4_metadata import exceptions
from ai4_metadata import utils


class MetadataVersions(str, enum.Enum):
    """Available versions of the AI4 metadata schema."""

    V2 = "2.3.0"
    V2_3_0 = "2.3.0"
    V2_2_0 = "2.2.0"
    V2_1_0 = "2.1.0"
    V2_0_0 = "2.0.0"

    V1 = "1.0.0"


LATEST_METADATA_VERSION = MetadataVersions.V2

_metadata_version_files = {}
for version in MetadataVersions:
    _metadata_version_files[version] = pathlib.Path(
        pathlib.Path(__file__).parent
        / f"assets/schemata/ai4-apps-v{version._value_}.json"  # noqa(W503)
    )


def get_latest_version() -> MetadataVersions:
    """Get the latest version of the AI4 metadata schema."""
    return LATEST_METADATA_VERSION


def get_schema_file(version: MetadataVersions) -> pathlib.Path:
    """Get the schema file path for a given version."""
    return _metadata_version_files[version]


def get_latest_schema_file() -> pathlib.Path:
    """Get the schema file path for the latest version."""
    return get_schema_file(get_latest_version())


def get_schema_file_from_metadata(metadata: dict) -> pathlib.Path:
    """Get the schema file path from a metadata dictionary."""
    try:
        version = metadata["metadata_version"]
    except (KeyError, AttributeError):
        raise exceptions.InvalidMetadataError("no-file", "metadata_version not found")
    return get_schema_file(version)


def get_schema(version: MetadataVersions) -> dict:
    """Get the schema for a given version."""
    schema_file = get_schema_file(version)
    return utils.load_json(schema_file)


def get_latest_schema() -> dict:
    """Get the schema for the latest version."""
    schema_file = get_latest_schema_file()
    return utils.load_json(schema_file)


def get_schema_from_metadata(metadata: dict) -> dict:
    """Get the schema from a metadata dictionary."""
    schema_file = get_schema_file_from_metadata(metadata)
    return utils.load_json(schema_file)


def get_validator_for_schema(
    schema: Union[dict, pathlib.Path],
) -> jsonschema.protocols.Validator:
    """Get the validator for a given schema.

    This function will return a validator for a given schema. It will guess if the
    schema is a dictionary or a file path, and will load the schema if it is a file.

    :returns: A validator for the schema.
    """
    schema_file = pathlib.Path("no-file")
    if isinstance(schema, pathlib.Path):
        schema_file = schema
        schema = utils.load_json(schema)

    try:
        # Get the validator class, and check the schema
        validator = validators.validator_for(schema)
        validator.check_schema(schema)
    except jsonschema.exceptions.SchemaError as e:
        raise exceptions.SchemaValidationError(schema_file, e)
    # Now return an instance of the validator class
    return validator(schema)


def get_validator_for_schema_file(
    schema_file: pathlib.Path,
) -> jsonschema.protocols.Validator:
    """Get the validator for a given schema file."""
    return get_validator_for_schema(schema_file)
