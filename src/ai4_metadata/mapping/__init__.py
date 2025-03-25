"""Module for mapping metadata between different formats."""

import pathlib
from typing_extensions import Annotated
from typing import Optional

import ai4_metadata
from ai4_metadata import exceptions
from ai4_metadata.mapping.profiles import mldcat
from ai4_metadata import utils
from ai4_metadata import validate

import typer

app = typer.Typer(help="Crosswalk metadata between different formats.")


# We only support one profile so far
SupportedInputProfiles = mldcat.SupportedInputProfiles


@app.command(name="map")
def _map(
    from_file: Annotated[
        pathlib.Path,
        typer.Argument(help="File to map from."),
    ],
    to_format: Annotated[
        mldcat.SupportedOutputFormats,
        typer.Option(
            "--output-format",
            help="Format to map to. Note that this depends on the input format.",
        ),
    ],
    to_profile: Annotated[
        mldcat.SupportedOutputProfiles,
        typer.Option("--output-profile", help="Profile to map to."),
    ],
    from_profile: Annotated[
        SupportedInputProfiles,
        typer.Option("--input-profile", help="Profile to map from."),
    ] = SupportedInputProfiles.ai4os,
    output: Annotated[
        Optional[pathlib.Path],
        typer.Option("--output", "-o", help="Output file for generated mapping."),
    ] = None,
    metadata_version: Annotated[
        ai4_metadata.MetadataVersions,
        typer.Option(help="AI4 application metadata version."),
    ] = ai4_metadata.get_latest_version(),
) -> None:
    """Generate a mapping file between two formats."""
    schema = ai4_metadata.get_schema(metadata_version)
    try:
        validate.validate(from_file, schema)
    except exceptions.MetadataValidationError as e:
        utils.format_rich_error(e)
        raise typer.Exit(1)
    except Exception as e:
        utils.format_rich_error(e)
        raise typer.Exit(4)

    try:
        metadata = utils.load_json(from_file)
    except exceptions.InvalidJSONError:
        metadata = utils.load_yaml(from_file)

    if to_profile == mldcat.SupportedOutputProfiles.mldcat:
        try:
            mapping = mldcat.generate_mapping(
                from_profile=from_profile,
                from_metadata=metadata,
                to_format=to_format,
                metadata_version=metadata_version,
            )
        except exceptions.InvalidMappingError as e:
            utils.format_rich_error(e)
            raise typer.Exit(1)

    if output:
        with open(output, "wb") as f:
            f.write(mapping.encode("utf-8"))
    else:
        typer.echo(mapping)
