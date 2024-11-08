"""Utility functions for the AI4 Metadata utils."""

import json
import os
import pathlib
import typing

import rich
import rich.console
import rich.highlighter
import rich.panel
import yaml

from ai4_metadata import exceptions


def load_json(path: typing.Union[str, pathlib.Path]) -> typing.Dict:
    """Load a JSON from the file f."""
    try:
        file = open(path, "r")
        data = file.read()
        return json.loads(data)
    except FileNotFoundError:
        raise exceptions.FileNotFoundError(path)
    except json.JSONDecodeError as e:
        raise exceptions.InvalidJSONError(path, e)


def load_yaml(path: typing.Union[str, pathlib.Path]) -> typing.Dict:
    """Load a YAML from the file f."""
    try:
        file = open(path, "r")
        data = file.read()
        return yaml.safe_load(data)
    except FileNotFoundError:
        raise exceptions.FileNotFoundError(path)
    except yaml.YAMLError as e:
        raise exceptions.InvalidYAMLError(path, e)


def dump_json(data: typing.Dict, path: typing.Optional[pathlib.Path] = None) -> None:
    """Dump a JSON object to stdout or to path if provided."""
    if path is None:
        print(json.dumps(data, indent=4))
    else:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)


_TERMINAL_WIDTH = os.getenv("TERMINAL_WIDTH")
MAX_WIDTH = int(_TERMINAL_WIDTH) if _TERMINAL_WIDTH else None
ALIGN_ERRORS_PANEL: typing.Literal["left", "center", "right"] = "left"
STYLE_ERRORS_PANEL_BORDER = "bold red"
ALIGN_WARNING_PANEL: typing.Literal["left", "center", "right"] = "left"
STYLE_WARNING_PANEL_BORDER = "bold yellow"
ALIGN_OK_PANEL: typing.Literal["left", "center", "right"] = "left"
STYLE_OK_PANEL_BORDER = "bold green"


def _get_rich_console(stderr: bool = False) -> rich.console.Console:
    return rich.console.Console(
        width=MAX_WIDTH,
        stderr=stderr,
    )


def format_rich_error(
    error: typing.Union[Exception, exceptions.BaseExceptionError]
) -> None:
    """Format an error using rich."""
    console = _get_rich_console(stderr=True)
    console.print(
        rich.panel.Panel(
            f"{error}",
            title="Error",
            highlight=True,
            border_style=STYLE_ERRORS_PANEL_BORDER,
            title_align=ALIGN_ERRORS_PANEL,
        )
    )


def format_rich_warning(error: typing.Union[str, Exception]) -> None:
    """Format a warning using rich."""
    console = _get_rich_console(stderr=True)
    console.print(
        rich.panel.Panel(
            f"{error}",
            title="Warning",
            highlight=True,
            border_style=STYLE_WARNING_PANEL_BORDER,
            title_align=ALIGN_WARNING_PANEL,
        )
    )


def format_rich_ok(message: str) -> None:
    """Format a message using rich."""
    console = _get_rich_console(stderr=False)
    console.print(
        rich.panel.Panel(
            f"{message}",
            title="Success",
            highlight=True,
            border_style=STYLE_OK_PANEL_BORDER,
            title_align=ALIGN_OK_PANEL,
        )
    )
