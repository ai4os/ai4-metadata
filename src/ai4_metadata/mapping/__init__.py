"""Module for mapping metadata between different formats."""

import enum

from ai4_metadata.mapping.profiles import mldcat

import typer

app = typer.Typer(help="Crosswalk between different metadata profiles and formats.")
# NOTE(aloga): do not use app.add_typer(<module>.app) as it will create a command group
# and add all commands as subcommands of that group.
# Check https://github.com/fastapi/typer/issues/187 for more details
app.registered_commands += mldcat.app.registered_commands


class SupportedOutputProfiles(str, enum.Enum):
    """Supported output profiles for crosswalks."""

    mldcat = mldcat


__all__ = ["app", "mldcat", "SupportedOutputProfiles"]
