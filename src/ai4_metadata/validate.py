"""Main module for AI4 metadata validator."""

import pathlib
from jsonschema import validators
import jsonschema.exceptions
from typing_extensions import Annotated
from typing import List, Optional, Union
import warnings

import typer

import ai4_metadata
from ai4_metadata import exceptions
from ai4_metadata import utils

app = typer.Typer(help="Validate an AI4 metadata file (YAML, JSON) against the schema.")


def validate(
    instance: Union[dict, pathlib.Path], schema: Union[dict, pathlib.Path]
) -> None:
    """Validate the schema."""
    if isinstance(instance, pathlib.Path):
        instance_file: Union[str, pathlib.Path] = instance
        try:
            instance = utils.load_json(instance_file)
        except exceptions.InvalidJSONError:
            instance = utils.load_yaml(instance_file)
    else:
        instance_file = "no-file"

    if isinstance(schema, pathlib.Path):
        schema_file: Union[str, pathlib.Path] = schema
        schema = utils.load_json(schema_file)
    else:
        schema_file = "no-file"

    try:
        validator = validators.validator_for(schema)
        validator.check_schema(schema)
    except jsonschema.exceptions.SchemaError as e:
        raise exceptions.SchemaValidationError(schema_file, e)

    try:
        validators.validate(instance, schema)
    except jsonschema.exceptions.ValidationError as e:
        raise exceptions.MetadataValidationError(instance_file, e)


@app.command(name="validate")
def main(
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
            validate(instance_file, schema_file)
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
    typer.run(main)
