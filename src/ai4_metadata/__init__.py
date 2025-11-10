"""AI4 Metadata validator."""

from contextlib import suppress
import importlib.metadata
import pathlib

from . import metadata
from . import generate
from . import migrate
from . import mapping
from . import validate

__version__ = "2.4.2"


def extract_version() -> str:
    """Return either the version of the package installed."""
    with suppress(FileNotFoundError, StopIteration):
        root_dir = pathlib.Path(__file__).parent.parent.parent
        with open(root_dir / "pyproject.toml", encoding="utf-8") as pyproject_toml:
            version = (
                next(line for line in pyproject_toml if line.startswith("version"))
                .split("=")[1]
                .strip("'\"\n ")
            )
            return f"{version}-dev (at {root_dir})"
    return importlib.metadata.version(__package__ or __name__.split(".", maxsplit=1)[0])


MetadataVersions = metadata.MetadataVersions
get_latest_version = metadata.get_latest_version
get_schema = metadata.get_schema


__all__ = [
    # From medatada.py
    "MetadataVersions",
    "get_latest_version",
    "get_schema",
    # From generate.py
    "generate",
    # From migrate.py
    "migrate",
    # From mapping
    "mapping",
    # From validate.py
    "validate",
    # From __init__.py
    "extract_version",
    "__version__",
]
