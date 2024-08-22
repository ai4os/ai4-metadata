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

    # NOTE(aloga): this works for the current schema, but we need to handle this
    # recursively in order to make it work for nested objects
    for key, value in properties.items():
        # If type is object, we need to go deeper
        if value.get("type") == "object":
            required_sub = value.get("required", [])
            if required_only:
                value["properties"] = {
                    k: v
                    for k, v in value.get("properties").items()
                    if k in required_sub
                }
            generated_json[key] = collections.OrderedDict()
            for sub_key, sub_value in value.get("properties").items():
                if sample_values:
                    generated_json[key][sub_key] = sub_value.get("example", "")
                else:
                    generated_json[key][sub_key] = ""
        elif value.get("type") == "array":
            if sample_values:
                generated_json[key] = value.get("example", [])
            else:
                generated_json[key] = []
        else:
            if sample_values:
                generated_json[key] = value.get("example", "")
            else:
                generated_json[key] = ""

    return generated_json
