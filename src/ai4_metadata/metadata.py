"""Metadata schema for AI4 applications and its versions."""

import enum
import pathlib


class MetadataVersions(str, enum.Enum):
    """Available versions of the AI4 metadata schema."""

    V2 = "2.2.0"
    V2_3_0 = "2.3.0"
    V2_2_0 = "2.2.0"
    V2_1_0 = "2.1.0"
    V2_0_0 = "2.0.0"

    V1 = "1.0.0"


LATEST_METADATA_VERSION = MetadataVersions.V2

_metadata_version_files = {}
for version in MetadataVersions:
    _metadata_version_files[version] = pathlib.Path(
        pathlib.Path(__file__).parent
        / f"schemata/ai4-apps-v{version._value_}.json"  # noqa(W503)
    )


def get_latest_version() -> MetadataVersions:
    """Get the latest version of the AI4 metadata schema."""
    return LATEST_METADATA_VERSION


def get_schema(version: MetadataVersions) -> pathlib.Path:
    """Get the schema file path for a given version."""
    return _metadata_version_files[version]
