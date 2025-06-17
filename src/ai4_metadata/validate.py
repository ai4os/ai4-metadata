"""Main module for AI4 metadata validator."""

import pathlib
import jsonschema.exceptions
from typing_extensions import Annotated
from typing import List, Optional, Union
import warnings

import typer

from ai4_metadata import metadata
from ai4_metadata import exceptions
from ai4_metadata import utils

app = typer.Typer(help="Validate an AI4 metadata file (YAML, JSON) against the schema.")


def validate(
    instance: Union[dict, pathlib.Path], schema: Union[dict, pathlib.Path]
) -> None:
    """Validate the schema.

    :param instance: JSON instance to validate or path to a file.
    :param schema: JSON schema to validate against, or a path to a schema file.

    :raises SchemaValidationError: If the schema is invalid.
    :raises MetadataValidationError: If the metadata is invalid.
    """
    msg = (
        "Using the 'validate' method is deprecated and will be removed in the next "
        "major version of the package, please use one of "
        "'validate_file' or 'validate_json' instead."
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)

    if isinstance(instance, pathlib.Path):
        validate_file(instance, schema)
    else:
        validate_json(instance, schema)


def validate_file(
    instance_file: pathlib.Path, schema: Union[dict, pathlib.Path]
) -> None:
    """Validate a file against a schema.

    :param instance_file: Path to the file to validate.
    :param schema: JSON/YAML schema to validate against, or a path to a schema file.

    :raises SchemaValidationError: If the schema is invalid.
    :raises MetadataValidationError: If the metadata is invalid.
    """
    instance = utils.load_file(instance_file)

    try:
        validate_json(instance, schema)
    except exceptions.MetadataValidationError as e:
        raise exceptions.MetadataValidationError(instance_file, e.e)


def validate_json(instance: dict, schema: Union[dict, pathlib.Path]) -> None:
    """Validate a JSON with a given schema.

    :param instance: JSON instance to validate.
    :param schema: JSON schema to validate against, or a path to a schema file.

    :raises SchemaValidationError: If the schema is invalid.
    """
    validator = metadata.get_validator_for_schema(schema)

    try:
        validator.validate(instance)
    except jsonschema.exceptions.ValidationError as e:
        raise exceptions.MetadataValidationError("no-file", e)


@app.command(name="validate")
def _main(
    metadata_file: Annotated[
        List[pathlib.Path],
        typer.Argument(
            help="AI4 application metadata file to validate. Supported formats are "
            "JSON and YAML."
            "\n\n\n\nValidating more than one file is deprecated and will "
            "be removed in the next major version of the package.",
            show_default=False,
        ),
    ],
    schema: Annotated[
        Optional[pathlib.Path],
        typer.Option(help="AI4 application metadata schema file to use."),
    ] = None,
    metadata_version: Annotated[
        Optional[metadata.MetadataVersions],
        typer.Option(help="AI4 application metadata version. Defaults to the latest."),
    ] = None,
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
    if metadata_version is None:
        metadata_version = metadata.get_latest_version()
    schema_file = schema or metadata.get_schema(metadata_version)

    if len(metadata_file) > 1:
        msg = (
            "Validating multiple files is deprecated and will be removed in the next "
            "major version of the package, please validate each file separately."
        )
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        utils.format_rich_warning(DeprecationWarning(msg))

    exit_code = 0
    for instance_file in metadata_file:
        try:
            validate_file(instance_file, schema_file)
        # NOTE(aloga): we catch the exceptions that are fatal (i.e. files not found,
        # invalid files, etc) and exit right away. For the rest of the exceptions we
        # just print the error and continue with the next file
        except (exceptions.FileNotFoundError, exceptions.InvalidFileError) as e:
            utils.format_rich_error(e)
            raise typer.Exit(2)
        except exceptions.SchemaValidationError as e:
            utils.format_rich_error(e)
            raise typer.Exit(3)
        except exceptions.MetadataValidationError as e:
            # This case does not need to exit, but to continue with the next file
            # and set the exit code to 1, so that at the end we exit with an error
            utils.format_rich_error(e)
            exit_code = 1
        except Exception as e:
            # If we arrive here is because we have an unexpected error, we print the
            # error and exit with an error code
            utils.format_rich_error(e)
            raise typer.Exit(4)
        else:
            if not quiet:
                utils.format_rich_ok(
                    f"'{instance_file}' is valid for version {metadata_version.value}"
                )

    raise typer.Exit(code=exit_code)


def _validate_main():
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
    typer.run(_main)
