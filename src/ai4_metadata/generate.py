"""Generate an AI4 metadata follwowing schema with empty of with samples."""

import collections
import json
import pathlib
import typing

from ai4_metadata import exceptions


def generate(
    schema: typing.Union[pathlib.Path, str],
    sample_values: bool = False,
    required_only: bool = False,
) -> collections.OrderedDict:
    """Generate an AI4 metadata schema empty of with samples."""
    schema_json = json.load(open(schema, "r"))

    properties = schema_json.get("properties")
    required = schema_json.get("required", [])

    if required_only:
        properties = {k: v for k, v in properties.items() if k in required}

    if not properties:
        raise exceptions.InvalidSchemaError(
            schema, "No definitions found in the schema."
        )

    generated_json: collections.OrderedDict[str, typing.Any] = collections.OrderedDict()

    version = properties.pop("metadata_version").get("example")
    generated_json["metadata_version"] = version

    for key, value in properties.items():
        generated_json[key] = _get_field_value(value, sample_values)

    return generated_json


def _get_field_value(value: dict, sample_values: bool = False) -> typing.Any:
    """Get the value of a field."""
    if value.get("type") == "object":
        required = value.get("required", [])

        properties = value.get("properties", {})
        if required:
            properties = {k: v for k, v in properties.items() if k in required}

        aux = collections.OrderedDict()
        for key, sub_value in properties.items():
            aux[key] = _get_field_value(sub_value, sample_values)
        return aux
    elif value.get("type") == "array":
        if sample_values:
            return value.get("example", [])
        else:
            return []
    else:
        if sample_values:
            return value.get("example", "")
        else:
            return ""
