"""Generate an AI4 metadata follwowing schema with empty of with samples."""

import collections
import pathlib
from typing_extensions import Annotated, Optional
from typing import Any

import typer

from ai4_metadata import metadata
from ai4_metadata import exceptions
from ai4_metadata import utils
from ai4_metadata import validate

app = typer.Typer(help="Generate an AI4 metadata file (empty or with sample values).")


def generate(
    schema: dict,
    sample_values: bool = False,
    required_only: bool = False,
) -> collections.OrderedDict:
    """Generate an AI4 metadata schema empty of with samples."""
    properties = schema.get("properties", {})
    required = schema.get("required", [])

    if required_only:
        properties = {k: v for k, v in properties.items() if k in required}

    if not properties:
        raise exceptions.InvalidSchemaError(
            "no-file", "No definitions found in the schema."
        )

    generated_json: collections.OrderedDict[str, Any] = collections.OrderedDict()

    version = properties.pop("metadata_version").get("example")
    generated_json["metadata_version"] = version

    for key, value in properties.items():
        generated_json[key] = _get_field_value(value, sample_values)

    return generated_json


def _get_field_value(value: dict, sample_values: bool = False) -> Any:
    """Get the value of a field based on its type definition."""
    # Get the field type, default to string if not specified
    field_type = value.get("type", "string")

    # Handle different field types
    if field_type == "object":
        result = collections.OrderedDict()

        # Get properties to include
        properties = value.get("properties", {})
        if value.get("required"):
            properties = {k: v for k, v in properties.items() if k in value["required"]}

        # Process each property
        for key, prop in properties.items():
            result[key] = _get_field_value(prop, sample_values)
        return result

    elif field_type == "array":
        return value.get("example", []) if sample_values else []

    elif field_type in ["integer", "number"]:
        return value.get("example", 0) if sample_values else 0

    else:  # string, boolean, null, etc.
        return value.get("example", "") if sample_values else ""


@app.command(name="generate")
def _main(
    metadata_version: Annotated[
        Optional[metadata.MetadataVersions],
        typer.Option(help="AI4 application metadata version. Defaults to the latest."),
    ] = None,
    sample_values: Annotated[
        bool, typer.Option("--sample-values", help="Generate sample values.")
    ] = False,
    required: Annotated[
        bool, typer.Option("--required-only", help="Include only required fields.")
    ] = False,
    output: Annotated[
        Optional[pathlib.Path],
        typer.Option("--output", "-o", help="Output file for generated metadata."),
    ] = None,
):
    """Generate an AI4 metadata schema."""
    if metadata_version is None:
        metadata_version = metadata.get_latest_version()
    schema = metadata.get_schema(metadata_version)

    try:
        generated_json = generate(schema, sample_values, required)
    except exceptions.InvalidSchemaError as e:
        schema_file = metadata.get_schema_file(metadata_version)
        e = exceptions.InvalidSchemaError(schema_file, e.e)
        utils.format_rich_error(e)
        raise typer.Exit(1)

    utils.dump_json(generated_json, output)

    try:
        validate.validate(generated_json, schema)
    except exceptions.MetadataValidationError as e:
        utils.format_rich_error(e)
        raise typer.Exit(1)

    if output:
        utils.format_rich_ok(
            f"Sample file stored in '{output}' for version {metadata_version.value}"
        )
