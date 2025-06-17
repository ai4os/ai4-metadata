"""Module to generate mappings from AI4OS metadata to MLDCAT-API."""

import copy
import enum
import json
import pathlib
from typing_extensions import Annotated
from typing import Optional, Union

import typer
import rdflib

from ai4_metadata import metadata
from ai4_metadata import exceptions
from ai4_metadata import utils
from ai4_metadata import validate


# NOTE(aloga): move to GH pages or documentation as soon as possible.
_url_prefix = "https://docs.ai4os.eu/projects/ai4-metadata/en/latest/_static/json-ld"
MetadataVersions = metadata.MetadataVersions

_JSON_LD_CONTEXT = {
    MetadataVersions.V2: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
    MetadataVersions.V2_3_0: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
    MetadataVersions.V2_2_0: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
    MetadataVersions.V2_1_0: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
    MetadataVersions.V2_0_0: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
}


def get_context_for_version(version: MetadataVersions) -> str:
    """Get the context for a given version."""
    try:
        return _JSON_LD_CONTEXT[version]
    except KeyError:
        raise exceptions.InvalidMetadataVersionError(version)


app = typer.Typer(help="Support for mapping into MLDCAT-AP profile.")


class SupportedInputProfiles(str, enum.Enum):
    """Supported input profiles for crosswalks."""

    ai4os = "ai4os"


class SupportedOutputFormats(str, enum.Enum):
    """Supported input formats for crosswalks."""

    jsonld = "jsonld"
    ttl = "ttl"


def generate_mapping(
    from_profile: SupportedInputProfiles,
    from_metadata: dict,
    to_format: SupportedOutputFormats,
    metadata_version: MetadataVersions = MetadataVersions.V2,
) -> str:
    """Generate a mapping file for a given input and output format."""
    if from_profile not in SupportedInputProfiles.__members__:
        raise exceptions.InvalidMappingError(
            msg=f"input format `{from_profile}` not supported for MLDCAT-API profile."
        )

    if to_format not in SupportedOutputFormats.__members__:
        raise exceptions.InvalidMappingError(
            msg=f"output format `{to_format}` not supported for MLDCAT-API profile."
        )

    uri = from_metadata.get("links", {}).get("self", "")
    if not uri:
        uri = from_metadata.get("links", {}).get("source_code", "")

    new_meta = copy.deepcopy(from_metadata)
    new_meta["@context"] = get_context_for_version(metadata_version)
    new_meta["uri"] = uri
    new_meta["type"] = "MachineLearningModel"

    links = new_meta.pop("links", {})
    new_meta["links"] = {}
    for key, value in links.items():
        new_meta["links"][key] = format_link(key, value)

    for key in ["categories", "tasks", "libraries"]:
        old_meta = new_meta.pop(key, [])
        new_meta[key] = [as_object(cat, key) for cat in old_meta]

    license_ = new_meta.pop("license", None)
    if license_:
        new_meta["license"] = {
            "uri": license_.replace(" ", "_"),
            "title": license_,
            "type": "LicenseDocument",
        }

    if to_format == SupportedOutputFormats.ttl:
        graph = rdflib.Graph()
        graph.parse(data=json.dumps(new_meta), format="json-ld")
        turtle_data = graph.serialize(format="turtle")
        return str(turtle_data)
    else:
        return json.dumps(new_meta)


def format_link(key: str, value: str) -> Union[str, dict]:
    """Format a link to a URI object."""
    if key == "source_code":
        return {
            "uri": value,
            "type": "Repository",
            "title": "Source code",
        }
    elif key == "docker_image":
        return {
            "uri": value,
            "type": "Repository",
            "title": "Docker image",
        }
    elif key == "dataset":
        return {
            "uri": value,
            "type": "Dataset",
            "title": "Dataset",
        }
    else:
        return value


def as_object(object_name: str, object_category: str) -> dict:
    """Convert a dictionary to an object with a given type."""
    object_type_map = {
        "categories": "Concept",
        "tasks": "TaskType",
        "libraries": "Library",
    }

    return {
        "uri": object_name.replace(" ", "_"),
        "title": object_name,
        "type": object_type_map.get(object_category, "Concept"),
    }


@app.command(
    name="mldcat-ap", help="Map to MLDCAT-AP profile, with different renderings."
)
def _map(
    from_file: Annotated[
        pathlib.Path,
        typer.Argument(help="File to map from."),
    ],
    to_format: Annotated[
        SupportedOutputFormats,
        typer.Option(
            "--output-format",
            help="Format to map to. Note that this depends on the input format.",
        ),
    ],
    from_profile: Annotated[
        SupportedInputProfiles,
        typer.Option("--input-profile", help="Profile to map from."),
    ] = SupportedInputProfiles.ai4os,
    output: Annotated[
        Optional[pathlib.Path],
        typer.Option("--output", "-o", help="Output file for generated mapping."),
    ] = None,
    metadata_version: Annotated[
        Optional[metadata.MetadataVersions],
        typer.Option(help="AI4 application metadata version. Defaults to the latest."),
    ] = None,
) -> None:
    """Generate a mapping file between two formats."""
    if metadata_version is None:
        metadata_version = metadata.get_latest_version()
    schema = metadata.get_schema(metadata_version)

    try:
        validate.validate(from_file, schema)
    except exceptions.MetadataValidationError as e:
        utils.format_rich_error(e)
        raise typer.Exit(1)
    except Exception as e:
        utils.format_rich_error(e)
        raise typer.Exit(4)

    from_metadata = utils.load_file(from_file)

    try:
        mapping = generate_mapping(
            from_profile=from_profile,
            from_metadata=from_metadata,
            to_format=to_format,
            metadata_version=metadata_version,
        )
    except exceptions.InvalidMappingError as e:
        utils.format_rich_error(e)
        raise typer.Exit(1)

    if output:
        with open(output, "wb") as f:
            f.write(mapping.encode("utf-8"))
    else:
        typer.echo(mapping)
