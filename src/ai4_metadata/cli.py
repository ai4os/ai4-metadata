"""Command line interface for the ai4-metadata package."""

import typer

import ai4_metadata
from ai4_metadata import generate
from ai4_metadata import migrate
from ai4_metadata import validate

app = typer.Typer(help="AI4 Metadata tools and utils.")
# NOTE(aloga): do not use app.add_typer(<module>.app) as it will create a command group
# and add all commands as subcommands of that group.
# Check https://github.com/fastapi/typer/issues/187 for more details
app.registered_commands += generate.app.registered_commands
app.registered_commands += migrate.app.registered_commands
app.registered_commands += validate.app.registered_commands


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
