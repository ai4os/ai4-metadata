"""Command line interface for the ai4-metadata package."""

import typer

import ai4_metadata
from ai4_metadata import generate
from ai4_metadata import migrate
from ai4_metadata import validate

app = typer.Typer(help="AI4 Metadata tools and utils.")
app.add_typer(generate.app, name="generate")
app.add_typer(migrate.app, name="migrate")
app.add_typer(validate.app, name="validate")


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
