"""Command line interface for the ai4-metadata package."""

import pathlib
from typing_extensions import Annotated, Optional
from typing import List
import warnings

import typer

import ai4_metadata
from ai4_metadata import generate
from ai4_metadata import exceptions
from ai4_metadata import migrate
from ai4_metadata import utils
from ai4_metadata import validate

app = typer.Typer()


@app.command(name="migrate")
def _migrate(
    v1_metadata: Annotated[
        pathlib.Path, typer.Argument(help="AI4 application metadata file to migrate.")
    ],
    output: Annotated[
        Optional[pathlib.Path],
        typer.Option("--output", "-o", help="Output file for migrated metadata."),
    ] = None,
):
    """Migrate an AI4 metadata file from V1 to the latest V2 version."""
    v1_schema = ai4_metadata.get_schema(ai4_metadata.MetadataVersions.V1)
    validate.validate(v1_metadata, v1_schema)

    # Migrate metadata
    v2_metadata = migrate.migrate(v1_metadata)
    v2_version = ai4_metadata.get_latest_version()
    v2_schema = ai4_metadata.get_schema(v2_version)
    validate.validate(v2_metadata, v2_schema)

    # Write out the migrated metadata
    utils.dump_json(v2_metadata, output)
    if output:
        utils.format_rich_ok(
            f"V1 metadata '{v1_metadata}' migrated to version {v2_version} and "
            f"stored in '{output}'",
        )


@app.command(name="validate")
def _validate(
    instances: Annotated[
        List[pathlib.Path],
        typer.Argument(
            help="AI4 application metadata file to validate. The file can "
            "be repeated to validate multiple files. Supported formats are "
            "JSON and YAML."
        ),
    ],
    schema: Annotated[
        Optional[pathlib.Path],
        typer.Option(help="AI4 application metadata schema file to use."),
    ] = None,
    metadata_version: Annotated[
        ai4_metadata.MetadataVersions,
        typer.Option(help="AI4 application metadata version."),
    ] = ai4_metadata.get_latest_version(),
    quiet: Annotated[
        bool, typer.Option("--quiet", "-q", help="Suppress output for valid instances.")
    ] = False,
):
    """Validate an AI4 metadata file against the AI4 metadata schema.

    This command receives an AI4 metadata file and validates it against a
    given version of the metadata schema. By default it will check against the latest
    metadata version.

    If the metadata is not valid it will exit with .

    If you provide the --shema option, it will override the --metadata-version option.
    """
    schema_file = schema or ai4_metadata.get_schema(metadata_version)

    exit_code = 0
    for instance_file in instances:
        try:
            validate.validate(instance_file, schema_file)
        except exceptions.FileNotFoundError as e:
            utils.format_rich_error(e)
            typer.Exit(2)
        except exceptions.InvalidFileError as e:
            utils.format_rich_error(e)
            typer.Exit(2)
        except exceptions.SchemaValidationError as e:
            utils.format_rich_error(e)
            typer.Exit(3)
        except exceptions.MetadataValidationError as e:
            utils.format_rich_error(e)
            exit_code = 1
        else:
            if not quiet:
                utils.format_rich_ok(
                    f"'{instance_file}' is valid for version {metadata_version.value}"
                )

    raise typer.Exit(code=exit_code)


@app.command(name="generate")
def _generate(
    metadata_version: Annotated[
        ai4_metadata.MetadataVersions,
        typer.Option(help="AI4 application metadata version."),
    ] = ai4_metadata.get_latest_version(),
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
    schema = ai4_metadata.get_schema(metadata_version)

    try:
        generated_json = generate.generate(schema, sample_values, required)
    except exceptions.InvalidSchemaError as e:
        utils.format_rich_error(e)
        raise typer.Exit(1)

    utils.dump_json(generated_json, output)

    validate.validate(generated_json, schema)

    if output:
        utils.format_rich_ok(
            f"Sample file stored in '{output}' for version {metadata_version.value}"
        )


def version_callback(value: bool):
    """Return the version for the --version option."""
    if value:
        typer.echo(ai4_metadata.extract_version())
        raise typer.Exit()


@app.callback()
def version(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Print the version and exit",
    )
):
    """Show version and exit."""
    pass


def migrate_main():
    """Run the migration command as an independent script."""
    # NOTE(aloga): This is a workaround to be able to provide the command as a separate
    # script, in order to be compatible with previous versions of the package. However,
    # this will be not be supported in the next major version of the package, therfore
    # we mark it as deprecated and raise a warining
    msg = (
        "The 'ai4-metadata-migrate' command is deprecated and will be removed "
        "in the next major version of the package, please use 'ai4-metadata migrate' "
        "instead."
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)
    utils.format_rich_warning(DeprecationWarning(msg))
    typer.run(_migrate)


def validate_main():
    """Run the validation command as an independent script."""
    # NOTE(aloga): This is a workaround to be able to provide the command as a separate
    # script, in order to be compatible with previous versions of the package. However,
    # this will be not be supported in the next major version of the package, therfore
    # we mark it as deprecated and raise a warining
    msg = (
        "The 'ai4-metadata-validator' command is deprecated and will be removed "
        "in the next major version of the package, please use 'ai4-metadata validate' "
        "instead."
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)
    utils.format_rich_warning(DeprecationWarning(msg))
    typer.run(_validate)
