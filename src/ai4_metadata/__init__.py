"""AI4 Metadata validator."""

from contextlib import suppress
import importlib.metadata
import pathlib

import enum

__version__ = "2.3.1"


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


class MetadataVersions(str, enum.Enum):
    """Available versions of the AI4 metadata schema."""

    V2 = "2.1.0"
    V2_1_0 = "2.1.0"
    V2_0_0 = "2.0.0"

    V1 = "1.0.0"


_metadata_version_files = {
    MetadataVersions.V1: pathlib.Path(
        pathlib.Path(__file__).parent / f"schemata/ai4-apps-v{MetadataVersions.V1}.json"
    ),
    MetadataVersions.V2: pathlib.Path(
        pathlib.Path(__file__).parent / f"schemata/ai4-apps-v{MetadataVersions.V2}.json"
    ),
}

LATEST_METADATA_VERSION = MetadataVersions.V2


def get_latest_version() -> MetadataVersions:
    """Get the latest version of the AI4 metadata schema."""
    return LATEST_METADATA_VERSION


def get_schema(version: MetadataVersions) -> pathlib.Path:
    """Get the schema file path for a given version."""
    return _metadata_version_files[version]
