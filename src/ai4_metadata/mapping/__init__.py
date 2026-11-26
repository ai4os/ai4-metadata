"""Module for mapping metadata between different formats."""

import pathlib
from typing import Optional

import typer
from typing_extensions import Annotated

from ai4_metadata import exceptions
from ai4_metadata import metadata
from ai4_metadata import utils
from ai4_metadata import validate
from ai4_metadata.mapping import registry
from ai4_metadata.mapping.profiles import base
from ai4_metadata.mapping.profiles import mldcatap

app = typer.Typer(help="Crosswalk between different metadata profiles and formats.")


def map_file(
    profile: base.Profile,
    from_file: pathlib.Path,
    to_format: base.SupportedOutputFormats,
    output: Optional[pathlib.Path],
    metadata_version: Optional[metadata.MetadataVersions],
    validate_shacl: bool = False,
) -> None:
    """Validate an AI4 metadata file, map it into a profile and write the result.

    If ``validate_shacl`` is set, the mapping is also validated against the profile
    SHACL shapes, and nothing is written if it does not conform.

    Exit codes: 1 if the metadata or the mapping are not valid, 4 on unexpected
    errors, 5 if SHACL validation is requested but pySHACL is not installed.
    """
    if metadata_version is None:
        metadata_version = metadata.get_latest_version()
    schema = metadata.get_schema(metadata_version)

    try:
        validate.validate_file(from_file, schema)
    except exceptions.MetadataValidationError as e:
        utils.format_rich_error(e)
        raise typer.Exit(1)
    except Exception as e:
        utils.format_rich_error(e)
        raise typer.Exit(4)

    if to_format not in profile.output_formats:
        error = exceptions.InvalidMappingError(
            msg=f"output format `{to_format.value}` not supported for "
            f"`{profile.name}` profile."
        )
        utils.format_rich_error(error)
        raise typer.Exit(1)

    from_metadata = utils.load_file(from_file)
    document = profile.to_jsonld(from_metadata, metadata_version)

    if validate_shacl:
        try:
            report = profile.validate_shacl(document)
        except exceptions.ShaclNotAvailableError as e:
            utils.format_rich_error(e)
            raise typer.Exit(5)
        if not report.conforms:
            utils.format_rich_error(
                exceptions.ShaclValidationError(profile.name, report.text)
            )
            raise typer.Exit(1)

    mapping = profile.serialize(document, to_format)

    if output:
        with open(output, "wb") as f:
            f.write(mapping.encode("utf-8"))
    else:
        typer.echo(mapping)


@app.command(name="mldcat-ap", help=mldcatap.PROFILE.description)
def _map_mldcatap(
    from_file: Annotated[
        pathlib.Path,
        typer.Argument(help="File to map from."),
    ],
    to_format: Annotated[
        base.SupportedOutputFormats,
        typer.Option(
            "--output-format",
            help="Format to map to. Note that this depends on the input format.",
        ),
    ],
    from_profile: Annotated[
        base.SupportedInputProfiles,
        typer.Option("--input-profile", help="Profile to map from."),
    ] = base.SupportedInputProfiles.ai4os,
    output: Annotated[
        Optional[pathlib.Path],
        typer.Option("--output", "-o", help="Output file for generated mapping."),
    ] = None,
    metadata_version: Annotated[
        Optional[metadata.MetadataVersions],
        typer.Option(help="AI4 application metadata version. Defaults to the latest."),
    ] = None,
    validate_shacl: Annotated[
        bool,
        typer.Option(
            "--shacl",
            help="Validate the mapping against the MLDCAT-AP SHACL shapes. Requires "
            "the optional 'shacl' extra to be installed.",
        ),
    ] = False,
) -> None:
    """Map an AI4 metadata file into the MLDCAT-AP profile."""
    map_file(
        registry.get_profile(mldcatap.PROFILE.name),
        from_file,
        to_format,
        output,
        metadata_version,
        validate_shacl,
    )


__all__ = ["app", "map_file", "mldcatap", "registry"]
