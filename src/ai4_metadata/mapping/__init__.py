"""Module for mapping metadata between different formats."""

import enum
import pathlib
from typing_extensions import Annotated
from typing import Optional

from ai4_metadata import metadata
from ai4_metadata import exceptions
from ai4_metadata.mapping.profiles import mldcat
from ai4_metadata import utils
from ai4_metadata import validate

import typer

app = typer.Typer(help="Crosswalk metadata between different formats.")


class SupportedInputProfiles(str, enum.Enum):
    """Supported input profiles for crosswalks."""

    ai4os = "ai4os"


class SupportedOutputProfiles(str, enum.Enum):
    """Supported output profiles for crosswalks."""

    mldcat = mldcat.SupportedOutputProfiles.mldcat.value


class OutputFormatMapping(enum.Enum):
    """Supported output formats for crosswalks."""

    mldcat = list(mldcat.SupportedOutputFormats.__members__.values())


def generate_output_formats() -> enum.Enum:
    """Generate the output formats for the command."""
    output_formats = {}

    for _, allowed_formats in OutputFormatMapping.__members__.items():
        for format_ in allowed_formats.value:
            output_formats[format_.name] = format_.value

    return enum.Enum("OutputFormatMapping", output_formats)


SupportedOutputFormats = generate_output_formats()


def mapping(
    from_metadata: dict,
    from_profile: SupportedInputProfiles,
    to_format: mldcat.SupportedOutputFormats,
    to_profile: SupportedOutputProfiles,
    metadata_version: metadata.MetadataVersions,
) -> str:
    """Generate a mapping file for a given input and output format.

    This command does not validate the input metadata, so it is assumed to be
    correct. If the input metadata is not correct, the command will fail with
    an exception.
    """
    if from_profile not in SupportedInputProfiles.__members__:
        raise exceptions.InvalidMappingError(
            msg=f"input format `{from_profile}` not supported."
        )
    if to_profile not in mldcat.SupportedOutputProfiles.__members__:
        raise exceptions.InvalidMappingError(
            msg=f"output format `{to_profile}` not supported."
        )

    if to_profile == mldcat.SupportedOutputProfiles.mldcat:
        try:
            mapping = mldcat.generate_mapping(
                from_profile=from_profile,
                from_metadata=from_metadata,
                to_format=to_format,
                metadata_version=metadata_version,
            )
        except exceptions.InvalidMappingError as e:
            utils.format_rich_error(e)
            raise typer.Exit(1)
    else:
        raise NotImplementedError(
            f"output profile `{to_profile}` not supported for MLDCAT-API profile."
        )

    return mapping


help_aux_str = ""

for profile, allowed_formats in OutputFormatMapping.__members__.items():
    for value in allowed_formats.value:
        help_aux_str += f"\t\t- {profile}: {value.value}\n\n"


@app.command(
    name="map",
    help=f"""
    Generate a mapping file between two formats.

    Supported output formats are dependant on the output profile. The following
    profiles and formats are supported.

    {help_aux_str}
    """,
)
def _map(
    from_file: Annotated[
        pathlib.Path,
        typer.Argument(help="File to map from."),
    ],
    # Ignore type because mypy cannot infer the type of the enum type that
    # we dynamically define above
    to_format: Annotated[  # type: ignore
        SupportedOutputFormats,
        typer.Option(
            "--output-format",
            help="Format to map to. Note that this depends on the input format.",
        ),
    ],
    to_profile: Annotated[
        SupportedOutputProfiles,
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
        metadata.MetadataVersions,
        typer.Option(help="AI4 application metadata version."),
    ] = metadata.get_latest_version(),
) -> None:
    """Generate a mapping file between two formats."""
    schema = metadata.get_schema(metadata_version)
    try:
        validate.validate(from_file, schema)
    except exceptions.MetadataValidationError as e:
        utils.format_rich_error(e)
        raise typer.Exit(1)
    except Exception as e:
        utils.format_rich_error(e)
        raise typer.Exit(4)

    try:
        meta = utils.load_json(from_file)
    except exceptions.InvalidJSONError:
        meta = utils.load_yaml(from_file)

    aux = mapping(meta, from_profile, to_format, to_profile, metadata_version)

    if output:
        with open(output, "wb") as f:
            f.write(aux.encode("utf-8"))
    else:
        typer.echo(aux)
