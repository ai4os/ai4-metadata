"""Generate an AI4 metadata follwowing schema with empty of with samples."""

import collections
import json
import pathlib
from typing_extensions import Annotated, Optional
from typing import Union, Any

import typer

from ai4_metadata import metadata
from ai4_metadata import exceptions
from ai4_metadata import utils
from ai4_metadata import validate

app = typer.Typer(help="Generate an AI4 metadata file (empty or with sample values).")


def generate(
    schema: Union[pathlib.Path, str],
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

    generated_json: collections.OrderedDict[str, Any] = collections.OrderedDict()

    version = properties.pop("metadata_version").get("example")
    generated_json["metadata_version"] = version

    for key, value in properties.items():
        generated_json[key] = _get_field_value(value, sample_values)

    return generated_json


def _get_field_value(value: dict, sample_values: bool = False) -> Any:
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
    elif value.get("type") in ["integer", "number"]:
        if sample_values:
            return value.get("example", 0)
        else:
            return 0
    else:
        if sample_values:
            return value.get("example", "")
        else:
            return ""


@app.command(name="generate")
def _main(
    metadata_version: Annotated[
        metadata.MetadataVersions,
        typer.Option(help="AI4 application metadata version."),
    ] = metadata.get_latest_version(),
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
    schema = metadata.get_schema(metadata_version)

    try:
        generated_json = generate(schema, sample_values, required)
    except exceptions.InvalidSchemaError as e:
        utils.format_rich_error(e)
        raise typer.Exit(1)

    utils.dump_json(generated_json, output)

    validate.validate(generated_json, schema)

    if output:
        utils.format_rich_ok(
            f"Sample file stored in '{output}' for version {metadata_version.value}"
        )
